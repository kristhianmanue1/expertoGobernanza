"""Independent on-demand consumer check for Skopos graph labels v0.4."""

import argparse
import json
import os
from pathlib import Path
import secrets
import socket

from scripts import skopos_document_pilot as document
from scripts.skopos_graph_review_pilot import canonical, require, sha


CONTRACT = 'expertogobernanza/skopos-graph-labels'
VERSION = 'v0.4-experimental'
SCHEMA = 'skopos/pdf-graph-labels-host/v0.4-experimental'
CONFIG_SHA = '1b21129583a5de8aac2938b00e594df36654452afc6e3c348983387ddd03803b'
MANIFEST_SHA = '07018142b74249edf0bc056f3b10bee5d1d004e43e77f556b3ef745027efaa98'
DERIVATION = '54ef4a35842a22896b1f881eb9a1c4c6076ac80e469d83dcbafa81f32e6c7e45'
PARENT_SHA = '5b6db3341f0f6058356de157ea5bab74bbffeceb9d38cfb0892869f25d076884'
COUNTS = [(18, 8), (19, 32), (20, 10), (21, 19), (22, 17)]
P18_LABELS = {
    'n1': 'DIRECCIÓN DE PRESTACIONES MÉDICAS',
    'n2': 'UNIDAD DE PLANEACIÓN E INNOVACIÓN EN SALUD',
    'n3': 'UNIDAD DE ATENCIÓN MÉDICA',
    'n4': 'UNIDAD DE EDUCACIÓN E INVESTIGACIÓN',
    'n5': ('UNIDAD DE INFRAESTRUCTURA, SERVICIOS MÉDICOS INDIRECTOS '
           'E INTEGRACIÓN SECTORIAL'),
    'n6': 'COORDINACIÓN DE PROYECTOS ESPECIALES EN SALUD',
    'n7': 'COORDINACIÓN DE SERVICIOS ADMINISTRATIVOS',
    'n8': ('DIVISIÓN DE MEJORA DE GESTIÓN ADMINISTRATIVA '
           'Y NORMATIVIDAD MÉDICA'),
}


def load_pins(args):
    config_raw = args.config.read_bytes()
    config = json.loads(config_raw)
    require(sha(canonical(config)) == CONFIG_SHA and
            config['manifest_sha256'] == MANIFEST_SHA and
            Path(config['socket_path']) == args.socket,
            'config_changed')
    raw = args.manifest.read_bytes()
    require(sha(raw) == MANIFEST_SHA, 'manifest_changed')
    manifest = json.loads(raw)
    require(manifest['schema'] == 'skopos/pdf-graph-labels/v0.4-experimental' and
            manifest['derivation_id'] == DERIVATION and
            manifest['parent_manifest_sha256'] == PARENT_SHA and
            manifest['source'] == document.SOURCE and
            manifest['fidelity_status'] == 'unreviewed_partial',
            'manifest_identity')
    require([(p['page_number'], len(p['labels'])) for p in manifest['pages']]
            == COUNTS, 'label_coverage')
    labels = [label for page in manifest['pages'] for label in page['labels']]
    methods = [label['method'] for label in labels]
    require(methods.count('visual_nonblind') == 8 and
            methods.count('native_bbox_spacing_join') == 77 and
            methods.count('native_bbox_with_visual_override') == 1 and
            all(label['status'] == 'candidate_unadjudicated' and
                label['label_candidate'] and label['parent_item_id'] and
                label['render_sha256'] for label in labels),
            'candidate_statuses')
    require({label['node_id']: label['label_candidate']
             for label in manifest['pages'][0]['labels']} == P18_LABELS,
            'p18_visual_transcription')
    p21 = manifest['pages'][3]
    n5 = next(label for label in p21['labels'] if label['node_id'] == 'n5')
    require(n5['native_joined_label'].endswith('SALUID') and
            n5['label_candidate'].endswith('SALUD') and
            n5['method'] == 'native_bbox_with_visual_override',
            'p21_override')
    return manifest


def exchange(args, operation, **fields):
    request_id = 'eg-label-' + secrets.token_hex(12)
    request = {'contract_id': CONTRACT, 'contract_version': VERSION,
               'request_id': request_id, 'project_id': 'expertogobernanza',
               'operation': operation, 'source': document.SOURCE,
               'labels_config_sha256': CONFIG_SHA, **fields}
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
    offer = accepted(args, 'describe_graph_labels')
    require(offer['derivation_id'] == DERIVATION and
            offer['manifest_sha256'] == MANIFEST_SHA and
            offer['parent_manifest_sha256'] == PARENT_SHA and
            offer['source'] == document.SOURCE and
            offer['fidelity_status'] == 'unreviewed_partial', 'offer_identity')
    for page in manifest['pages']:
        result = accepted(args, 'get_graph_labels_page',
                          derivation_id=DERIVATION,
                          manifest_sha256=MANIFEST_SHA,
                          page_number=page['page_number'])
        require(result['page'] == page and result['source'] == document.SOURCE and
                result['manifest_sha256'] == MANIFEST_SHA and
                result['fidelity_status'] == 'unreviewed_partial',
                'page_mismatch')
    for number, node_id in ((18, 'n3'), (21, 'n5'), (22, 'n10')):
        page = next(p for p in manifest['pages'] if p['page_number'] == number)
        item = next(x for x in page['labels'] if x['node_id'] == node_id)
        result = accepted(args, 'fetch_graph_label_item',
                          derivation_id=DERIVATION,
                          manifest_sha256=MANIFEST_SHA,
                          item_id=item['item_id'])
        require(result['item'] == item and result['page_number'] == number and
                result['render_sha256'] == page['render_sha256'] and
                result['source'] == document.SOURCE and
                result['fidelity_status'] == 'unreviewed_partial',
                'item_mismatch')
    defaults = {'derivation_id': DERIVATION,
                'manifest_sha256': MANIFEST_SHA, 'page_number': 22}
    negatives = (
        ('wrong_source', 'get_graph_labels_page',
         dict(defaults, source=dict(document.SOURCE, source_sha256='0' * 64)),
         'source_mismatch'),
        ('wrong_manifest', 'get_graph_labels_page',
         dict(defaults, manifest_sha256='0' * 64), 'labels_identity_mismatch'),
        ('outside_pages', 'get_graph_labels_page',
         dict(defaults, page_number=23), 'page_out_of_scope'),
        ('unknown_item', 'fetch_graph_label_item',
         {'derivation_id': DERIVATION, 'manifest_sha256': MANIFEST_SHA,
          'item_id': '0' * 64}, 'evidence_unavailable'),
    )
    for name, operation, fields, code in negatives:
        bad = exchange(args, operation, **fields)
        require(bad['status'] != 'ok' and bad['result'] is None and
                bad['error']['code'] == code, f'{name}_accepted')
    print(json.dumps({'status': 'consumer_graph_labels_passed',
                      'derivation_id': DERIVATION,
                      'manifest_sha256': MANIFEST_SHA,
                      'pages': [number for number, _ in COUNTS],
                      'labels': sum(count for _, count in COUNTS),
                      'negative_controls': [row[0] for row in negatives],
                      'fidelity_status': 'unreviewed_partial'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
