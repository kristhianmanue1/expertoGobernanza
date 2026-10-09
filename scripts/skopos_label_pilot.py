"""Check Skopos label candidates against the pinned IMSS graph manifest."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = 'expertogobernanza/skopos-label-candidates'
VERSION = 'v0.2-experimental'
SCHEMA = 'skopos/pdf-label-host/v0.2-experimental'
SOURCE_SHA = '719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323'
POLICY_SHA = '21540db84c1b6b10cdbd433392caa6ed66b26d9820814c227d2d08dec948be1d'
DOCUMENT_POLICY_SHA = '4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b'
MANIFEST_SHA = '8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee'
DERIVATION = '1ef12d5a480075214369e9d19dcb6949370119e212b84007ce1b1a5ef1b7b8cf'
SOURCE = {
    'material_id': 'imss-2000-002-001',
    'source_revision': 1,
    'source_sha256': SOURCE_SHA,
    'custody_receipt_id': 'expertogobernanza:imss-2000-002-001:1:4fbed2bd3d2633aa',
    'custody_policy_sha256': 'a92b9252cc27a5a0a421fa1422b583d61cafdb0026956794a302c09db3c52160',
}
PAGES = {18: (8, 7), 19: (32, 19), 20: (10, 9), 21: (19, 5), 22: (17, 5)}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':')).encode('utf-8')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def write_new(path, raw):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'wb') as target:
        target.write(raw)
        target.flush()
        os.fsync(target.fileno())


def make_request(operation, **fields):
    return {'request_id': 'eg-label-consumer-' + secrets.token_hex(10),
            'contract_id': CONTRACT, 'contract_version': VERSION,
            'project_id': 'expertogobernanza', 'operation': operation,
            'source': SOURCE, 'label_policy_sha256': POLICY_SHA, **fields}


def send(socket_path, envelope_ref):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(10)
        connection.connect(str(socket_path))
        connection.sendall(canonical({'envelope_ref': envelope_ref}) + b'\n')
        raw = connection.makefile('rb').readline(65537)
    require(0 < len(raw) <= 65536, 'response_size')
    return json.loads(raw)


def exchange(args, request):
    raw = canonical(request)
    nonce = secrets.token_hex(12)
    request_ref = nonce + '.request.json'
    envelope_ref = nonce + '.envelope.json'
    envelope = {'request_file_ref': request_ref, 'request_sha256': digest(raw),
                'request_id': request['request_id'], 'contract_id': CONTRACT,
                'contract_version': VERSION}
    write_new(args.requests_root / request_ref, raw)
    write_new(args.requests_root / envelope_ref, canonical(envelope))
    response = send(args.socket, envelope_ref)
    require(response.get('schema') == SCHEMA, 'response_schema')
    require(response.get('contract_id') == CONTRACT and
            response.get('contract_version') == VERSION, 'response_contract')
    require(response.get('request_id') == request['request_id'] and
            response.get('request_sha256') == digest(raw), 'response_correlation')
    return response, envelope_ref


def check_page(result, manifest_page, derived_root):
    number = manifest_page['page_number']
    require(result['derivation_id'] == DERIVATION and
            result['manifest_sha256'] == MANIFEST_SHA and
            result['label_policy_sha256'] == POLICY_SHA and
            result['source_sha256'] == SOURCE_SHA and
            result['page_number'] == number and
            result['fidelity_status'] == 'unreviewed', 'page_identity')
    render = manifest_page['render']
    require(result['render_sha256'] == render['sha256'], 'render_identity')
    render_path = (derived_root / render['file_ref']).resolve()
    require(render_path.is_relative_to(derived_root.resolve()), 'render_path')
    require(digest(render_path.read_bytes()) == render['sha256'], 'render_bytes')
    graph = manifest_page['visual_graph']
    coverage = result['coverage']
    require(coverage['graph_status'] == 'partial' and
            coverage['topology_completeness'] == 'unreviewed_partial' and
            (len(result['nodes']), len(result['edges'])) == PAGES[number] and
            coverage['node_count'] == len(result['nodes']) and
            coverage['edge_count'] == len(result['edges']) and
            coverage['native_text_status'] == manifest_page['native_text']['status'] and
            coverage['ocr_text_status'] == manifest_page['ocr_text']['status'] and
            coverage['connector_count'] == len(graph['connectors']) and
            coverage['unresolved_connector_count'] == len(graph['unknown']) and
            result['edges'] == graph['edges'] and
            result['unresolved_connectors'] == graph['unknown'], 'graph_coverage')
    expected_nodes = {node['node_id']: node for node in graph['nodes']}
    require({node['node_id'] for node in result['nodes']} == set(expected_nodes),
            'node_inventory')
    for node in result['nodes']:
        parent = expected_nodes[node['node_id']]
        require(node['parent_item_id'] == parent['item_id'] and
                node['bbox'] == parent['bbox'], 'node_identity')
        candidates = node['label_candidates']
        require([item['method'] for item in candidates] ==
                ['native_text', 'selective_ocr'], 'candidate_methods')
        for candidate in candidates:
            layer = ('native_text' if candidate['method'] == 'native_text'
                     else 'ocr_text')
            lines = {line['item_id']: line for line in manifest_page[layer]['lines']}
            ids = candidate['line_item_ids']
            expected = [line for line in lines.values()
                        if node['bbox'][0] <=
                        (line['bbox'][0] + line['bbox'][2]) / 2 <= node['bbox'][2]
                        and node['bbox'][1] <=
                        (line['bbox'][1] + line['bbox'][3]) / 2 <= node['bbox'][3]]
            expected.sort(key=lambda line: (line['bbox'][1], line['bbox'][0],
                                            line['item_id']))
            require(ids == [line['item_id'] for line in expected],
                    'line_inventory')
            require(candidate['line_bboxes'] == [lines[item]['bbox'] for item in ids]
                    and candidate['text'] == ' '.join(lines[item]['text'] for item in ids)
                    and candidate['status'] == ('unreviewed' if ids else 'no_lines'),
                    'line_content')
    require(coverage['missing_native_labels'] == sum(
        not node['label_candidates'][0]['text'] for node in result['nodes']) and
        coverage['missing_ocr_labels'] == sum(
            not node['label_candidates'][1]['text'] for node in result['nodes']),
        'missing_label_counts')
    return {'nodes': len(result['nodes']), 'edges': len(result['edges']),
            'unresolved_connectors': coverage['unresolved_connector_count'],
            'missing_native': coverage['missing_native_labels'],
            'missing_ocr': coverage['missing_ocr_labels'],
            'graph_status': coverage['graph_status']}


def run(args):
    require(digest((ROOT / 'docs/fuentes/imss/2000-002-001.pdf').read_bytes()) ==
            SOURCE_SHA, 'original_pdf_changed')
    raw = args.manifest.read_bytes()
    require(digest(raw) == MANIFEST_SHA, 'manifest_changed')
    manifest = json.loads(raw)
    require(manifest['derivation_id'] == DERIVATION and
            manifest['parent'] == SOURCE and
            manifest['fidelity_status'] == 'unreviewed', 'manifest_identity')
    require(args.requests_root.is_dir(), 'requests_root_missing')
    offer, _ = exchange(args, make_request('describe_label_capabilities'))
    require(offer['status'] == 'ok', 'describe_failed')
    advertised = offer['result']
    require(advertised['allowed_pages'] == list(PAGES) and
            advertised['label_policy_sha256'] == POLICY_SHA and
            advertised['document_policy_sha256'] == DOCUMENT_POLICY_SHA and
            advertised['max_pages_per_request'] == 1 and
            advertised['max_nodes_per_response'] == 40 and
            advertised['fidelity_status'] == 'unreviewed' and
            advertised['request_persistence'] == 'existing_requests_root' and
            advertised['response_persistence'] == 'none_by_label_host' and
            advertised['request_retention_action'] ==
            'block_then_explicit_retirement' and
            advertised['request_retention_until'] == '2026-11-08T00:00:00Z',
            'capability_mismatch')
    pages = {}
    for manifest_page in manifest['pages']:
        number = manifest_page['page_number']
        if number not in PAGES:
            continue
        response, _ = exchange(args, make_request(
            'get_label_candidates', derivation_id=DERIVATION,
            manifest_sha256=MANIFEST_SHA, page_number=number, max_nodes=40))
        require(response['status'] == 'ok', f'page_{number}_failed')
        pages[str(number)] = check_page(response['result'], manifest_page,
                                        args.derived_root)
    require(set(pages) == {str(number) for number in PAGES}, 'page_inventory')
    for name, changes, code in (
            ('outside', {'page_number': 23}, 'page_out_of_scope'),
            ('manifest', {'manifest_sha256': '0' * 64}, 'manifest_mismatch'),
            ('policy', {'label_policy_sha256': '0' * 64}, 'label_policy_mismatch')):
        request = make_request('get_label_candidates', derivation_id=DERIVATION,
                               manifest_sha256=MANIFEST_SHA, page_number=20,
                               max_nodes=40)
        request.update(changes)
        rejected, _ = exchange(args, request)
        require(rejected['status'] != 'ok' and
                rejected['result'] is None and
                rejected['error']['code'] == code, f'{name}_negative_failed')
    return {'status': 'consumer_label_smoke_passed', 'manifest_sha256': MANIFEST_SHA,
            'label_policy_sha256': POLICY_SHA, 'pages': pages,
            'request_persistence': advertised['request_persistence'],
            'response_persistence': advertised['response_persistence'],
            'fidelity_status': 'unreviewed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', type=Path, required=True)
    parser.add_argument('--requests-root', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--derived-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
