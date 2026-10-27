import json
from pathlib import Path

root = Path(__file__).resolve().parents[5]
reels = root / '10_automation/runs/2026-W37/reels'
record_path = reels / 'M04_two_looks_review_v1_01.json'
record = json.loads(record_path.read_text(encoding='utf-8-sig'))
record['status'] = 'user_visual_approved_clean_picture_track'
record['qa'].update(user_approval='可以，沿用這版', approval_date='2026-10-01',
                    approval_scope='User accepted the full eight-second preview for two-look cut, camera retreat and background. Music, caption and publication are separate.',
                    continuous_watch_done=True, continuous_review_basis='User reply to explicit full-playback question; no claim of assistant full-playback observation.')
record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
manifest_path = reels / 'production_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
item = next(r for r in manifest['reels'] if r['model_profile_id'] == 'M04')
item['status'] = 'user_visual_approved_clean_picture_track_music_publication_pending'
item['qa'].update(status='technical_decode_and_user_visual_approved', user_approval='可以，沿用這版',
                   approval_date='2026-10-01',continuous_watch_done=True,continuous_review_reviewer='user')
item['music']['clean_master'] = item['output_path']
item['caption_path'] = '10_automation/runs/2026-W37/reels/M04_instagram_caption_draft.md'
item['cover_candidate_path'] = '10_automation/runs/2026-W37/generated_images/2026-W37-003/looks/2026-W37-003-L01/reel/2026-W37-003-L01_M04_S01_storyboard_v1_start_candidate.png'
for shot in item['storyboard']:
    shot['qa'] = 'selected_interval_user_visual_approved_2026-10-01'
for view in item['views']:
    if view['role'] == 'proof' and view['look_id'].endswith('L01'):
        view['approval'] = 'selected_video_interval_user_visual_approved_2026-10-01'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for filename,start,end in [('M04_A_L01_upload_trial_01.json',0,90),('M04_B_L02_motion_v1_01.json',6,108)]:
    trial_path = reels / filename
    trial = json.loads(trial_path.read_text(encoding='utf-8-sig'))
    trial['qa']['selected_interval_approval'] = dict(start_frame=start,end_frame_exclusive=end,approval='可以，沿用這版',date='2026-10-01',source='User accepted assembled eight-second preview; whole source outside selected interval remains unapproved.')
    trial_path.write_text(json.dumps(trial,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('M04 picture approval and selected source intervals recorded; no publication.')
