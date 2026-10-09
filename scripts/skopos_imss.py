"""Consulta local bajo demanda del PDF IMSS custodiado por Skopos."""

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import secrets
import signal
import socket
import subprocess
import sys
import time

from scripts import skopos_document_pilot as document


ROOT = Path(__file__).resolve().parents[1]
SKOPOS = Path('/Users/krisnova/www/aria/skopos')
RUN = SKOPOS / 'runs/pdf-document-imss-pilot-v1'
REQUESTS = ROOT / 'runs/pdf-custody-imss-pilot-v1/requests'
DELIVERY = RUN / 'delivery'
SOURCE_URL = 'https://www.imss.gob.mx/sites/all/statics/pdf/manualesynormas/2000-002-001.pdf'
POLICY_SHA = '4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b'
LABEL_CONFIG_SHA = 'b9333d73a7eabf4ed8bc5e272de20ad81954f9edeaa3eb2c82f708b2e916888f'
LABEL_MANIFEST_SHA = '0d79b1e5d10219e844aa54b3d470ccf57a5868611a5a4fe8b5fb1d0fce58e20a'
LABEL_DERIVATION = 'ae1609defbfc0d6441452cae23a36bc6109fadce0ab51b4dfab0fa55dda7b778'
NATIVE = ('372fdaef7fb1171ec8dce708b79ef1e32b38e43dfb1b079e6b27ae070d8f7587',
          '7f81b1616b10549439cd536737e76663cfea7cec3bf7a6ec3fbf10241d8292ed')
OCR = ('7f132071b5e1c372e41d0ce9a83df7c966955c7fcb7036f80cdcbcecf5654a46',
       '3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d')
LABEL_CONTRACT = 'expertogobernanza/skopos-graph-labels'
LABEL_VERSION = 'v0.5-local'
LABEL_SCHEMA = 'skopos/pdf-graph-labels-host/v0.5-local'


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def local_preflight(kind):
    pdf = ROOT / 'docs/fuentes/imss/2000-002-001.pdf'
    require(sha(pdf.read_bytes()) == document.SOURCE_SHA, 'source_changed')
    require(sha((ROOT / 'docs/fuentes/imss/2000-002-001-PROCEDENCIA.md').read_bytes())
            == document.PROVENANCE_SHA, 'provenance_changed')
    require(REQUESTS.is_dir() and DELIVERY.is_dir(), 'roots_missing')
    policy = json.loads((RUN / 'policy.json').read_bytes())
    require(sha(document.canonical(policy)) == POLICY_SHA, 'policy_changed')
    require(policy['source_sha256'] == document.SOURCE_SHA and
            policy['requests_root'] == str(REQUESTS), 'policy_source_or_root_changed')
    if kind == 'label':
        config = json.loads((RUN / 'graph-labels-v05-host.json').read_bytes())
        require(sha(document.canonical(config)) == LABEL_CONFIG_SHA and
                config['manifest_sha256'] == LABEL_MANIFEST_SHA and
                config['socket_path'] == str(RUN / 'graph-labels-v05.sock'),
                'label_config_changed')
        manifest = (SKOPOS / 'docs/evidencia/pdf-imss-graph-labels-v0.5-local.json')
        require(sha(manifest.read_bytes()) == LABEL_MANIFEST_SHA,
                'label_manifest_changed')
    else:
        host = json.loads((RUN / 'host.json').read_bytes())
        require(host['socket_path'] == str(RUN / 'document.sock') and
                host['database'] == 'skopos_pdf_imss_pilot_v1', 'document_host_changed')


