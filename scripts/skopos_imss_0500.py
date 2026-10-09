"""On-demand consumer of the separately pinned IMSS 0500 Skopos source."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import sys
import time

from scripts import skopos_document_pilot as protocol


ROOT = Path(__file__).resolve().parents[1]
SKOPOS = Path('/Users/krisnova/www/aria/skopos')
RUN = SKOPOS / 'runs/pdf-imss-0500-pilot-v1'
SOURCE_URL = 'https://www.imss.gob.mx/sites/all/statics/pdf/manualesynormas/0500-002-001_3.pdf'
SOURCE_SHA = 'ce665959759f74331464471c71dc9cff107e061de09b8be5419a7cf1302e48b7'
PROVENANCE_SHA = '04164dc8de865957e0c6ea3bce29f47bf2d742beacabe83bf7bfc647e380669a'
POLICY_SHA = '6ba80ec17b74325f121b59243e9593c12a5bb272d87f8e9e41a6907cd6f12afc'
SOURCE = {
    'material_id': 'imss-0500-002-001-2022', 'source_revision': 1,
    'source_sha256': SOURCE_SHA,
    'custody_receipt_id': 'expertogobernanza:imss-0500-002-001-2022:1:ba8eb8c2180d6cc9',
    'custody_policy_sha256': '6a339819659469decb56ec610792eca85a1ec78b927bb04e66c5d090c7048f91',
}
DERIVATIVES = {
    'native': ('e86d5c6ab6d45d1143bc964fdcd4ecfeceda2c4a23965cc693655fd6b643eadd',
               'd9eeacbeab511a831999540136c72cb37c62f9aacb859fa6b75389f83e8f1ab0'),
    'ocr': ('6c05342bb617c0ce59a2346840b9a8e3c47eae14fa660703538731187526e433',
            'f58f4143b395d222ec64f3472109af26474c9bb56aa0e4cf7000412f81a9b49c'),
    'graph': ('2f6e9554c1f273485c4e06a65d3608072c614df601607d12d43335f2e52c1c82',
              '9ed5ee6ddcbdcd679782e6899f672653cee3135eeaf7b3a68f1504aefe1e13e7'),
}


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def preflight():
    pdf = ROOT / 'docs/fuentes/imss/0500-002-001_3.pdf'
    provenance = ROOT / 'docs/fuentes/imss/0500-002-001_3-PROCEDENCIA.md'
    require(protocol.digest(pdf.read_bytes()) == SOURCE_SHA, 'source_changed')
    require(protocol.digest(provenance.read_bytes()) == PROVENANCE_SHA,
            'provenance_changed')
    policy = json.loads((RUN / 'document-policy.json').read_bytes())
    require(protocol.digest(protocol.canonical(policy)) == POLICY_SHA,
            'policy_changed')
    require(policy['source_sha256'] == SOURCE_SHA and policy['max_page'] == 80 and
            policy['requests_root'] == str(RUN / 'requests') and
            policy['delivery_root'] == str(RUN / 'document-delivery'),
            'policy_scope_changed')
    host = json.loads((RUN / 'document-host.json').read_bytes())
    require(host['schema'] == 'skopos/pdf-document-host-config/v0.2' and
            host['policy_path'] == str(RUN / 'document-policy.json') and
            host['socket_path'] == str(RUN / 'document.sock') and
            host['database'] == 'skopos_pdf_imss_pilot_v1', 'host_changed')
    require((RUN / 'requests').is_dir() and (RUN / 'document-delivery').is_dir(),
            'roots_missing')


@contextmanager
def local_host():
    preflight()
    py = str(SKOPOS / '.venv/bin/python')
    controller = str(SKOPOS / 'scripts/pdf_custody_pilot.py')
    subprocess.run([py, controller, 'preflight'], cwd=SKOPOS, check=True,
                   stdout=subprocess.DEVNULL)
    socket_path = RUN / 'document.sock'
    require(not socket_path.exists(), 'host_already_running')
    process = None
    started = False
    try:
        subprocess.run([py, controller, 'start'], cwd=SKOPOS, check=True,
                       stdout=subprocess.DEVNULL)
        started = True
        descriptor = os.open(RUN / 'document-host.operational.log',
                             os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW,
                             0o600)
        with os.fdopen(descriptor, 'ab') as log:
            process = subprocess.Popen(
                [py, '-m', 'skopos', 'document-host', 'serve',
                 '--config', str(RUN / 'document-host.json')],
                cwd=SKOPOS, stdout=log, stderr=log)
        for _ in range(50):
            require(process.poll() is None, 'host_start_failed')
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe:
                    probe.settimeout(1)
                    probe.connect(str(socket_path))
                break
            except (FileNotFoundError, ConnectionRefusedError, socket.timeout):
                time.sleep(0.2)
        else:
            raise RuntimeError('host_not_ready')
        yield socket_path
    finally:
        errors = []
        if process is not None:
            try:
                if process.poll() is None:
                    process.terminate()
                process.wait(timeout=10)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
                errors.append('host_forced_stop_reconcile_socket')
        if started:
            try:
                subprocess.run([py, controller, 'stop'], cwd=SKOPOS, check=True,
                               stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                errors.append('mongo_stop_unconfirmed')
        if socket_path.exists():
            errors.append('host_socket_remains')
        if started:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                probe.settimeout(0.5)
                if probe.connect_ex(('127.0.0.1', 37034)) == 0:
                    errors.append('mongo_port_remains')
        require(not errors, ','.join(errors))


def call(socket_path, operation, **fields):
    request_id = 'eg-0500-' + secrets.token_hex(10)
    payload = protocol.request(operation, request_id, source=SOURCE, **fields)
    response, _ = protocol.exchange(socket_path, RUN / 'requests', payload)
    require(response['status'] == 'ok', f'{operation}:{response.get("error")}')
    return response['result']


def manifest(socket_path, name):
    derivation_id, manifest_sha = DERIVATIVES[name]
    output_ref = 'eg-0500-' + secrets.token_hex(12) + '.json'
    output = RUN / 'document-delivery' / output_ref
    try:
        result = call(socket_path, 'fetch_derivative', derivation_id=derivation_id,
                      manifest_sha256=manifest_sha, artifact_id='manifest',
                      artifact_sha256=manifest_sha, output_ref=output_ref)
        raw = output.read_bytes()
        require(result['sha256'] == protocol.digest(raw) == manifest_sha and
                result['byte_length'] == len(raw), 'manifest_delivery_mismatch')
        value = json.loads(raw)
        expected_pages = (list(range(1, 81)) if name == 'native' else
                          [1, 37] if name == 'ocr' else [37])
        require(value['parent'] == SOURCE and value['page_count'] == 80 and
                value['derivation_id'] == derivation_id and
                [p['page_number'] for p in value['pages']] == expected_pages,
                'manifest_identity_mismatch')
        return value
    finally:
        output.unlink(missing_ok=True)


def run(args):
    with local_host() as socket_path:
        if args.operation == 'search':
            manifest(socket_path, 'native')
            result = call(socket_path, 'search_document',
                          derivation_id=DERIVATIVES['native'][0],
                          manifest_sha256=DERIVATIVES['native'][1],
                          term=args.term, limit=args.limit)
            require(all(item['parent'] == SOURCE and
                        item['manifest_sha256'] == DERIVATIVES['native'][1]
                        for item in result['candidates']), 'candidate_lineage_changed')
        else:
            name = ('graph' if args.operation == 'graph' else
                    'ocr' if args.operation == 'ocr' or args.page == 1 or
                    (args.operation == 'item' and args.modality == 'ocr_text')
                    else 'native')
            value = manifest(socket_path, name)
            page = next((p for p in value['pages'] if p['page_number'] == args.page), None)
            require(page is not None, 'page_unavailable')
            if args.operation == 'item':
                result = call(socket_path, 'fetch_evidence',
                              derivation_id=DERIVATIVES[name][0],
                              manifest_sha256=DERIVATIVES[name][1],
                              item_id=args.item_id)
                layer_name = 'ocr_text' if name == 'ocr' else 'native_text'
                require(result['parent'] == SOURCE and
                        result['page_number'] == args.page and
                        result['modality'] == layer_name and
                        result['item'] in page[layer_name]['lines'],
                        'item_page_mismatch')
            elif args.operation == 'graph':
                result = {'page_number': 37, 'status': page['visual_graph']['status'],
                          'nodes': page['visual_graph']['nodes'],
                          'edges': page['visual_graph']['edges'],
                          'fidelity_status': value['fidelity_status'],
                          'derivation_id': DERIVATIVES[name][0],
                          'manifest_sha256': DERIVATIVES[name][1]}
            else:
                layer_name = 'ocr_text' if name == 'ocr' else 'native_text'
                layer = page[layer_name]
                require(layer['status'] == 'extracted', 'page_text_unavailable')
                result = {'page_number': args.page, 'modality': layer_name,
                          'status': layer['status'], 'lines': layer['lines'],
                          'derivation_id': DERIVATIVES[name][0],
                          'manifest_sha256': DERIVATIVES[name][1]}
    return {'status': 'ok', 'source': SOURCE, 'source_url': SOURCE_URL,
            'citation_rule': 'verify_page_and_fragment_visually_before_new_quote',
            'content_currentness': 'not_established', 'operation': args.operation,
            'result': result, 'runtime': 'stopped'}


def main():
    signal.signal(signal.SIGTERM, lambda _number, _frame: sys.exit(143))
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    page = commands.add_parser('page')
    page.add_argument('page', type=int, choices=range(1, 81))
    ocr = commands.add_parser('ocr')
    ocr.add_argument('page', type=int, choices=(1, 37))
    search = commands.add_parser('search')
    search.add_argument('term')
    search.add_argument('--limit', type=int, choices=range(1, 21), default=5)
    item = commands.add_parser('item')
    item.add_argument('page', type=int, choices=range(1, 81))
    item.add_argument('item_id')
    item.add_argument('--modality', choices=('native_text', 'ocr_text'),
                      default='native_text')
    commands.add_parser('graph')
    args = parser.parse_args()
    if args.operation == 'graph':
        args.page = 37
    try:
        print(json.dumps(run(args), ensure_ascii=False, sort_keys=True))
        return 0
    except (RuntimeError, ValueError, OSError, KeyError, TypeError,
            subprocess.CalledProcessError, KeyboardInterrupt, SystemExit) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False),
              file=sys.stderr)
        return (error.code if isinstance(error, SystemExit) and
                isinstance(error.code, int) else
                130 if isinstance(error, KeyboardInterrupt) else 1)


if __name__ == '__main__':
    raise SystemExit(main())
