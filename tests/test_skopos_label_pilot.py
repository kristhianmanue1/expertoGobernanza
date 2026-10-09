"""Mutation control for the bilateral label candidate verifier."""

import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import skopos_label_pilot as pilot


class LabelPilotTests(unittest.TestCase):
    def test_omitted_line_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'render.png').write_bytes(b'fixture-render')
            box = [0.1, 0.1, 0.9, 0.9]
            line_box = [0.2, 0.2, 0.8, 0.3]
            line = {'item_id': 'line-1', 'bbox': line_box,
                    'text': 'UNIDAD DE PRUEBA'}
            node = {'node_id': 'n1', 'item_id': 'node-1', 'bbox': box}
            manifest_page = {
                'page_number': 18,
                'render': {'file_ref': 'render.png',
                           'sha256': pilot.digest(b'fixture-render')},
                'native_text': {'status': 'extracted', 'lines': [line]},
                'ocr_text': {'status': 'no_text', 'lines': []},
                'visual_graph': {'nodes': [node], 'connectors': [],
                                 'edges': [], 'unknown': []},
            }
            candidates = [
                {'method': 'native_text', 'text': line['text'],
                 'line_item_ids': [line['item_id']],
                 'line_bboxes': [line_box], 'status': 'unreviewed'},
                {'method': 'selective_ocr', 'text': '',
                 'line_item_ids': [], 'line_bboxes': [], 'status': 'no_lines'},
            ]
            result = {
                'derivation_id': pilot.DERIVATION,
                'manifest_sha256': pilot.MANIFEST_SHA,
                'label_policy_sha256': pilot.POLICY_SHA,
                'source_sha256': pilot.SOURCE_SHA,
                'page_number': 18,
                'fidelity_status': 'unreviewed',
                'render_sha256': manifest_page['render']['sha256'],
                'nodes': [{'node_id': 'n1', 'parent_item_id': 'node-1',
                           'bbox': box, 'label_candidates': candidates}],
                'edges': [], 'unresolved_connectors': [],
                'coverage': {
                    'graph_status': 'partial',
                    'topology_completeness': 'unreviewed_partial',
                    'node_count': 1, 'edge_count': 0,
                    'native_text_status': 'extracted', 'ocr_text_status': 'no_text',
                    'connector_count': 0, 'unresolved_connector_count': 0,
                    'missing_native_labels': 0, 'missing_ocr_labels': 1,
                },
            }
            with patch.dict(pilot.PAGES, {18: (1, 0)}, clear=True):
                self.assertEqual(pilot.check_page(result, manifest_page, root)['nodes'], 1)
                omitted = copy.deepcopy(result)
                candidate = omitted['nodes'][0]['label_candidates'][0]
                candidate.update({'text': '', 'line_item_ids': [],
                                  'line_bboxes': [], 'status': 'no_lines'})
                omitted['coverage']['missing_native_labels'] = 1
                with self.assertRaisesRegex(ValueError, 'line_inventory'):
                    pilot.check_page(omitted, manifest_page, root)


if __name__ == '__main__':
    unittest.main()
