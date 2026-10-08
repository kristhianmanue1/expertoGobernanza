"""Verify one IMSS PDF custody exchange through the Skopos host socket."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket


ROOT = Path(__file__).resolve().parents[1]
SOURCE_REF = 'docs/fuentes/imss/2000-002-001.pdf'
PROVENANCE_REF = 'docs/fuentes/imss/2000-002-001-PROCEDENCIA.md'
SOURCE_SHA256 = '719d6da341bff3733750f05357de50ca09fabc7c31c4354186dae8a7a3a70323'
PROVENANCE_SHA256 = 'f934b0ec1bfbe97aae347b86bb3aa4e0831af79f704e571c27702f9203b62bff'
SOURCE_LENGTH = 1311822
CONTRACT = 'expertogobernanza/skopos-source'
VERSION = 'v0.2'
HOST_SCHEMA = 'skopos/pdf-custody-host/v0.1'
POLICY_SHA256 = 'a92b9252cc27a5a0a421fa1422b583d61cafdb0026956794a302c09db3c52160'
ADMISSION_ID = 'imss-2000-002-001-r1-admit-v1'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def write_new(directory, name, raw):
    descriptor = os.open(directory / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                         0o600)
    with os.fdopen(descriptor, 'wb') as target:
        target.write(raw)
        target.flush()
        os.fsync(target.fileno())


def exchange(socket_path, requests_root, request):
    raw = json.dumps(request, sort_keys=True, separators=(',', ':'),
                     ensure_ascii=False).encode('utf-8')
    digest = hashlib.sha256(raw).hexdigest()
    nonce = secrets.token_hex(12)
    request_ref = f'{nonce}.request.json'
    envelope_ref = f'{nonce}.envelope.json'
    envelope = {'request_file_ref': request_ref, 'request_sha256': digest,
                'request_id': request['request_id'],
                'contract_id': CONTRACT, 'contract_version': VERSION}
    write_new(requests_root, request_ref, raw)
    write_new(requests_root, envelope_ref,
              json.dumps(envelope, sort_keys=True).encode('utf-8'))
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(5)
        connection.connect(str(socket_path))
        connection.sendall(json.dumps({'envelope_ref': envelope_ref}).encode() + b'\n')
        response_raw = connection.makefile('rb').readline(65537)
    require(0 < len(response_raw) <= 65536, 'response_size')
    response = json.loads(response_raw)
    require(response.get('schema') == HOST_SCHEMA, 'response_schema')
    require(response.get('contract_id') == CONTRACT, 'response_contract')
    require(response.get('contract_version') == VERSION, 'response_version')
    require(response.get('request_id') == request['request_id'], 'response_request_id')
    require(response.get('request_sha256') == digest, 'response_request_digest')
    require(response.get('producer_version') == HOST_SCHEMA, 'producer_version')
    require(response.get('adapter_version') ==
            'skopos/pdf-binary-reference/v0.1', 'adapter_version')
    return response, digest


def request(operation, request_id, **fields):
    return {'contract_id': CONTRACT, 'contract_version': VERSION,
            'request_id': request_id, 'operation': operation,
            'project_id': 'expertogobernanza', **fields}


def run(args):
    source = (ROOT / SOURCE_REF).read_bytes()
    provenance = (ROOT / PROVENANCE_REF).read_bytes()
    require(len(source) == SOURCE_LENGTH, 'source_length')
    require(hashlib.sha256(source).hexdigest() == SOURCE_SHA256, 'source_hash')
    require(hashlib.sha256(provenance).hexdigest() == PROVENANCE_SHA256,
            'provenance_hash')
    requests_root = Path(args.requests_root)
    delivery_root = Path(args.delivery_root)
    require(requests_root.is_dir() and delivery_root.is_dir(), 'host_roots_missing')

    capabilities, _ = exchange(args.socket, requests_root,
                               request('describe_capabilities', 'imss-pdf-capabilities'))
    require(capabilities.get('status') == 'ok', 'capabilities_failed')
    offer = capabilities['result']['policy']
    require(offer['id'] == args.policy_id and
            offer['version'] == args.policy_version, 'policy_identity')
    require(offer['policy_sha256'] == POLICY_SHA256, 'policy_digest')
    require(offer['recovery_requirement'] == 'while_reference_available',
            'recovery_requirement')
    require(offer['seal_policy'] == 'not_required', 'seal_policy')
    require(offer['max_bytes'] >= SOURCE_LENGTH, 'max_bytes')
    require(offer['retention_until'] == '2026-11-08T00:00:00Z',
            'retention_until')
    require('verified_external_reference' in offer['custody_modes'], 'custody_mode')
    require('single_object' in offer['scope'], 'scope')
    require(capabilities['result']['format_validation'] == 'pdf_header_only',
            'format_validation')

    admission = request(
        'admit_original', ADMISSION_ID, material_id='imss-2000-002-001',
        source_revision=1, scope='single_object',
        source_delivery={'mode': 'authorized_reference', 'file_ref': SOURCE_REF},
        expected_source_sha256=SOURCE_SHA256,
        media_type_declared='application/pdf',
        classification='consumer_declared_public',
        custody_mode='verified_external_reference',
        custody_policy_id=args.policy_id,
        custody_policy_version=args.policy_version,
        seal_profile_id=args.seal_profile_id,
        recovery_requirement='while_reference_available',
        limits={'max_bytes': 2000000, 'allow_network': False, 'allow_ocr': False},
        provenance={'asserted_by': 'expertogobernanza',
                    'claim_status': 'consumer_declared',
                    'record_ref': PROVENANCE_REF,
                    'record_sha256': PROVENANCE_SHA256})
    admitted, admission_digest = exchange(args.socket, requests_root, admission)
    require(admitted.get('status') == 'ok', f'admission_failed:{admitted.get("error")}')
    result = admitted['result']
    require(result['admission_status'] in ('admitted', 'duplicate'), 'admission_status')
    require(result['source_sha256'] == SOURCE_SHA256, 'admission_source_sha')
    require(result['request_sha256'] == admission_digest, 'admission_request_sha')

    identity = {'material_id': 'imss-2000-002-001', 'source_revision': 1,
                'expected_source_sha256': SOURCE_SHA256}
    received, _ = exchange(args.socket, requests_root,
                           request('receipt', 'imss-pdf-receipt', **identity,
                                   admission_request_sha256=admission_digest))
    require(received.get('status') == 'ok', 'receipt_failed')
    require(received['result']['receipt_id'] == result['receipt_id'], 'receipt_mismatch')
    require(received['result']['request_sha256'] == admission_digest,
            'receipt_admission_digest')
    rejected, _ = exchange(args.socket, requests_root,
                           request('receipt', 'imss-pdf-receipt-wrong-digest',
                                   **identity, admission_request_sha256='0' * 64))
    require(rejected.get('status') == 'invalid_input' and
            rejected.get('error', {}).get('code') == 'revision_conflict',
            'wrong_receipt_digest_was_accepted')
    other_material, _ = exchange(
        args.socket, requests_root,
        dict(admission, request_id='imss-pdf-reject-other-material',
             material_id='other-in-same-project'))
    require(other_material.get('status') == 'invalid_input' and
            other_material.get('error', {}).get('code') == 'material_not_allowed',
            'other_material_was_accepted')

    output_ref = 'imss-pdf-' + secrets.token_hex(12) + '.pdf'
    fetched, _ = exchange(args.socket, requests_root,
                          request('fetch_original', 'imss-pdf-fetch', **identity,
                                  output_ref=output_ref))
    require(fetched.get('status') == 'ok', f'fetch_failed:{fetched.get("error")}')
    output = delivery_root / output_ref
    returned = output.read_bytes()
    require(fetched['result']['bytes_ref'] == output_ref, 'output_ref')
    require(fetched['result']['byte_length'] == SOURCE_LENGTH, 'reported_length')
    require(fetched['result']['source_sha256'] == SOURCE_SHA256, 'reported_hash')
    require(len(returned) == SOURCE_LENGTH and returned == source, 'returned_bytes')
    require(hashlib.sha256(returned).hexdigest() == SOURCE_SHA256, 'returned_hash')

    print(json.dumps({'status': 'verified_reference_pilot',
                      'contract_id': CONTRACT, 'contract_version': VERSION,
                      'host_schema': HOST_SCHEMA,
                      'policy_id': args.policy_id,
                      'policy_version': args.policy_version,
                      'material_id': identity['material_id'],
                      'source_revision': 1,
                      'source_sha256': SOURCE_SHA256,
                      'provenance_sha256': PROVENANCE_SHA256,
                      'byte_length': SOURCE_LENGTH,
                      'admission_request_sha256': admission_digest,
                      'receipt_id': result['receipt_id'],
                      'admission_status': result['admission_status'],
                      'output_ref': output_ref,
                      'output_sha256': hashlib.sha256(returned).hexdigest()},
                     sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', type=Path, required=True)
    parser.add_argument('--requests-root', type=Path, required=True)
    parser.add_argument('--delivery-root', type=Path, required=True)
    parser.add_argument('--policy-id', required=True)
    parser.add_argument('--policy-version', required=True)
    parser.add_argument('--seal-profile-id', required=True)
    run(parser.parse_args())


if __name__ == '__main__':
    main()
