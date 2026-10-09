"""Fail-closed checks for the page-one visual candidate comparison."""

import copy
import json
import unittest

from scripts import skopos_p1_visual_gate as gate
from scripts import skopos_document_pilot as document


class PageOneVisualGateTests(unittest.TestCase):
    def fixture(self):
        reference = json.loads(gate.REFERENCE.read_text())
        lines = [{'item_id': f'synthetic-{index}', 'text': 'fixture'}
                 for index in range(20)]
        for region in reference['regions']:
            for index, item_id in zip(gate.REGIONS[region['region_id']],
                                      region['ocr_item_ids']):
                lines[index]['item_id'] = item_id
        image = b'\x89PNG\r\n\x1a\nsynthetic-image'
        render_sha = gate.hashlib.sha256(image).hexdigest()
        reference['producer_derivative']['render_sha256'] = render_sha
        manifest = {
            'derivation_id': gate.DERIVATION, 'parent': document.SOURCE,
            'fidelity_status': 'unreviewed',
            'pages': [{'page_number': 1, 'native_text': {'status': 'no_text'},
                       'ocr_text': {'status': 'extracted', 'lines': lines},
                       'render': {'sha256': render_sha}}],
        }
        return reference, manifest, image

    def test_candidate_is_recoverable_but_cannot_authorize_quote(self):
        reference, manifest, image = self.fixture()
        result = gate.evaluate(reference, manifest, image)
        self.assertEqual('p1_layers_recovered', result['status'])
        self.assertEqual('blocked_pending_independent_review',
                         result['literal_quote_status'])
        promoted = copy.deepcopy(reference)
        promoted['status'] = 'independently_confirmed'
        promoted['literal_quote_allowed'] = True
        with self.assertRaisesRegex(ValueError, 'reference_status'):
            gate.evaluate(promoted, manifest, image)

    def test_mismatched_ocr_locator_and_render_are_rejected(self):
        reference, manifest, image = self.fixture()
        changed = copy.deepcopy(reference)
        changed['regions'][2]['ocr_item_ids'][0] = 'other-item'
        with self.assertRaisesRegex(ValueError, 'ocr_line_binding'):
            gate.evaluate(changed, manifest, image)
        with self.assertRaisesRegex(ValueError, 'render_identity'):
            gate.evaluate(reference, manifest, image + b'changed')


if __name__ == '__main__':
    unittest.main()
