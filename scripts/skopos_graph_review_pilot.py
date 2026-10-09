"""Independent on-demand consumer check for Skopos graph review v0.3."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket

from scripts import skopos_document_pilot as document


CONTRACT = 'expertogobernanza/skopos-graph-review'
VERSION = 'v0.3-experimental'
SCHEMA = 'skopos/pdf-graph-review-host/v0.3-experimental'
CONFIG_SHA = '8ee6ec7b550dfcee2eb244425d39f8af8a15301fc89a074214eebfb695c02515'
MANIFEST_SHA = '5b6db3341f0f6058356de157ea5bab74bbffeceb9d38cfb0892869f25d076884'
DERIVATION = '3cd64933f11b0e64733565b4c7acf99423bca129fc7ee5526daf35962cd8504c'
PARENT_SHA = '8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee'
COUNTS = [(18, 8, 7), (19, 32, 31), (20, 10, 9),
          (21, 19, 18), (22, 17, 16)]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(',', ':')).encode('utf-8')


def load_pins(args):
    config_raw = args.config.read_bytes()
    require(sha(canonical(json.loads(config_raw))) == CONFIG_SHA,
            'config_changed')
    config = json.loads(config_raw)
    require(Path(config['socket_path']) == args.socket and
            config['manifest_sha256'] == MANIFEST_SHA and
            Path(config['manifest_path']) == args.manifest,
            'config_paths')
    raw = args.manifest.read_bytes()
    require(sha(raw) == MANIFEST_SHA, 'manifest_changed')
    manifest = json.loads(raw)
    require(manifest['schema'] == 'skopos/pdf-graph-review/v0.3-experimental' and
            manifest['derivation_id'] == DERIVATION and
            manifest['parent_manifest_sha256'] == PARENT_SHA and
            manifest['source'] == document.SOURCE and
            manifest['fidelity_status'] == 'unreviewed_partial',
            'manifest_identity')
    require([(p['page_number'], len(p['nodes']), len(p['edges']))
             for p in manifest['pages']] == COUNTS and
            sum(p['coverage']['added_visual_candidates']
                for p in manifest['pages']) == 36 and
            all(p['coverage']['graph_status'] == 'partial'
                for p in manifest['pages']), 'graph_coverage')
    nodes = [node for page in manifest['pages'] for node in page['nodes']]
    edges = [edge for page in manifest['pages'] for edge in page['edges']]
    require(sum(node['review_status'] == 'nonblind_visual_candidate' and
                bool(node['visual_label_candidate']) for node in nodes) == 5 and
            all((node['review_status'] == 'nonblind_visual_candidate') ==
                bool(node['visual_label_candidate']) for node in nodes) and
            all(edge['status'] == 'visual_candidate_unadjudicated' and
                edge['direction'] == 'layout_parent_to_child_candidate' and
                edge['origin'] in ('v0.1_topology_hypothesis',
                                   'nonblind_visual_review')
                for edge in edges) and
            sum(edge['origin'] == 'nonblind_visual_review'
                for edge in edges) == 36, 'candidate_statuses')
    return manifest


def exchange(args, operation, **fields):
    request_id = 'eg-graph-' + secrets.token_hex(12)
    request = {'contract_id': CONTRACT, 'contract_version': VERSION,
               'request_id': request_id, 'project_id': 'expertogobernanza',
               'operation': operation, 'source': document.SOURCE,
               'graph_config_sha256': CONFIG_SHA, **fields}
    raw = canonical(request)
    nonce = secrets.token_hex(12)
    request_ref = nonce + '.request.json'
    envelope_ref = nonce + '.envelope.json'
    envelope = {'request_file_ref': request_ref, 'request_sha256': sha(raw),
                'request_id': request_id, 'contract_id': CONTRACT,
                'contract_version': VERSION}
    for name, payload in ((request_ref, raw),
                          (envelope_ref, canonical(envelope))):
        descriptor = os.open(args.requests_root / name,
                             os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600)
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(10)
        connection.connect(str(args.socket))
        connection.sendall(canonical({'envelope_ref': envelope_ref}) + b'\n')
        response_raw = connection.makefile('rb').readline(65537)
    require(0 < len(response_raw) <= 65536, 'response_length')
    response = json.loads(response_raw)
    require(response.get('schema') == SCHEMA and
            response.get('contract_id') == CONTRACT and
            response.get('contract_version') == VERSION and
            response.get('request_id') == request_id and
            response.get('request_sha256') == sha(raw),
            'response_correlation')
    return response


def accepted(args, operation, **fields):
    response = exchange(args, operation, **fields)
    require(response['status'] == 'ok', f'{operation}:{response["error"]}')
    return response['result']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('config', 'manifest', 'socket', 'requests_root'):
        parser.add_argument('--' + name.replace('_', '-'), type=Path,
                            required=True)
    args = parser.parse_args()
    manifest = load_pins(args)
    offer = accepted(args, 'describe_graph_review')
    require(offer['derivation_id'] == DERIVATION and
            offer['manifest_sha256'] == MANIFEST_SHA and
            offer['source'] == document.SOURCE and
            offer['fidelity_status'] == 'unreviewed_partial', 'offer_identity')
    for page in manifest['pages']:
        response = accepted(args, 'get_graph_review_page',
                            derivation_id=DERIVATION,
                            manifest_sha256=MANIFEST_SHA,
                            page_number=page['page_number'])
        require(response['page'] == page and
                response['fidelity_status'] == 'unreviewed_partial' and
                response['source'] == document.SOURCE and
                response['derivation_id'] == DERIVATION and
                response['manifest_sha256'] == MANIFEST_SHA, 'page_mismatch')
    p22 = manifest['pages'][-1]
    node = next(n for n in p22['nodes'] if n['node_id'] == 'n10')
    edge = next(e for e in p22['edges'] if
                (e['parent_node_id'], e['child_node_id']) == ('n3', 'n8'))
    for item, modality in ((node, 'visual_graph_node'),
                           (edge, 'visual_graph_edge')):
        response = accepted(args, 'fetch_graph_review_item',
                            derivation_id=DERIVATION,
                            manifest_sha256=MANIFEST_SHA,
                            item_id=item['item_id'])
        require(response['item'] == item and response['modality'] == modality and
                response['page_number'] == 22 and
                response['source'] == document.SOURCE and
                response['derivation_id'] == DERIVATION and
                response['manifest_sha256'] == MANIFEST_SHA and
                response['render_sha256'] == p22['render_sha256'] and
                response['fidelity_status'] == 'unreviewed_partial',
                'item_mismatch')
    require(node['visual_label_candidate'] ==
            'COORDINACIÓN TÉCNICA DE INFRAESTRUCTURA MÉDICA' and
            edge['status'] == 'visual_candidate_unadjudicated' and
            edge['origin'] == 'nonblind_visual_review', 'promotion_claim')
    negatives = (
        ('wrong_source', 'fetch_graph_review_item',
         {'source': dict(document.SOURCE, source_sha256='0' * 64),
          'derivation_id': DERIVATION, 'manifest_sha256': MANIFEST_SHA,
          'item_id': edge['item_id']}, 'source_mismatch'),
        ('wrong_manifest', 'get_graph_review_page',
         {'derivation_id': DERIVATION, 'manifest_sha256': '0' * 64,
          'page_number': 22}, 'graph_identity_mismatch'),
        ('outside_pages', 'get_graph_review_page',
         {'derivation_id': DERIVATION, 'manifest_sha256': MANIFEST_SHA,
          'page_number': 23}, 'page_out_of_scope'),
        ('unknown_item', 'fetch_graph_review_item',
         {'derivation_id': DERIVATION, 'manifest_sha256': MANIFEST_SHA,
          'item_id': '0' * 64}, 'evidence_unavailable'),
    )
    for name, operation, fields, code in negatives:
        bad = exchange(args, operation, **fields)
        require(bad['status'] != 'ok' and bad['result'] is None and
                bad['error']['code'] == code, f'{name}_accepted')
    print(json.dumps({'status': 'consumer_graph_review_passed',
                      'derivation_id': DERIVATION, 'manifest_sha256': MANIFEST_SHA,
                      'pages': [row[0] for row in COUNTS],
                      'nodes': sum(row[1] for row in COUNTS),
                      'edge_candidates': sum(row[2] for row in COUNTS),
                      'added_candidates': 36,
                      'negative_controls': [row[0] for row in negatives],
                      'fidelity_status': 'unreviewed_partial'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
