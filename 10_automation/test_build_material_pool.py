import csv
import json
import tempfile
import unittest
from pathlib import Path

from build_material_pool import build, file_hash, iso_monday, material_id


class MaterialPoolTests(unittest.TestCase):
    def setUp(self):
        self.parent = Path(__file__).resolve().parent
        self.temporary = tempfile.TemporaryDirectory(dir=self.parent, prefix='_test_material_pool_')
        self.root = Path(self.temporary.name).resolve()
        self.master = self.root / '04_prompts/item_prompt_database.csv'
        self.output = self.root / '04_prompts/material_pool'
        self.output.mkdir(parents=True)
        self.registry = self.output / 'series_registry.json'
        self.registry.write_text(json.dumps({'schema_version': 1, 'series': [], 'uses': [],
                                             'manual_note': 'Keep this exact file'}), encoding='utf-8')

    def tearDown(self):
        self.assertEqual(self.root.parent, self.parent)
        self.assertTrue(self.root.name.startswith('_test_material_pool_'))
        self.temporary.cleanup()

    def row(self, week='2026-W41', row_id='P1', **changes):
        return dict({'id': row_id, 'week': week, 'trend_name': 'Light jacket',
                     'clothing_item': 'Ivory jacket', 'color_palette': 'ivory / blue',
                     'fabric': 'cotton', 'fit': 'relaxed', 'styling_rules': 'over tee',
                     'occasion': 'office', 'status': 'draft'}, **changes)

    def write_csv(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8-sig', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=self.row().keys())
            writer.writeheader()
            writer.writerows(rows)

    def source(self, rows, week=None, receipt=True):
        week = week or rows[0]['week']
        path = self.root / '10_automation/runs' / week / 'source_perplexity.csv'
        self.write_csv(path, rows)
        if receipt:
            path.with_name('source_receipt.json').write_text(json.dumps({
                'week': week, 'sha256': file_hash(path), 'rows': len(rows),
                'retrieved_date': '2026-10-08'}), encoding='utf-8')
        return path

    def test_origin_classification_and_master_source_deduplication(self):
        rows = [self.row(), self.row(row_id='P2'), self.row('2026-W36', 'older'),
                self.row(row_id='W41-E001', status='editorial_approved'),
                self.row('2026-W21-test', 'test'), self.row('1', 'demo')]
        self.write_csv(self.master, rows)
        self.source(rows[:2])
        pool, index = build(self.root, '2026-10-15')
        self.assertEqual(4, len(index['entries']))
        self.assertEqual(2, len(index['quarantined_rows']))
        self.assertEqual(2, len(pool['saved_source_candidates_for_review']))
        self.assertEqual(1, len(pool['editorial_expansions_for_review']))
        self.assertEqual(['2026-W40', '2026-W42'], [item['week'] for item in pool['coverage']
                                                  if item['status'] == 'missing_original_csv'])
        original = next(item for item in index['entries'] if item['source_row_id'] == 'P1')
        self.assertEqual(2, len(original['provenance']))
        self.assertFalse(original['external_claims_verified'])
        self.assertEqual('not_checked_for_this_build', pool['weather']['status'])

    def test_comparison_groups_keep_occasions_and_fabric_differences(self):
        rows = [self.row(row_id='P1'),
                self.row(row_id='P2', clothing_item='  IVORY  jacket ', occasion='dinner'),
                self.row(row_id='P3', fabric='linen')]
        self.write_csv(self.master, rows)
        _, index = build(self.root, '2026-10-15')
        self.assertEqual(2, len(index['comparison_groups']))
        shared = next(group for group in index['comparison_groups'] if len(group['material_ids']) == 2)
        self.assertEqual(['dinner', 'office'], shared['occasions'])
        self.assertEqual(3, len(index['entries']))

    def test_iso_cross_year_and_future_old_exclusion(self):
        rows = [self.row('2026-W51', 'old'), self.row('2026-W53', 'current'),
                self.row('2027-W02', 'future')]
        self.write_csv(self.master, rows)
        self.source([rows[1]])
        pool, _ = build(self.root, '2027-01-04')
        self.assertEqual(['2026-W52', '2026-W53', '2027-W01'], pool['window_weeks'])
        self.assertEqual(1, len(pool['saved_source_candidates_for_review']))
        self.assertEqual(1, pool['older_materials_retained'])
        self.assertEqual(1, pool['future_materials_excluded'])
        with self.assertRaises(ValueError):
            iso_monday('2027-W53')
        with self.assertRaises(ValueError):
            iso_monday('2026-W1')

    def test_reorder_rerun_preserves_ids_notes_registry_and_source_bytes(self):
        rows = [self.row(), self.row(row_id='P2')]
        self.write_csv(self.master, rows)
        source = self.source(rows)
        registry_bytes, source_bytes = self.registry.read_bytes(), source.read_bytes()
        _, first = build(self.root, '2026-10-15')
        target = self.output / 'material_index.json'
        first['entries'][0]['editor_notes'] = {'checked': 'manual'}
        target.write_text(json.dumps(first), encoding='utf-8')
        self.write_csv(self.master, list(reversed(rows)))
        master_bytes = self.master.read_bytes()
        _, second = build(self.root, '2026-10-15')
        self.assertEqual([item['material_id'] for item in first['entries']],
                         [item['material_id'] for item in second['entries']])
        self.assertEqual({'checked': 'manual'}, second['entries'][0]['editor_notes'])
        self.assertTrue(all(not item['revisions'] for item in second['entries']))
        self.assertEqual(registry_bytes, self.registry.read_bytes())
        self.assertEqual(source_bytes, source.read_bytes())
        self.assertEqual(master_bytes, self.master.read_bytes())

    def test_content_changes_retain_previous_row_with_same_identity(self):
        self.write_csv(self.master, [self.row()])
        _, first = build(self.root, '2026-10-15')
        self.write_csv(self.master, [self.row(fabric='linen')])
        _, second = build(self.root, '2026-10-16')
        entry = second['entries'][0]
        self.assertEqual(first['entries'][0]['material_id'], entry['material_id'])
        self.assertEqual('cotton', entry['revisions'][0]['row']['fabric'])
        self.assertEqual('linen', entry['row']['fabric'])

    def test_removed_original_retains_provenance_and_receipt_history(self):
        self.write_csv(self.master, [self.row()])
        source = self.source([self.row()])
        _, first = build(self.root, '2026-10-15')
        source.unlink()
        pool, second = build(self.root, '2026-10-16')
        entry = second['entries'][0]
        self.assertEqual('legacy_source_unverified', entry['origin'])
        self.assertEqual('saved_weekly_source', first['entries'][0]['origin'])
        self.assertEqual(2, len(entry['revisions'][0]['provenance']))
        self.assertEqual('matched', second['source_history'][0]['source']['receipt_state'])
        self.assertEqual(0, len(pool['saved_source_candidates_for_review']))
        self.assertEqual(1, len(pool['legacy_candidates_needing_source_check']))

    def test_conflicts_excluded_and_resolved_conflict_snapshot_retained(self):
        self.write_csv(self.master, [self.row(fabric='linen')])
        self.source([self.row()])
        pool, first = build(self.root, '2026-10-15')
        self.assertEqual(0, len(pool['saved_source_candidates_for_review']))
        self.assertEqual(2, len(first['entries'][0]['conflicting_variants']))
        self.write_csv(self.master, [self.row()])
        pool, second = build(self.root, '2026-10-16')
        self.assertEqual(1, len(pool['saved_source_candidates_for_review']))
        self.assertEqual(2, len(second['entries'][0]['revisions'][0]['conflicting_variants']))

    def test_missing_receipt_distinct_from_null_empty_or_mismatched_receipt(self):
        self.write_csv(self.master, [self.row()])
        source = self.source([self.row()], receipt=False)
        pool, first = build(self.root, '2026-10-15')
        self.assertEqual('missing', first['sources'][0]['receipt_state'])
        self.assertIsNone(first['sources'][0]['retrieved_date'])
        self.assertEqual(1, len(pool['saved_source_candidates_for_review']))
        for bad in (None, {}, {'sha256': 'bad', 'rows': 1, 'week': '2026-W41'},
                    {'sha256': file_hash(source), 'rows': 2, 'week': '2026-W41'}):
            with self.subTest(receipt=bad):
                source.with_name('source_receipt.json').write_text(json.dumps(bad), encoding='utf-8')
                pool, index = build(self.root, '2026-10-15')
                self.assertEqual('mismatch', index['sources'][0]['receipt_state'])
                self.assertIsNotNone(index['sources'][0]['receipt_path'])
                self.assertEqual(0, len(pool['saved_source_candidates_for_review']))

    def test_removed_row_retained_as_history_not_current_candidate(self):
        self.write_csv(self.master, [self.row(), self.row(row_id='P2')])
        build(self.root, '2026-10-15')
        self.write_csv(self.master, [self.row(row_id='P2')])
        pool, index = build(self.root, '2026-10-16')
        entry = next(item for item in index['entries'] if item['source_row_id'] == 'P1')
        self.assertEqual('absent_from_current_inputs', entry['availability'])
        self.assertNotIn(material_id('2026-W41', 'P1'),
                         pool['legacy_candidates_needing_source_check'])

    def test_bad_input_does_not_overwrite_existing_outputs(self):
        self.write_csv(self.master, [self.row()])
        build(self.root, '2026-10-15')
        before = {path: path.read_bytes() for path in self.output.iterdir()}
        self.write_csv(self.master, [self.row(), self.row(fabric='linen')])
        with self.assertRaisesRegex(ValueError, 'conflicting duplicate'):
            build(self.root, '2026-10-16')
        self.assertTrue(all(path.read_bytes() == content for path, content in before.items()))

    def test_source_folder_week_mismatch_fails_before_output(self):
        self.write_csv(self.master, [self.row()])
        self.source([self.row('2026-W40')], week='2026-W41')
        with self.assertRaisesRegex(ValueError, 'differs from source folder'):
            build(self.root, '2026-10-15')
        self.assertFalse((self.output / 'material_index.json').exists())

    def test_unknown_series_reference_and_backdating_fail_closed(self):
        self.write_csv(self.master, [self.row()])
        build(self.root, '2026-10-15')
        with self.assertRaisesRegex(ValueError, 'backdate'):
            build(self.root, '2026-10-14')
        self.registry.write_text(json.dumps({'schema_version': 1, 'series': [
            {'series_id': 'new', 'source_material_ids': ['missing_material']}]}), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Unknown material reference'):
            build(self.root, '2026-10-16')


if __name__ == '__main__':
    unittest.main()
