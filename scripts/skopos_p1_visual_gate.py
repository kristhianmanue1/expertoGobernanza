"""Recover Skopos page-one OCR and compare it with a local visual candidate."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import secrets
import unicodedata

from scripts import skopos_document_pilot as document


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'docs/evidencia/imss-p1-visual-candidate-2026-10-08.json'
REFERENCE_SHA = '53918240b3ac3c494cc9c462c7c2e95971e48d0ecdd4c493f6dcfd1afd7a1b80'
MANIFEST_SHA = '3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d'
DERIVATION = '7f132071b5e1c372e41d0ce9a83df7c966955c7fcb7036f80cdcbcecf5654a46'
POLICY_SHA = '4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b'
REGIONS = {'title': [2, 3], 'signer': [5], 'role': [6],
           'stamp': [9, 10, 11, 12, 13], 'bottom_paragraph': list(range(14, 20))}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def tokens(text):
    normalized = unicodedata.normalize('NFKC', text).casefold()
    return re.findall(r'\w+', normalized, flags=re.UNICODE)


def edit_distance(left, right):
    previous = list(range(len(right) + 1))
    for row, item in enumerate(left, 1):
        current = [row]
        for column, other in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[column] + 1,
                               previous[column - 1] + (item != other)))
        previous = current
    return previous[-1]


def evaluate(reference, manifest, render_bytes):
    require(reference.get('schema') ==
            'expertogobernanza/imss-p1-visual-candidate/v0.1' and
            reference.get('status') == 'codex_visual_candidate_unconfirmed' and
            reference.get('literal_quote_allowed') is False and
            reference.get('method', {}).get('independent_second_reviewer') is False,
            'reference_status')
    source = reference['source']
    require(source == {'material_id': 'imss-2000-002-001', 'page_number': 1,
                       'sha256': document.SOURCE_SHA}, 'reference_source')
    binding = reference['producer_derivative']
    require(binding['derivation_id'] == DERIVATION and
            binding['manifest_sha256'] == MANIFEST_SHA and
            manifest['derivation_id'] == DERIVATION and
            manifest['parent'] == document.SOURCE and
            manifest['fidelity_status'] == 'unreviewed', 'manifest_identity')
    pages = [page for page in manifest['pages'] if page['page_number'] == 1]
    require(len(pages) == 1, 'page_inventory')
    page = pages[0]
    require(page['native_text']['status'] == 'no_text' and
            page['ocr_text']['status'] == 'extracted' and
            len(page['ocr_text']['lines']) == 20, 'page_layers')
    render = page['render']
    require(render['sha256'] == binding['render_sha256'] and
            hashlib.sha256(render_bytes).hexdigest() == render['sha256'] and
            render_bytes.startswith(b'\x89PNG\r\n\x1a\n'), 'render_identity')
    lines = page['ocr_text']['lines']
    regions = reference['regions']
    require({region['region_id'] for region in regions} == set(REGIONS) and
            len(regions) == len(REGIONS), 'region_inventory')
    comparisons = {}
    for region in regions:
        name = region['region_id']
        selected = [lines[index] for index in REGIONS[name]]
        require(region['ocr_item_ids'] == [line['item_id'] for line in selected],
                'ocr_line_binding')
        expected = region['visual_transcription_candidate']
        require(isinstance(expected, str) and expected.strip(), 'visual_candidate')
        observed = ' '.join(line['text'] for line in selected)
        expected_words, observed_words = tokens(expected), tokens(observed)
        comparisons[name] = {'candidate_words': len(expected_words),
                             'ocr_words': len(observed_words),
                             'word_edits': edit_distance(expected_words,
                                                         observed_words),
                             'exact_words': expected_words == observed_words,
                             'ocr_item_ids': region['ocr_item_ids']}
    return {'status': 'p1_layers_recovered', 'source_sha256': document.SOURCE_SHA,
            'manifest_sha256': MANIFEST_SHA, 'render_sha256': render['sha256'],
            'visual_status': 'codex_visual_candidate_unconfirmed',
            'ocr_status': 'unreviewed',
            'literal_quote_status': 'blocked_pending_independent_review',
            'comparisons': comparisons}


def run(args):
    require(hashlib.sha256((ROOT / 'docs/fuentes/imss/2000-002-001.pdf')
                           .read_bytes()).hexdigest() == document.SOURCE_SHA,
            'local_original_changed')
    reference_raw = REFERENCE.read_bytes()
    require(hashlib.sha256(reference_raw).hexdigest() == REFERENCE_SHA,
            'visual_reference_changed')
    reference = json.loads(reference_raw)
    offer, _ = document.checked_exchange(args, document.request(
        'describe_document_capabilities',
        'eg-p1-cap-' + secrets.token_hex(10)))
    require(offer['policy']['id'] ==
            'expertogobernanza/imss-2000-002-001-derivatives' and
            offer['policy']['version'] == 'v0.1-2026-10-08' and
            offer['policy']['policy_sha256'] == POLICY_SHA and
            offer['capabilities']['selective_ocr'] == 'partial',
            'capability_mismatch')
    raw = document.fetch(args, DERIVATION, MANIFEST_SHA, 'manifest', MANIFEST_SHA)
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, 'manifest_bytes')
    manifest = json.loads(raw)
    page = next(p for p in manifest['pages'] if p['page_number'] == 1)
    render = page['render']
    image = document.fetch(args, DERIVATION, MANIFEST_SHA,
                           render['artifact_id'], render['sha256'])
    result = evaluate(reference, manifest, image)
    role_line = page['ocr_text']['lines'][6]
    evidence, _ = document.checked_exchange(args, document.request(
        'fetch_evidence', 'eg-p1-line-' + secrets.token_hex(10),
        source=document.SOURCE, derivation_id=DERIVATION,
        manifest_sha256=MANIFEST_SHA, item_id=role_line['item_id']))
    require(evidence['item'] == role_line and
            evidence['page_number'] == 1 and
            evidence['modality'] == 'ocr_text' and
            evidence['fidelity_status'] == 'unreviewed' and
            evidence['render_sha256'] == render['sha256'],
            'evidence_correlation')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket', type=Path, required=True)
    parser.add_argument('--requests-root', type=Path, required=True)
    parser.add_argument('--delivery-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
