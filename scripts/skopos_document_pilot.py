"""Independent consumer check of the on-demand Skopos PDF derivative host."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = 'expertogobernanza/skopos-document-derivatives'
VERSION = 'v0.1'
SCHEMA = 'skopos/pdf-document-host/v0.1'
SOURCE_SHA = '719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323'
PROVENANCE_SHA = 'f934b0ec1bfbe97aae347b86bb3aa4e0831af79f704e571c27702f9203b62bff'
CUSTODY_POLICY_SHA = 'a92b9252cc27a5a0a421fa1422b583d61cafdb0026956794a302c09db3c52160'
RECEIPT = 'expertogobernanza:imss-2000-002-001:1:4fbed2bd3d2633aa'
SOURCE = {'material_id': 'imss-2000-002-001', 'source_revision': 1,
          'source_sha256': SOURCE_SHA, 'custody_receipt_id': RECEIPT,
          'custody_policy_sha256': CUSTODY_POLICY_SHA}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':')).encode('utf-8')


def write_new(path, raw):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'wb') as target:
        target.write(raw)
        target.flush()
        os.fsync(target.fileno())


def request(operation, request_id, **fields):
    return {'contract_id': CONTRACT, 'contract_version': VERSION,
            'request_id': request_id, 'operation': operation,
            'project_id': 'expertogobernanza', **fields}


def exchange(socket_path, requests_root, payload):
    raw = canonical(payload)
    nonce = secrets.token_hex(12)
    request_ref = nonce + '.request.json'
    envelope_ref = nonce + '.envelope.json'
    envelope = {'request_file_ref': request_ref, 'request_sha256': digest(raw),
                'request_id': payload['request_id'], 'contract_id': CONTRACT,
                'contract_version': VERSION}
    write_new(requests_root / request_ref, raw)
    write_new(requests_root / envelope_ref, canonical(envelope))
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(130 if payload['operation'] == 'derive_document'
                              else 10)
        connection.connect(str(socket_path))
        connection.sendall(canonical({'envelope_ref': envelope_ref}) + b'\n')
        response_raw = connection.makefile('rb').readline(65537)
    require(0 < len(response_raw) <= 65536, 'response_size')
    response = json.loads(response_raw)
    require(response.get('schema') == SCHEMA, 'response_schema')
    require(response.get('contract_id') == CONTRACT, 'response_contract')
    require(response.get('contract_version') == VERSION, 'response_version')
    require(response.get('request_id') == payload['request_id'],
            'response_request_id')
    require(response.get('request_sha256') == digest(raw), 'response_digest')
    return response, digest(raw)


def checked_exchange(args, payload):
    response, sha = exchange(args.socket, args.requests_root, payload)
    require(response['status'] == 'ok',
            f"{payload['operation']}:{response.get('error')}")
    return response['result'], sha


def fetch(args, derivation_id, manifest_sha, artifact_id, artifact_sha):
    output_ref = 'eg-document-' + secrets.token_hex(12) + '.bin'
    result, _ = checked_exchange(args, request(
        'fetch_derivative', 'eg-fetch-' + secrets.token_hex(10), source=SOURCE,
        derivation_id=derivation_id, manifest_sha256=manifest_sha,
        artifact_id=artifact_id, artifact_sha256=artifact_sha,
        output_ref=output_ref))
    output = args.delivery_root / output_ref
    raw = output.read_bytes()
    require(result['bytes_ref'] == output_ref, 'output_reference')
    require(result['byte_length'] == len(raw), 'output_length')
    require(result['sha256'] == artifact_sha == digest(raw), 'output_hash')
    output.unlink()
    return raw


def check_bbox(box):
    require(isinstance(box, list) and len(box) == 4 and
            all(isinstance(n, (int, float)) and 0 <= n <= 1 for n in box) and
            box[0] <= box[2] and box[1] <= box[3], 'invalid_bbox')


def check_manifest(manifest, derivation_id, policy_sha, pages, ocr_pages):
    require(manifest['schema'] == 'skopos/pdf-document-manifest/v0.1',
            'manifest_schema')
    require(manifest['derivation_id'] == derivation_id, 'manifest_identity')
    require(manifest['parent'] == SOURCE, 'manifest_parent')
    require(manifest['policy_sha256'] == policy_sha, 'manifest_policy')
    require(manifest['page_count'] == 188, 'physical_page_count')
    require([p['page_number'] for p in manifest['pages']] == pages,
            'page_coverage')
    require(manifest['fidelity_status'] == 'unreviewed', 'fidelity_claim')
    items = []
    for page in manifest['pages']:
        for modality in ('native_text', 'ocr_text'):
            layer = page[modality]
            require(layer['status'] in ('extracted', 'no_text', 'not_run', 'partial'),
                    'layer_status')
            if modality == 'ocr_text' and page['page_number'] not in ocr_pages:
                require(layer['status'] == 'not_run', 'unexpected_ocr')
            for index, line in enumerate(layer['lines']):
                require(isinstance(line['text'], str), 'line_text')
                require(isinstance(line.get('item_id'), str) and
                        len(line['item_id']) == 64 and
                        all(c in '0123456789abcdef' for c in line['item_id']),
                        'item_id')
                check_bbox(line['bbox'])
                expected_item_id = digest(canonical({
                    'derivation_id': derivation_id,
                    'page_number': page['page_number'],
                    'modality': 'selective_ocr' if modality == 'ocr_text'
                                else 'native_text',
                    'index': index, 'text': line['text'], 'bbox': line['bbox']}))
                require(line['item_id'] == expected_item_id,
                        'item_identity_mismatch')
                items.append((page['page_number'], modality, line))
    return items


def run(args):
    require(digest((ROOT / 'docs/fuentes/imss/2000-002-001.pdf').read_bytes()) ==
            SOURCE_SHA, 'local_source_hash')
    require(digest((ROOT / 'docs/fuentes/imss/2000-002-001-PROCEDENCIA.md').read_bytes()) ==
            PROVENANCE_SHA, 'local_provenance_hash')
    require(args.requests_root.is_dir() and args.delivery_root.is_dir(),
            'host_roots_missing')
    offer, _ = checked_exchange(args, request(
        'describe_document_capabilities', 'eg-doc-cap-' + secrets.token_hex(10)))
    policy = offer['policy']
    require(policy['id'] == args.policy_id and
            policy['version'] == args.policy_version and
            policy['policy_sha256'] == args.policy_sha256,
            'derivative_policy_identity')
    require(offer['capabilities']['native_text'] in ('partial', 'available'),
            'native_unavailable')
    require(offer['capabilities']['selective_ocr'] in ('partial', 'available'),
            'ocr_unavailable')
    if args.mode == 'graph':
        require(offer['capabilities']['visual_graph'] == 'partial',
                'graph_capability_mismatch')
    pages = ([1, 18, 19, 20, 21, 22] if args.mode == 'ocr' else
             [18, 19, 20, 21, 22] if args.mode == 'graph' else
             list(range(1, 189)))
    ocr_pages = pages if args.mode == 'ocr' else pages if args.mode == 'graph' else []
    graph_pages = pages if args.mode == 'graph' else []
    modalities = (['native_text', 'selective_ocr', 'visual_graph']
                  if graph_pages else
                  ['native_text', 'selective_ocr'] if ocr_pages else
                  ['native_text'])
    derive_request = request(
        'derive_document', 'eg-doc-' + args.mode + '-' + secrets.token_hex(10),
        source=SOURCE, pages=pages, modalities=modalities,
        ocr_pages=ocr_pages, graph_pages=graph_pages,
        limits={'max_pages': len(pages), 'max_render_pixels': 4452000,
                'max_seconds': 120, 'max_output_bytes': 10000000,
                'allow_network': False})
    receipt, request_sha = checked_exchange(args, derive_request)
    require(receipt['derivation_status'] in ('created', 'duplicate'),
            'derivation_status')
    manifest_sha = receipt['manifest_sha256']
    derivation_id = receipt['derivation_id']
    manifest_raw = fetch(args, derivation_id, manifest_sha, 'manifest', manifest_sha)
    manifest = json.loads(manifest_raw)
    items = check_manifest(manifest, derivation_id, policy['policy_sha256'],
                           pages, ocr_pages)
    if args.mode == 'native':
        require(sum(p['native_text']['status'] == 'extracted'
                    for p in manifest['pages']) == 187,
                'native_coverage_mismatch')
        require(manifest['pages'][0]['native_text']['status'] == 'no_text',
                'cover_native_status')
    recovered, _ = checked_exchange(args, request(
        'derivation_receipt', 'eg-receipt-' + secrets.token_hex(10),
        source=SOURCE, derivation_request_id=derive_request['request_id'],
        derivation_request_sha256=request_sha))
    require(recovered['manifest_sha256'] == manifest_sha and
            recovered['derivation_id'] == derivation_id, 'receipt_recovery')
    if args.mode == 'ocr':
        require(manifest['pages'][0]['native_text']['status'] == 'no_text',
                'cover_native_status')
        require(manifest['pages'][0]['ocr_text']['status'] == 'extracted',
                'cover_ocr_status')
        require(len(manifest['pages'][0]['ocr_text']['lines']) > 0,
                'cover_ocr_empty')
        cover = ' '.join(line['text'] for line in
                         manifest['pages'][0]['ocr_text']['lines'])
        require('MANUAL DE ORGANIZACIÓN' in cover and
                'DIRECCIÓN DE PRESTACIONES MÉDICAS' in cover,
                'cover_ocr_positive_control')
    if args.mode in ('ocr', 'graph'):
        require(all(p['ocr_text']['status'] == 'extracted' and
                    p['ocr_text']['lines'] and p['render'] is not None
                    for p in manifest['pages']), 'ocr_page_coverage')
        render = manifest['artifacts']['20']
        render_raw = fetch(args, derivation_id, manifest_sha,
                           render['artifact_id'], render['sha256'])
        require(render_raw.startswith(b'\x89PNG\r\n\x1a\n') and
                len(render_raw) == render['byte_length'] and
                next(p for p in manifest['pages'] if p['page_number'] == 20)
                ['render']['sha256'] == digest(render_raw),
                'render_mismatch')
    if args.mode == 'graph':
        require(all(p['visual_graph']['status'] == 'partial' and
                    p['visual_graph']['nodes'] and p['visual_graph']['edges']
                    for p in manifest['pages']), 'graph_status')
        page20 = next(p for p in manifest['pages'] if p['page_number'] == 20)
        graph = page20['visual_graph']
        require(graph['status'] == 'partial' and len(graph['nodes']) == 10 and
                len(graph['edges']) == 9, 'page20_topology')
        require({(e['from_node'], e['to_node']) for e in graph['edges']} == {
            ('n1', 'n2'), ('n2', 'n3'), ('n2', 'n4'),
            ('n3', 'n5'), ('n3', 'n7'), ('n3', 'n9'),
            ('n4', 'n6'), ('n4', 'n8'), ('n4', 'n10')},
                'page20_branch_mismatch')
        require(all(edge['direction'] == 'unknown' and
                    edge['status'] == 'topology_hypothesis'
                    for edge in graph['edges']), 'unobserved_direction_claimed')
        node_ids = {node['node_id'] for node in graph['nodes']}
        require(all(edge['from_node'] in node_ids and edge['to_node'] in node_ids
                    for edge in graph['edges']), 'graph_dangling_node')
        connector_ids = {c['connector_id'] for c in graph['connectors']}
        require(all(e['connector_id'] in connector_ids for e in graph['edges']) and
                all(port['node_id'] in node_ids for c in graph['connectors']
                    for port in c['ports']), 'graph_dangling_connector')
        root, unit = graph['nodes'][:2]
        require('DIRECCIÓN' in root['label'] and 'MÉDICAS' in root['label'] and
                'UNIDAD DE EDUCACIÓN E INVESTIGACIÓN' in unit['label'],
                'page20_material_labels')
        require(0.50 < root['bbox'][0] < 0.53 and
                0.26 < root['bbox'][1] < 0.28 and
                0.50 < unit['bbox'][0] < 0.53 and
                0.33 < unit['bbox'][1] < 0.35,
                'page20_material_regions')
        node = graph['nodes'][0]
        check_bbox(node['bbox'])
        expected_node_id = digest(canonical({
            'derivation_id': derivation_id, 'page_number': 20,
            'modality': 'visual_graph_node', 'node_id': node['node_id'],
            'bbox': node['bbox'], 'label': node['label']}))
        require(node['item_id'] == expected_node_id, 'graph_item_identity')
        node_evidence, _ = checked_exchange(args, request(
            'fetch_evidence', 'eg-node-' + secrets.token_hex(10),
            source=SOURCE, derivation_id=derivation_id,
            manifest_sha256=manifest_sha, item_id=node['item_id']))
        require(node_evidence['item'] == node and
                node_evidence['modality'] == 'visual_graph_node' and
                node_evidence['page_number'] == 20 and
                node_evidence['render_sha256'] == page20['render']['sha256'] and
                node_evidence['parent'] == SOURCE and
                node_evidence['fidelity_status'] == 'unreviewed',
                'graph_evidence_mismatch')
    sample = next((entry for entry in items if entry[2]['text'].strip()), None)
    require(sample is not None, 'no_evidence_sample')
    page, modality, item = sample
    evidence, _ = checked_exchange(args, request(
        'fetch_evidence', 'eg-evidence-' + secrets.token_hex(10),
        source=SOURCE, derivation_id=derivation_id,
        manifest_sha256=manifest_sha, item_id=item['item_id']))
    require(evidence['item'] == item and evidence['page_number'] == page and
            evidence['modality'] == modality and evidence['parent'] == SOURCE,
            'evidence_mismatch')
    matches, _ = checked_exchange(args, request(
        'search_document', 'eg-match-' + secrets.token_hex(10),
        source=SOURCE, derivation_id=derivation_id,
        manifest_sha256=manifest_sha, term='MANUAL DE ORGANIZACIÓN', limit=5))
    require(matches['match_status'] == 'matched' and matches['candidates'] and
            matches['search_method'] == 'literal_scan_v0.1',
            'positive_search_failed')
    require(matches['coverage']['modalities_scanned'] ==
            ['native_text', 'ocr_text'] and
            'semantic_matches' in matches['coverage']['exclusions'] and
            matches['coverage']['page_statuses'] == [
                {'page_number': p['page_number'],
                 'native_text': p['native_text']['status'],
                 'ocr_text': p['ocr_text']['status']}
                for p in manifest['pages']],
            'search_coverage_mismatch')
    candidate = matches['candidates'][0]
    require(candidate['parent'] == SOURCE and
            candidate['derivation_id'] == derivation_id and
            candidate['manifest_sha256'] == manifest_sha and
            candidate['search_method'] == 'literal_scan_v0.1' and
            candidate['fidelity_status'] == 'unreviewed',
            'candidate_provenance_mismatch')
    source_page = next(p for p in manifest['pages']
                       if p['page_number'] == candidate['page_number'])
    source_layer = source_page[candidate['modality']]
    source_item = next((line for line in source_layer['lines']
                        if line['item_id'] == candidate['item_id']), None)
    require(source_item is not None and
            candidate['text'] == source_item['text'] and
            candidate['bbox'] == source_item['bbox'],
            'candidate_manifest_mismatch')
    cited, _ = checked_exchange(args, request(
        'fetch_evidence', 'eg-cited-' + secrets.token_hex(10),
        source=SOURCE, derivation_id=derivation_id,
        manifest_sha256=manifest_sha, item_id=candidate['item_id']))
    require(cited['item'] == source_item and
            cited['page_number'] == candidate['page_number'] and
            cited['modality'] == candidate['modality'] and
            cited['parent'] == SOURCE and
            cited['fidelity_status'] == 'unreviewed' and
            cited['render_sha256'] == (source_page['render'] or {}).get('sha256'),
            'candidate_evidence_mismatch')
    no_match, _ = checked_exchange(args, request(
        'search_document', 'eg-no-match-' + secrets.token_hex(10),
        source=SOURCE, derivation_id=derivation_id,
        manifest_sha256=manifest_sha, term='ZZZ-absent-91827643', limit=5))
    require(no_match['match_status'] == 'no_match' and not no_match['candidates'],
            'false_candidate')
    bad, _ = exchange(args.socket, args.requests_root, request(
        'fetch_derivative', 'eg-bad-hash-' + secrets.token_hex(10),
        source=SOURCE, derivation_id=derivation_id,
        manifest_sha256='0' * 64, artifact_id='manifest',
        artifact_sha256=manifest_sha, output_ref='bad-' + secrets.token_hex(10)))
    require(bad['status'] != 'ok' and bad['error']['code'] ==
            'manifest_integrity_failed', 'bad_manifest_accepted')
    print(json.dumps({'status': 'consumer_smoke_passed', 'mode': args.mode,
                      'derivation_id': derivation_id, 'manifest_sha256': manifest_sha,
                      'pages': len(pages), 'ocr_pages': len(ocr_pages),
                      'graph_pages': len(graph_pages),
                      'evidence_sample_page': page, 'evidence_modality': modality,
                      'fidelity_status': 'unreviewed'}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', type=Path, required=True)
    parser.add_argument('--requests-root', type=Path, required=True)
    parser.add_argument('--delivery-root', type=Path, required=True)
    parser.add_argument('--policy-id', required=True)
    parser.add_argument('--policy-version', required=True)
    parser.add_argument('--policy-sha256', required=True)
    parser.add_argument('--mode', choices=('native', 'ocr', 'graph'), required=True)
    run(parser.parse_args())


if __name__ == '__main__':
    main()