@contextmanager
def local_host(kind):
    local_preflight(kind)
    py = str(SKOPOS / '.venv/bin/python')
    controller = str(SKOPOS / 'scripts/pdf_custody_pilot.py')
    subprocess.run([py, controller, 'preflight'], cwd=SKOPOS, check=True,
                   stdout=subprocess.DEVNULL)
    socket_path = RUN / ('graph-labels-v05.sock' if kind == 'label' else 'document.sock')
    require(not socket_path.exists(), 'host_already_running')
    process = None
    started = False
    try:
        subprocess.run([py, controller, 'start'], cwd=SKOPOS, check=True,
                       stdout=subprocess.DEVNULL)
        started = True
        command = ([py, '-m', 'skopos.pdf_graph_labels_v05_host', 'serve',
                    '--config', str(RUN / 'graph-labels-v05-host.json')]
                   if kind == 'label' else
                   [py, '-m', 'skopos', 'document-host', 'serve',
                    '--config', str(RUN / 'host.json')])
        log_path = RUN / ('graph-labels-v05-host.stdout.log' if kind == 'label'
                          else 'document-host.operational.log')
        descriptor = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW,
                             0o600)
        with os.fdopen(descriptor, 'ab') as log:
            process = subprocess.Popen(command, cwd=SKOPOS, stdout=log, stderr=log)
        for _ in range(50):
            require(process.poll() is None, 'host_start_failed')
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
                    connection.settimeout(1)
                    connection.connect(str(socket_path))
                break
            except (FileNotFoundError, ConnectionRefusedError, socket.timeout):
                time.sleep(0.2)
        else:
            raise RuntimeError('host_not_ready')
        yield socket_path
    finally:
        cleanup_errors = []
        if process is not None:
            try:
                if process.poll() is None:
                    process.terminate()
                process.wait(timeout=10)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                try:
                    process.kill()
                    process.wait(timeout=5)
                    cleanup_errors.append('host_forced_stop_reconcile_socket')
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    cleanup_errors.append('host_stop_unconfirmed')
        if started:
            try:
                subprocess.run([py, controller, 'stop'], cwd=SKOPOS, check=True,
                               stdout=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                cleanup_errors.append('mongo_stop_unconfirmed')
        if socket_path.exists():
            cleanup_errors.append('host_socket_remains')
        if started:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                probe.settimeout(0.5)
                if probe.connect_ex(('127.0.0.1', 37034)) == 0:
                    cleanup_errors.append('mongo_port_remains')
        require(not cleanup_errors, ','.join(cleanup_errors))


def document_call(socket_path, operation, **fields):
    payload = document.request(operation, 'eg-operational-' + secrets.token_hex(10),
                               source=document.SOURCE, **fields)
    response, _ = document.exchange(socket_path, REQUESTS, payload)
    require(response['status'] == 'ok', f'{operation}:{response.get("error")}')
    return response['result']


def manifest(socket_path, pair):
    derivation_id, manifest_sha = pair
    ref = 'eg-operational-' + secrets.token_hex(12) + '.json'
    try:
        result = document_call(socket_path, 'fetch_derivative',
                               derivation_id=derivation_id, manifest_sha256=manifest_sha,
                               artifact_id='manifest', artifact_sha256=manifest_sha,
                               output_ref=ref)
        raw = (DELIVERY / ref).read_bytes()
        require(result['sha256'] == sha(raw) == manifest_sha and
                result['byte_length'] == len(raw), 'manifest_delivery_mismatch')
        value = json.loads(raw)
        require(value['derivation_id'] == derivation_id and
                value['parent'] == document.SOURCE and
                value['page_count'] == 188 and
                [page['page_number'] for page in value['pages']] ==
                (list(range(1, 189)) if pair == NATIVE else [1, 18, 19, 20, 21, 22]),
                'manifest_identity_mismatch')
        return value
    finally:
        (DELIVERY / ref).unlink(missing_ok=True)


def label_call(socket_path, operation, **fields):
    request_id = 'eg-v05-' + secrets.token_hex(10)
    payload = {'contract_id': LABEL_CONTRACT, 'contract_version': LABEL_VERSION,
               'request_id': request_id, 'project_id': 'expertogobernanza',
               'operation': operation, 'source': document.SOURCE,
               'labels_config_sha256': LABEL_CONFIG_SHA, **fields}
    raw = document.canonical(payload)
    nonce = secrets.token_hex(12)
    request_ref, envelope_ref = nonce + '.request.json', nonce + '.envelope.json'
    envelope = {'request_file_ref': request_ref, 'request_sha256': sha(raw),
                'request_id': request_id, 'contract_id': LABEL_CONTRACT,
                'contract_version': LABEL_VERSION}
    document.write_new(REQUESTS / request_ref, raw)
    document.write_new(REQUESTS / envelope_ref, document.canonical(envelope))
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(10)
        connection.connect(str(socket_path))
        connection.sendall(document.canonical({'envelope_ref': envelope_ref}) + b'\n')
        response_raw = connection.makefile('rb').readline(65537)
    require(0 < len(response_raw) <= 65536 and response_raw.endswith(b'\n'),
            'label_response_size')
    response = json.loads(response_raw)
    require(response.get('schema') == LABEL_SCHEMA and
            response.get('contract_id') == LABEL_CONTRACT and
            response.get('contract_version') == LABEL_VERSION and
            response.get('request_id') == request_id and
            response.get('request_sha256') == sha(raw), 'label_response_mismatch')
    require(response['status'] == 'ok', f'{operation}:{response.get("error")}')
    return response['result']


def run(args):
    kind = 'label' if args.operation == 'label' else 'document'
    with local_host(kind) as socket_path:
        if args.operation == 'page':
            pair = OCR if args.page == 1 else NATIVE
            value = manifest(socket_path, pair)
            page = next((p for p in value['pages'] if p['page_number'] == args.page), None)
            require(page is not None, 'page_unavailable')
            modality = 'ocr_text' if args.page == 1 else 'native_text'
            layer = page[modality]
            require(layer['status'] == 'extracted', 'page_text_unavailable')
            result = {'page_number': args.page, 'modality': modality,
                      'status': layer['status'], 'lines': layer['lines'],
                      'derivation_id': pair[0], 'manifest_sha256': pair[1]}
        elif args.operation == 'search':
            value = manifest(socket_path, NATIVE)
            require(len(value['pages']) == 188, 'native_coverage_changed')
            result = document_call(socket_path, 'search_document',
                                   derivation_id=NATIVE[0], manifest_sha256=NATIVE[1],
                                   term=args.term, limit=args.limit)
            require(all(candidate['parent'] == document.SOURCE and
                        candidate['manifest_sha256'] == NATIVE[1]
                        for candidate in result['candidates']), 'candidate_lineage_changed')
        elif args.operation == 'item':
            pair = OCR if args.page == 1 else NATIVE
            value = manifest(socket_path, pair)
            result = document_call(socket_path, 'fetch_evidence',
                                   derivation_id=pair[0], manifest_sha256=pair[1],
                                   item_id=args.item_id)
            page = next((p for p in value['pages'] if p['page_number'] == args.page), None)
            require(page is not None, 'item_page_unavailable')
            modality = 'ocr_text' if args.page == 1 else 'native_text'
            require(result['page_number'] == args.page and
                    result['parent'] == document.SOURCE and
                    result['item']['item_id'] == args.item_id and
                    result['modality'] == modality and
                    result['item'] in page[modality]['lines'],
                    'item_page_mismatch')
        else:
            offer = label_call(socket_path, 'describe_graph_labels')
            require(offer['manifest_sha256'] == LABEL_MANIFEST_SHA and
                    offer['derivation_id'] == LABEL_DERIVATION and
                    offer['source'] == document.SOURCE, 'label_offer_changed')
            page = label_call(socket_path, 'get_graph_labels_page',
                              derivation_id=offer['derivation_id'],
                              manifest_sha256=LABEL_MANIFEST_SHA,
                              page_number=args.page)
            require(page['source'] == document.SOURCE and
                    page['page']['page_number'] == args.page and
                    page['manifest_sha256'] == LABEL_MANIFEST_SHA and
                    page['derivation_id'] == LABEL_DERIVATION,
                    'label_page_mismatch')
            labels = page['page']['labels']
            if args.node:
                labels = [item for item in labels if item['node_id'] == args.node]
                require(len(labels) == 1, 'node_unavailable')
                recovered = label_call(socket_path, 'fetch_graph_label_item',
                                       derivation_id=offer['derivation_id'],
                                       manifest_sha256=LABEL_MANIFEST_SHA,
                                       item_id=labels[0]['item_id'])
                require(recovered['item'] == labels[0] and
                        recovered['page_number'] == args.page and
                        recovered['render_sha256'] == page['page']['render_sha256'] and
                        recovered['manifest_sha256'] == LABEL_MANIFEST_SHA and
                        recovered['derivation_id'] == LABEL_DERIVATION,
                        'label_item_mismatch')
            result = {'page_number': args.page, 'labels': labels,
                      'derivation_id': offer['derivation_id'],
                      'manifest_sha256': LABEL_MANIFEST_SHA,
                      'render_sha256': page['page']['render_sha256']}
    return {'status': 'ok', 'source': document.SOURCE, 'source_url': SOURCE_URL,
            'citation_rule': 'verify_page_and_fragment_visually_before_new_quote',
            'content_currentness': 'not_established', 'operation': args.operation,
            'result': result, 'runtime': 'stopped'}


def main():
    signal.signal(signal.SIGTERM, lambda _number, _frame: sys.exit(143))
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    page = commands.add_parser('page')
    page.add_argument('page', type=int, choices=range(1, 189), metavar='1..188')
    search = commands.add_parser('search')
    search.add_argument('term')
    search.add_argument('--limit', type=int, choices=range(1, 21), default=5,
                        metavar='1..20')
    item = commands.add_parser('item')
    item.add_argument('page', type=int, choices=range(1, 189), metavar='1..188')
    item.add_argument('item_id')
    label = commands.add_parser('label')
    label.add_argument('page', type=int, choices=range(18, 23), metavar='18..22')
    label.add_argument('--node')
    args = parser.parse_args()
    try:
        print(json.dumps(run(args), ensure_ascii=False, sort_keys=True))
    except (RuntimeError, ValueError, OSError, KeyError, TypeError,
            subprocess.CalledProcessError, KeyboardInterrupt, SystemExit) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False),
              file=sys.stderr)
        return (error.code if isinstance(error, SystemExit) and
                isinstance(error.code, int) else
                130 if isinstance(error, KeyboardInterrupt) else 1)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
