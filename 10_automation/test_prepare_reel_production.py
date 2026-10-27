import csv
import json
import shutil
import uuid
import unittest
from pathlib import Path
from prepare_reel_production import build


class ProductionTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent / ('_test_reel_production_' + uuid.uuid4().hex)
        self.root.mkdir()
        self.run = self.root / '2026-W37'
        self.run.mkdir()
        (self.root / '02_brand').mkdir()
        (self.root / 'ref.png').write_bytes(b'reference fixture')
        self.looks = [dict(week_id='2026-W37', carousel_id=f't{i}', model_profile_id=f'M0{i}',
            look_id=f't{i}-L{j}', look_order=str(j), theme_name='theme', visual_proof='detail',
            clothing_item='shirt', dressing_decision='layering') for i in range(1,6) for j in (1,2)]
        self.write(self.run / 'weekly_look_plan.csv', self.looks)
        self.write(self.run / 'weekly_content_packet.csv', [dict(carousel_id=f't{i}',model_profile_id=f'M0{i}') for i in range(1,6)])
        self.write(self.root / '02_brand/mira_reference_images.csv', [dict(model_profile_id=f'M0{i}', status='approved', reference_face_path='ref.png',reference_full_path='ref.png') for i in range(1,6)])

    def tearDown(self):
        self.assertEqual(self.root.resolve().parent, Path(__file__).resolve().parent)
        self.assertTrue(self.root.name.startswith('_test_reel_production_'))
        shutil.rmtree(self.root)

    def write(self, path, data):
        with path.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=data[0].keys())
            w.writeheader()
            w.writerows(data)

    def test_shape_and_counterbalance(self):
        manifest = json.loads(build(self.root,self.run).read_text())
        self.assertEqual(5,len(manifest['reels']))
        self.assertTrue(all(len(r['views']) == 4 for r in manifest['reels']))
        self.assertTrue(all(r['storyboard'] == [] for r in manifest['reels']))
        self.assertTrue(all(r['visual_theme'] is None for r in manifest['reels']))
        self.assertTrue(all(r['delivered_video_text'] == 'none' for r in manifest['reels']))
        self.assertTrue(all(r['instagram_editor_text_note'] is None for r in manifest['reels']))
        with (self.run/'reels/four_week_trial.csv').open(encoding='utf-8-sig') as f:
            schedule = list(csv.DictReader(f))
        self.assertEqual(20,len(schedule))
        for model in ['M01','M02','M03','M04','M05']:
            self.assertEqual(['A','A','B','B'],sorted(r['format_variant'] for r in schedule if r['model_profile_id']==model))

    def test_rerun_preserves_review_and_schedule(self):
        path = build(self.root,self.run)
        data = json.loads(path.read_text())
        data['reels'][0]['qa']['user_approval']='accepted'
        path.write_text(json.dumps(data))
        schedule = self.run/'reels/four_week_trial.csv'
        schedule.write_text('manually scheduled')
        build(self.root,self.run)
        self.assertEqual('accepted',json.loads(path.read_text())['reels'][0]['qa']['user_approval'])
        self.assertEqual('manually scheduled',schedule.read_text())

    def test_cross_model_pair_rejected(self):
        self.looks[0]['model_profile_id']='M02'
        self.write(self.run/'weekly_look_plan.csv',self.looks)
        with self.assertRaises(ValueError): build(self.root,self.run)
        self.assertFalse((self.run/'reels/production_manifest.json').exists())

    def test_changed_look_lock_rejected(self):
        path = build(self.root,self.run)
        before = path.read_bytes()
        self.looks[0]['look_id']='replacement'
        self.write(self.run/'weekly_look_plan.csv',self.looks)
        with self.assertRaises(ValueError): build(self.root,self.run)
        self.assertEqual(before,path.read_bytes())

    def test_missing_reference_rejected(self):
        (self.root/'ref.png').unlink()
        with self.assertRaises(ValueError): build(self.root,self.run)


if __name__ == '__main__':
    unittest.main()
