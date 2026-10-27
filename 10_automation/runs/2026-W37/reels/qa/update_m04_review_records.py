import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
candidate = run / 'generated_images/2026-W37-003/looks/2026-W37-003-L02/reel/2026-W37-003-L02_M04_S03_medium_start_candidate_v1.png'
with Image.open(candidate) as im:
    pixels = list(im.size)
record = {
    'look_id': '2026-W37-003-L02', 'model_profile_id': 'M04',
    'date': '2026-10-01', 'status': 'candidate_pending_user_visual_approval',
    'provider': 'built_in_imagegen', 'source_path': str(candidate.relative_to(root)).replace('\\', '/'),
    'pixels': pixels, 'sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
    'prompt_path': '10_automation/runs/2026-W37/reels/prompts/M04_B_L02_medium_start_v1.md',
    'references': [
        'approved L02 full still (exact wardrobe and scene)',
        '02_brand/reference_models/M04_start_v3_face.png (identity)',
        '02_brand/reference_models/M04_start_v3_full.png (identity/proportion)',
        'reels/qa/M04_A_L01_upload_trial_01/checkpoint_5_3.750s.png (framing only)'],
    'assistant_still_review': {
        'framing': 'Native vertical head-to-knees; eyes near 13% height; face and shoulder scale close to A 3.75s sample; exact moving cut still requires validation.',
        'wardrobe': 'Ivory sleeveless standing collar, concealed placket, tucked navy waistband and straight satin skirt remain visible; black shoulder bag and silver studs present.',
        'scene': 'Left daylight, pale wall, wooden displays preserved in scene logic; not certified geometrically compatible as Last frame with separate full still.',
        'identity': 'No obvious departure from approved L02 still; user confirmation pending.',
        'text': 'none'},
    'user_visual_approval': None, 'grok_submitted': False,
    'planned_motion': 'One short smooth camera retreat; ordinary weight shift; no independently generated Last frame.'}
candidate.with_name('S03_medium_start_generation_v1.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

trial_path = run / 'reels/M04_A_L01_upload_trial_01.json'
trial = json.loads(trial_path.read_text(encoding='utf-8-sig'))
trial['status'] = 'technical_decode_complete_sampled_visual_review_continuous_qa_pending'
trial['qa'].update({
    'decode_scan': 'reels/qa/M04_A_L01_upload_trial_01/decode_scan.json',
    'sample_sheet': 'reels/qa/M04_A_L01_upload_trial_01/checkpoints.jpg',
    'decoded_frames': 145, 'black_candidate_frames': [], 'near_identical_frame_pairs': [],
    'sampled_visual_review': 'Nine checkpoints from 0 to 6s inspected. Face and navy jacket/ivory dress show no obvious sampled jump; left window and right shelves retain coherent scene layout. Shoes leave frame as she approaches; ordinary perspective movement must still be assessed in continuous playback.',
    'provisional_cut_time_seconds': 3.75,
    'usable_seconds': None, 'dynamic_acceptance': False,
    'continuous_watch_done': False,
    'aspect_ratio_note': '720x1264 source, not exact 9:16. Do not stretch; final export framing still unresolved.',
    'audio_note': 'AAC stream present; remove generated audio from clean assembly.'})
trial_path.write_text(json.dumps(trial, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

manifest_path = run / 'reels/production_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
item = next(item for item in manifest['reels'] if item['model_profile_id'] == 'M04')
view = next(v for v in item['views'] if v['look_id'].endswith('L02') and v['role'] == 'proof')
view.update(source_path=record['source_path'], source_type='native_vertical_still_candidate', approval='pending_user_visual_approval', framing_review=record['assistant_still_review']['framing'], clarity_review=record['assistant_still_review']['wardrobe'])
item['status'] = 'L01_sampled_review_done_continuous_qa_pending_L02_medium_user_approval_pending'
item['generation']['trials'][-1]['qa'] = trial['status']
item['generation']['settings'] = 'L01 upload trial: 6.041667s, 720x1264, 24fps, AAC audio stream present. Submitted prompt, UI audio setting and saved character selection unknown.'
item['storyboard'][0]['plan'] = 'Observed upload trial: full-person approach to near-knee framing by 3.75s; actual submitted prompt/camera intent unknown. Provisional source cut only, not accepted.'
item['storyboard'][1]['source_still_status'] = 'L02_full_user_approved; medium_start_candidate_generated_2026-10-01_pending_user_approval'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'candidate': record['source_path'], 'pixels': pixels, 'sha256': record['sha256'], 'records_updated': True}))
