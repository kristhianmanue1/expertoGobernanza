"""Run a bounded Skopos -> Agora check for five pinned CTIM sources."""

from contextlib import contextmanager
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKOPOS = Path('/Users/krisnova/www/aria/skopos')
AGORA = Path('/Users/krisnova/www/aria/agora')
RUN = SKOPOS / 'runs/source-imss-ctim-pilot-v1'
PDF_IDS = (
    'imss-administration-1000-002-001-2025',
    'imss-procedure-2900-003-001-2021',
    'imss-pobalines-1000-001-029-2022',
)
HTML_ITEMS = {
    'dof-pobalines-1000-001-029-2021':
        'e594a8d40939b7f09a288219c53e1f40b762a96f8264353a3e1f9366306cf4c4',
    'dof-pobalines-1000-001-029-2022-agreement':
        '2753eb895f2bbf1e362184963dbefd8a96740774e1967aa93337881a12de1eb8',
}
EXPECTED_DERIVATIVES = {
    PDF_IDS[0]: '84f5ef8ebd2934b4d1f3e6802cc2af7117ac85e9687fbd0da0faa7fc4f4a5530',
    PDF_IDS[1]: '773a2900597873c96488142a378b11b86b00bb58c07f3c06c26e98adff789b1b',
    PDF_IDS[2]: '9dd220c141bf660fdd251c556deeb7c2b7827f85a1a51bb6c80d3c691a2a67f1',
    'dof-pobalines-1000-001-029-2021':
        '2d9812a3d6e15e9a98c8087c84384631a5c9faee64a8864a0d0e239f1f07fc6f',
    'dof-pobalines-1000-001-029-2022-agreement':
        '949a7db37ced1b87c484e2007a3c09850d475b9558375117eb54395d2321289a',
}
DATES = {
    PDF_IDS[0]: '2025-04-16',
    PDF_IDS[1]: '2021-06-03',
    PDF_IDS[2]: '2022-11-28',
    'dof-pobalines-1000-001-029-2021': '2021',
    'dof-pobalines-1000-001-029-2022-agreement': '2022-11-28',
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def call(arguments):
    result = subprocess.run(arguments, cwd=SKOPOS, text=True, capture_output=True)
    require(result.returncode == 0, f'command_failed:{arguments[1:]}:{result.stderr[-500:]}')
    return json.loads(result.stdout)


@contextmanager
def skopos_runtime():
    py = str(SKOPOS / '.venv/bin/python')
    controller = [py, 'scripts/pdf_custody_pilot.py']
    call(controller + ['preflight'])
    status = subprocess.run(controller + ['status'], cwd=SKOPOS,
                            text=True, capture_output=True)
    require(status.returncode != 0, 'skopos_runtime_already_running')
    started = False
    try:
        call(controller + ['start'])
        started = True
        yield py
    finally:
        if started:
            stopped = call(controller + ['stop'])
            require(stopped['status'] == 'stopped', 'skopos_shutdown_unconfirmed')


def inventory():
    register = json.loads((ROOT / 'docs/evidencia/ctim-source-register-2026-10-08.json').read_text())
    sources = {source['id']: source for source in register['sources']}
    require(all(ident in sources for ident in (*PDF_IDS, *HTML_ITEMS)), 'source_missing')
    for ident in (*PDF_IDS, *HTML_ITEMS):
        source = sources[ident]
        raw = (ROOT / source['path']).read_bytes()
        require(digest(raw) == source['sha256'] and len(raw) == source['bytes'],
                'source_changed:' + ident)
    return sources


def exchange_record(source, text, locator, producer_sha, producer_version,
                    derivative_id, media_type=None):
    raw = (text + '\n').encode('utf-8')
    manifest = {
        'schema': 'agora/source-evidence-exchange/v1',
        'source': {'id': source['id'], 'sha256': source['sha256'],
                   'media_type': media_type or source['media_type'],
                   'revision': '1', 'uri': source['url'],
                   'temporal': {'document_date': DATES[source['id']], 'status': 'not_assessed'}},
        'derivative': {'id': derivative_id, 'sha256': digest(raw), 'coverage': 'partial',
                       'producer': {'system': 'skopos', 'version': producer_version,
                                    'manifest_sha256': producer_sha,
                                    'derivation_id': derivative_id},
                       'normalization': {'status': 'not_applied', 'description': None}},
        'segments': [{'id': 'selected-item', 'start_byte': 0, 'end_byte': len(raw),
                      'sha256': digest(raw), 'locator': locator,
                      'modality': 'native_text' if source['media_type'] == 'application/pdf'
                      else 'html_text', 'extraction_status': 'unreviewed'}],
    }
    return raw, manifest


def pdf_exchange(ident, source):
    area = RUN / ident
    receipt = json.loads((area / 'derivation-operation-receipt.json').read_text())
    raw_manifest = (area / 'derived' / receipt['derivation_id'] / 'manifest.json').read_bytes()
    require(digest(raw_manifest) == receipt['manifest_sha256'] == EXPECTED_DERIVATIVES[ident],
            'manifest_changed:' + ident)
    producer = json.loads(raw_manifest)
    response = json.loads((area / 'queries/evidence-response.json').read_text())
    require(response['status'] == 'ok', 'skopos_response_failed:' + ident)
    result = response['result']
    require(result['parent'] == producer['parent'] and
            result['parent']['source_sha256'] == source['sha256'] and
            result['fidelity_status'] == 'unreviewed', 'pdf_lineage_changed:' + ident)
    page = next((page for page in producer['pages']
                 if page['page_number'] == result['page_number']), None)
    require(page is not None and result['item'] in page[result['modality']]['lines'],
            'pdf_item_not_in_manifest:' + ident)
    item = result['item']
    locator = {'kind': 'pdf_page', 'value': {'page': result['page_number'],
               'item_id': item['item_id'], 'bbox': item['bbox']}}
    data, manifest = exchange_record(source, item['text'], locator,
                                     receipt['manifest_sha256'],
                                     producer['contract_version'], receipt['derivation_id'])
    return data, manifest, {'page': result['page_number'], 'item_id': item['item_id'],
                            'text': item['text'], 'producer_manifest_sha256': digest(raw_manifest)}


def html_exchange(ident, source):
    area = RUN / ident
    path = area / 'derived/html-text.json'
    raw_derivative = path.read_bytes()
    require(digest(raw_derivative) == EXPECTED_DERIVATIVES[ident],
            'html_derivative_changed:' + ident)
    producer = json.loads(raw_derivative)
    item = next((item for item in producer['items'] if item['item_id'] == HTML_ITEMS[ident]), None)
    require(item is not None and producer['source_sha256'] == source['sha256'] and
            producer['fidelity_status'] == 'unreviewed', 'html_lineage_changed:' + ident)
    original = (ROOT / source['path']).read_bytes()
    fragment = original[item['start_byte']:item['end_byte']]
    require(digest(fragment) == item['raw_sha256'] and
            digest(item['text'].encode('utf-8')) == item['text_sha256'],
            'html_fragment_changed:' + ident)
    locator = {'kind': 'html_fragment', 'value': {'start_byte': item['start_byte'],
               'end_byte': item['end_byte'], 'item_id': item['item_id']}}
    encoding = {'latin-1': 'iso-8859-1', 'utf-8': 'utf-8'}.get(producer['encoding'])
    require(encoding is not None, 'unsupported_html_encoding:' + ident)
    data, manifest = exchange_record(source, item['text'], locator,
                                     digest(raw_derivative), producer['extractor_version'],
                                     'html-item-' + item['item_id'],
                                     'text/html; charset=' + encoding)
    return data, manifest, {'start_byte': item['start_byte'], 'end_byte': item['end_byte'],
                            'item_id': item['item_id'], 'text': item['text'],
                            'raw_fragment_sha256': item['raw_sha256'],
                            'producer_manifest_sha256': digest(raw_derivative)}


def run():
    sources = inventory()
    with skopos_runtime() as py:
        recovery = [call([py, 'scripts/source_ctim_verify.py', '--material', ident])
                    for ident in (*PDF_IDS, *HTML_ITEMS)]
        queries = [call([py, 'scripts/source_ctim_query.py', '--material', ident])
                   for ident in PDF_IDS]
    require(all(item['negative_code'] == 'material_not_allowed' for item in recovery),
            'negative_control_failed')
    sys.path.insert(0, str(AGORA / 'src'))
    from agora.source import SourceError
    from agora.source_evidence_exchange import validate_exchange, resolve_bundle
    summaries = {}
    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        exchanges = []
        for ident in (*PDF_IDS, *HTML_ITEMS):
            data, manifest, summary = (pdf_exchange(ident, sources[ident]) if ident in PDF_IDS
                                       else html_exchange(ident, sources[ident]))
            derived = temp_root / (ident + '.txt')
            derived.write_bytes(data)
            original = ROOT / sources[ident]['path']
            _, _, integrity = validate_exchange(derived, manifest, original)
            require(integrity == 'sha256_verified', 'agora_original_unverified:' + ident)
            manifest_raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True).encode()
            exchanges.append((derived, manifest_raw, manifest, original))
            summaries[ident] = {'source_sha256': sources[ident]['sha256'],
                                'exchange_sha256': digest(manifest_raw), **summary}
        altered = copy.deepcopy(exchanges[0][2])
        altered['segments'][0]['locator']['value']['page'] = 0
        try:
            validate_exchange(exchanges[0][0], altered, exchanges[0][3])
        except SourceError as error:
            require(str(error) == 'invalid_pdf_page', 'unexpected_locator_rejection')
        else:
            raise RuntimeError('altered_locator_accepted')
        altered_html = copy.deepcopy(exchanges[3][2])
        altered_html['segments'][0]['locator']['value']['end_byte'] = 0
        try:
            validate_exchange(exchanges[3][0], altered_html, exchanges[3][3])
        except SourceError as error:
            require(str(error) == 'invalid_html_byte_range', 'unexpected_html_rejection')
        else:
            raise RuntimeError('altered_html_locator_accepted')
        hashes = [digest(item[1]) for item in exchanges]
        def refs(indexes):
            return [{'manifest_sha256': hashes[index], 'segment_id': 'selected-item',
                     'start_byte': 0, 'end_byte': exchanges[index][0].stat().st_size}
                    for index in indexes]
        candidate = {'schema': 'agora/source-evidence-bundle-candidate/v1',
                     'manifest_sha256s': hashes,
                     'claims': [
                         {'id': 'institutional-link-unresolved', 'kind': 'relation_candidate',
                          'text': 'Compare CTIM and DA organizational references.',
                          'relation': {'kind': 'identity_unresolved_candidate',
                                       'temporal_status': 'not_assessed',
                                       'identity_status': 'not_assessed',
                                       'normalization': {'status': 'not_applied', 'description': None}},
                          'evidence_refs': refs((0, 1))},
                         {'id': 'pobalines-version-candidate', 'kind': 'relation_candidate',
                          'text': 'Compare 2021 text, later POBALINES, and 2023 agreement.',
                          'relation': {'kind': 'version_relation_candidate',
                                       'version_relation': 'supersedes',
                                       'temporal_status': 'not_assessed',
                                       'identity_status': 'not_assessed',
                                       'normalization': {'status': 'not_applied', 'description': None}},
                          'evidence_refs': refs((2, 3, 4))}]}
        bundle = resolve_bundle(exchanges, candidate)
        require(bundle['status'] == 'candidate_unreviewed' and
                bundle['admitted'] is False and bundle['provider_calls'] == 0 and
                len(bundle['claims']) == 2, 'agora_bundle_changed')
        return {'status': 'ok', 'sources': summaries, 'recovery': recovery,
                'queries': queries, 'relations': [item['relation'] for item in bundle['claims']],
                'agora_negative': ['invalid_pdf_page', 'invalid_html_byte_range'],
                'runtime': 'stopped'}


if __name__ == '__main__':
    try:
        print(json.dumps(run(), ensure_ascii=False, sort_keys=True))
    except (RuntimeError, ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False),
              file=sys.stderr)
        raise SystemExit(1)
