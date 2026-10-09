"""Audit page coverage across the pinned Skopos IMSS PDF derivatives."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import secrets
import unicodedata

from pypdf import PdfReader

from scripts import skopos_document_pilot as document


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = document.SOURCE_SHA
POLICY_SHA = '4d09e940ea340ea686c77b4fab84dcf8bb05a371c2119434e60d8744227b3c6b'
NATIVE_SHA = '7f81b1616b10549439cd536737e76663cfea7cec3bf7a6ec3fbf10241d8292ed'
OCR_SHA = '3ca9d7a5be5e451f63608015585a4eee92d2109046d390de99d793ac2f83651d'
GRAPH_SHA = '8a1880b84b0e52f934f09759f3a83efb5a3a752afda914d6c5cce9c7803aaaee'
SPECIAL = [1, 18, 19, 20, 21, 22]
SENTINELS = [2, 18, 22, 23, 61, 188]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def load_manifest(path, expected_sha, pages, ocr_pages):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == expected_sha,
            'manifest_changed')
    manifest = json.loads(raw)
    document.check_manifest(manifest, manifest['derivation_id'], POLICY_SHA,
                            pages, ocr_pages)
    require(manifest['parent'] == document.SOURCE, 'parent_mismatch')
    return manifest


def words(text):
    normalized = unicodedata.normalize('NFKC', text).casefold()
    return re.findall(r'\w+', normalized, flags=re.UNICODE)


def overlap(left, right):
    return sum((Counter(left) & Counter(right)).values())


def audit(pdf_path, native, ocr, graph):
    require(hashlib.sha256(pdf_path.read_bytes()).hexdigest() == SOURCE_SHA,
            'source_changed')
    reader = PdfReader(str(pdf_path))
    require(len(reader.pages) == 188, 'pdf_page_count')
    require([page['page_number'] for page in native['pages']] ==
            list(range(1, 189)), 'native_page_inventory')
    require([page['page_number'] for page in ocr['pages']] == SPECIAL and
            [page['page_number'] for page in graph['pages']] == SPECIAL[1:],
            'special_page_inventory')
    require(native['pages'][0]['native_text']['status'] == 'no_text' and
            not native['pages'][0]['native_text']['lines'] and
            ocr['pages'][0]['ocr_text']['status'] == 'extracted' and
            len(ocr['pages'][0]['ocr_text']['lines']) == 20,
            'cover_page_layers')
    require(all(page['visual_graph']['status'] == 'partial'
                for page in graph['pages']), 'organigram_status')
    counts = {'pypdf': 0, 'skopos': 0, 'overlap': 0}
    minimum = (1.0, None)
    low_pages = []
    logo_hashes = set()
    for number, (source_page, derived) in enumerate(
            zip(reader.pages, native['pages']), 1):
        source_words = words(source_page.extract_text() or '')
        derived_words = words(' '.join(line['text'] for line in
                                       derived['native_text']['lines']))
        if number == 1:
            require(not source_words and not derived_words, 'cover_has_native_text')
            continue
        require(derived['native_text']['status'] == 'extracted' and
                source_words and derived_words, f'page_{number}_missing_text')
        text = ' '.join(line['text'] for line in derived['native_text']['lines'])
        require(re.search(r'Página\s+' + str(number) + r'\s+de\s+188', text),
                f'page_{number}_footer')
        matched = overlap(source_words, derived_words)
        recall = matched / len(source_words)
        require(recall >= 0.95, f'page_{number}_native_disagreement')
        if recall < minimum[0]:
            minimum = (recall, number)
        if recall < 0.99:
            low_pages.append(number)
        counts['pypdf'] += len(source_words)
        counts['skopos'] += len(derived_words)
        counts['overlap'] += matched
        if number >= 23:
            images = [value.get_object().get_data() for value in
                      source_page['/Resources'].get('/XObject', {}).values()
                      if value.get_object().get('/Subtype') == '/Image']
            require(len(images) == 1, f'page_{number}_raster_inventory')
            logo_hashes.add(hashlib.sha256(images[0]).hexdigest())
    require(len(logo_hashes) == 1, 'post_organigram_raster_variation')
    p18 = ' '.join(line['text'] for line in
                   native['pages'][17]['native_text']['lines'])
    p22 = ' '.join(line['text'] for line in
                   native['pages'][21]['native_text']['lines'])
    p23 = ' '.join(line['text'] for line in
                   native['pages'][22]['native_text']['lines'])
    require('6. Organigramas' in p18 and '6.1.4' in p22 and
            '7. Funciones Sustantivas' in p23, 'section_boundary')
    return {'status': 'full_page_inventory_passed', 'pages': 188,
            'native_extracted_pages': 187, 'cover_ocr_lines': 20,
            'organigram_pages': SPECIAL[1:], 'organigram_status': 'partial',
            'section_7_starts_page': 23, 'native_tokens': counts,
            'minimum_token_recall': {'page': minimum[1], 'value': minimum[0]},
            'pages_below_0_99': low_pages,
            'post_page_22_raster_payloads': len(logo_hashes),
            'text_fidelity': 'unreviewed_visual',
            'page_23_to_188_visual_inventory': 'separate_contact_sheet_review'}


def check_live_evidence(args, native):
    checked = []
    for number in SENTINELS:
        page = native['pages'][number - 1]
        line = page['native_text']['lines'][len(page['native_text']['lines']) // 2]
        evidence, _ = document.checked_exchange(args, document.request(
            'fetch_evidence', 'eg-full-' + secrets.token_hex(10),
            source=document.SOURCE, derivation_id=native['derivation_id'],
            manifest_sha256=NATIVE_SHA, item_id=line['item_id']))
        require(evidence['page_number'] == number and
                evidence['modality'] == 'native_text' and
                evidence['item'] == line and
                evidence['parent'] == document.SOURCE and
                evidence['fidelity_status'] == 'unreviewed',
                f'page_{number}_live_evidence')
        checked.append(number)
    bad, _ = document.exchange(args.socket, args.requests_root,
                               document.request(
        'fetch_evidence', 'eg-full-bad-' + secrets.token_hex(10),
        source=document.SOURCE, derivation_id=native['derivation_id'],
        manifest_sha256=NATIVE_SHA, item_id='0' * 64))
    require(bad['status'] != 'ok' and bad['result'] is None and
            bad['error']['code'] == 'evidence_unavailable',
            'missing_item_accepted')
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-manifest', type=Path, required=True)
    parser.add_argument('--ocr-manifest', type=Path, required=True)
    parser.add_argument('--graph-manifest', type=Path, required=True)
    parser.add_argument('--socket', type=Path)
    parser.add_argument('--requests-root', type=Path)
    args = parser.parse_args()
    native = load_manifest(args.native_manifest, NATIVE_SHA,
                           list(range(1, 189)), [])
    ocr = load_manifest(args.ocr_manifest, OCR_SHA, SPECIAL, SPECIAL)
    graph = load_manifest(args.graph_manifest, GRAPH_SHA, SPECIAL[1:],
                          SPECIAL[1:])
    result = audit(ROOT / 'docs/fuentes/imss/2000-002-001.pdf',
                   native, ocr, graph)
    if args.socket or args.requests_root:
        require(args.socket is not None and args.requests_root is not None,
                'incomplete_live_args')
        result['live_sentinel_pages'] = check_live_evidence(args, native)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
