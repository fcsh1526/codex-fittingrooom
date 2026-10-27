"""Link the two-look candidate and exact-source proof crops; never assign acceptance."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
reels = run / 'reels'
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def relative(path):
    return path.relative_to(root).as_posix()

b_source = reels / 'videos/M01_B_L02_fixed_full_v1_01.mp4'
b_still = run / 'generated_images/2026-W37-004/looks/2026-W37-004-L02/reel/2026-W37-004-L02_M01_S02_full_start_candidate_v1.png'
b_record = dict(reel_id='2026-W37-M01-reel', look_id='2026-W37-004-L02', trial_id='M01_B_L02_fixed_full_v1_01', date='2026-10-01', status='decoded_sampled_review_complete_continuous_qa_pending', source_post_url='https://grok.com/imagine/post/c8638cbf-890f-4da7-8419-5bdc3daf0ef6?conversation=fad61295-df9b-401e-a17b-64172f9360cb', input_still=relative(b_still), still_user_approval='可以，沿用這張', input_role='Single First frame, no Last frame', identity_reference='No separate saved character reference selected; approved near-frontal outfit still is identity input.', prompt_path=relative(reels / 'prompts/M01_B_L02_motion_v1.md'), ui_settings=dict(resolution='720p', duration='6s', audio='off (checkbox0 confirmed)', model='unnamed in visible UI'), video=dict(output_path=relative(b_source), sha256=hashlib.sha256(b_source.read_bytes()).hexdigest(), resolution=[720,1264], fps=24, duration_seconds=145/24), qa=dict(decode_scan=read(reels / 'qa/M01_B_L02_fixed_full_v1_01/full_scan.json'), sample_sheet=relative(reels / 'qa/M01_B_L02_fixed_full_v1_01/checkpoints.jpg'), sampled_review='Nine timepoints inspected; black mid-calf skirt, cream square-toe T intersections and full shoes readable. Weight shift and small foot plant stay in frame; window, doorway and paving show no obvious sampled morph. Face changes pose slightly. Continuous playback remains user review.', usable_seconds=None, continuous_watch_done=False, user_visual_approval=None), time=dict(active_minutes=None, generation_wait_minutes=None), upload=dict(status='assistant_upload_success', method='AX Upload media button + filechooser/setFiles; exact filename and First-frame role verified'))
write(reels / 'M01_B_L02_fixed_full_v1_01.json', b_record)
still_record = b_still.parent / 'S02_full_start_generation_v1.json'
data = read(still_record)
data['grok_submitted'] = True
data['motion_record'] = relative(reels / 'M01_B_L02_fixed_full_v1_01.json')
write(still_record, data)

proofs = []
for index, shot in [(1, 'S01'), (2, 'S02')]:
    look_id = f'2026-W37-004-L0{index}'
    folder = run / f'generated_images/2026-W37-004/looks/{look_id}/reel'
    source = folder / f'{look_id}_M01_{shot}_full_start_candidate_v1.png'
    target = folder / f'{look_id}_M01_shoe_proof_crop_v1.png'
    box = [245,872,695,1672]
    with Image.open(source) as im:
        im.crop(tuple(box)).save(target)
    proof = dict(look_id=look_id, role='proof', source_path=relative(target), source_type='exact_crop_from_approved_native_vertical_still', parent_path=relative(source), parent_user_approval='可以，沿用這張', crop_xyxy=box, pixels=[450,800], resampling='none; no generative edit or upscale', framing_review='pending', clarity_review='pending', status='crop_review_pending', motion_use='Independent styling-proof asset; not inserted as another hard cut or used as a face-reveal First frame.')
    write(folder / 'shoe_proof_crop_review_v1.json', proof)
    proofs.append(proof)

output_record = reels / 'M01_two_looks_review_v1_01.json'
candidate = read(output_record)
candidate['qa']['technical_scan'] = read(reels / 'qa/M01_two_looks_review_v1_01/full_scan.json')
candidate['qa']['sampled_review'] = 'Output start, during step, cut-adjacent frames83/84, later weight shift and final frame inspected. Full hair and shoes retained. Subject centers and eye/shoe heights approximately matched; one visible intentional outfit cut remains. No obvious sampled face/wardrobe jump or background morph; normal-speed user review pending.'
candidate['qa']['sample_sheet'] = relative(reels / 'qa/M01_two_looks_review_v1_01/checkpoints.jpg')
write(output_record, candidate)
manifest_path = reels / 'production_manifest.json'
manifest = read(manifest_path)
item = next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
item['status'] = 'two_look_clean_review_pending_user_approval'
item['output_path'] = candidate['output_path']
item['output_record_path'] = relative(output_record)
item['qa'] = dict(status='technical_and_sampled_review_complete_user_full_playback_pending', continuous_watch_done=False, user_approval=None)
item['generation']['trials'] = [t for t in item['generation']['trials'] if t['trial_id']!='M01_B_L02_fixed_full_v1_01']
item['generation']['trials'].append(dict(trial_id=b_record['trial_id'], output_path=relative(b_source), source_url=b_record['source_post_url'], record_path=relative(reels / 'M01_B_L02_fixed_full_v1_01.json'), qa=b_record['status'], motion_result=None))
for index, (shot, source) in enumerate(zip(item['storyboard'], candidate['sources'])):
    shot.update(source_still_status='user_visual_approved_for_motion_2026-10-01', source_video=source['path'], source_start_frame=source['start_frame'], source_end_frame_exclusive=source['end_frame_exclusive'], framing_filter=source['framing'], dynamic_status='selected_interval_pending_user_continuous_review')
for proof in proofs:
    view = next(v for v in item['views'] if v['look_id']==proof['look_id'] and v['role']=='proof')
    view.update(source_path=proof['source_path'], source_type=proof['source_type'], approval='approved_parent_crop_review_pending', framing_review='pending', clarity_review='pending')
write(manifest_path, manifest)
print('M01 candidate linked; proof crops require visual clarity review; final approval remains pending.')
