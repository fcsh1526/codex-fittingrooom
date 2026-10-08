import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / '10_automation/runs/2026-W41'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def describe(path):
    with Image.open(path) as image:
        size = list(image.size)
    return {'file': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'actual_pixels': size}

manifest_path = RUN / 'reels/production_manifest.json'
manifest = read(manifest_path)
entry = next(x for x in manifest['reels'] if x['model_profile_id'] == 'M02')
pair = []
for number, version, prompt, wait in [(1, 4, 'hero_production_prompt_restart_v4.txt', 110.6), (2, 3, 'hero_production_prompt_restart_v3.txt', 55.9)]:
    look = f'2026-W41-003-L{number:02d}'
    folder = RUN / f'generated_images/2026-W41-003/looks/{look}/reel'
    file = folder / f'{look}_M02_reel_candidate_A_v{version}.png'
    data = describe(file)
    data.update(look_id=look, model='M02', week='2026-W41', generator='built_in_image_gen', prompt=prompt,
                references=['02_brand/reference_models/M02_start_v3_face.png', '02_brand/reference_models/M02_start_v3_full.png'],
                tool_wall_seconds=wait, active_minutes=None, status='static_review_pass_pending_user_visual_approval',
                user_approval=None, dynamic_QA=None)
    data['static_review'] = {
        'identity': 'Recognizable v3 face and pinned-back hair, healthy proportions; separate user visual check pending.',
        'wardrobe': 'Plain cocoa five-pocket straight-leg denim, black belt/shoes/small shoulder bag; L01 cream tee with open ivory light cropped jacket; L02 white short-sleeve point-collar shirt. Natural seam/cloth tonal variation, no apparent decorative motifs in selected sources.',
        'framing': 'Generated directly in portrait 9:16 composition, actual941x1672; full hair and both shoes visible, no resize/crop applied.',
        'scene': 'Shared left daylight and greige cafe walkway. Independent source renders have small face/pose/door/bench geometry differences; not identical matched pixels.',
        'animation_start': 'Both feet grounded, one slightly ahead; arms rest beside hips. Use one modest forward step and settle, no cloth handling.',
        'continuity': 'Black shoulder bag stays at image-left in both selected sources. Approximate subject scale and shoe placement similar; final generated join still requires review.',
        'limitations': 'Static inspection only; no video generation, dynamic pass, proof approval or complete delivery implied.'
    }
    rejected = []
    for previous in folder.glob(f'{look}_M02_reel_candidate_A*.png'):
        if previous == file:
            continue
        old = describe(previous)
        old.update(status='rejected_not_for_animation', reason='Decorative-looking trouser texture and/or failed pair continuity; targeted texture edit did not resolve. Originals preserved.')
        rejected.append(old)
    data['rejected_prior_versions'] = rejected
    receipt_path = folder / f'generation_receipt_v{version}.json'
    if receipt_path.exists():
        raise SystemExit('Already checkpointed; do not overwrite.')
    write(receipt_path, data)
    pair.append(data)
    sheet = folder / 'review_sheet.csv'
    with sheet.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    row = rows[0]
    row['candidate_file'] = file.name
    for key in ['model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity','ai_realism','scene_lighting_integration','outfit_continuity','expression_liveliness','pose_variation','canva_frame_fit','commerce_value']:
        row[key] = '4'
    row.update(publishable='yes', status='static_pass_pending_user_visual_approval', notes='Static scores only. Exact selected version has plain denim; earlier texture failures preserved and rejected. Native portrait, full hair/shoes. Video and user approval still pending; small source background differences require join review.')
    with sheet.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    slot = next(x for x in entry['views'] if x['look_id'] == look and x['role'] == 'full')
    slot.update(source_path=data['file'], source_type='native_reel_candidate_still', approval=None,
                framing_review='assistant_static_pass_pending_user', clarity_review='assistant_static_pass_pending_user')
entry['status'] = 'two_full_first_frame_candidates_pending_user_visual_approval'
entry['starting_source_review'] = 'L01 v4 + L02 v3 only. Earlier decorative texture versions rejected. Both bags image-left; native full person. Modest independent cafe geometry differences require generated join review.'
entry['qa']['status'] = 'no_video_yet'
write(manifest_path, manifest)
paired_path = RUN / 'reels/M02_full_pair_static_review_2026-10-08.json'
write(paired_path, {'model': 'M02', 'week': '2026-W41', 'files': pair, 'user_approval': None,
                    'production_rule': 'Do not animate either source until separate user visual acceptance of the exact selected pair.',
                    'generation_count': 7, 'targeted_edits': 2, 'identity_anchor_only_restarts': 2, 'continuity_reconstruction': 1,
                    'lesson': 'Production-image continuity references propagated ornamental trouser texture; one targeted edit of each affected chain failed. Rebuild from approved identity anchors only, record rejected versions, and recheck scene/scale instead of carrying rejected surfaces forward.'})
request_path = ROOT / '10_automation/production_requests/2026-10-08_next_five_reels.json'
request = read(request_path)
slot = next(x for x in request['slots'] if x['model'] == 'M02')
slot['status'] = entry['status']
slot['first_frame_candidates'] = [x['file'] for x in pair]
write(request_path, request)
pub_path = RUN / 'publishing_structure.md'
pub = pub_path.read_text(encoding='utf-8-sig')
pub = pub.replace('M02–M04已準備獨立Reel/Carousel素材工作單，尚未生成新素材。', 'M02已完成兩張全身候選：第一套v4、第二套v3，待使用者分別核准；先前褲面異常版本保留且不送Grok。M03–M04已準備独立Reel/Carousel工作單，尚未生成新素材。', 1)
pub_path.write_text(pub, encoding='utf-8')
status_path = ROOT / 'CURRENT_STATUS.md'
status = status_path.read_text(encoding='utf-8-sig')
new = '## W41 M02 plain-denim full pair prepared; still approval pending — 2026-10-08\n\nSelected W41-003 L01 v4 (cream tee/open ivory cropped jacket) and L02 v3 (white short-sleeve point-collar shirt) are saved with plain cocoa straight-leg five-pocket jeans and black shoes/belt/bag. Both bags are image-left; full hair/shoes and native941×1672 portrait framing pass assistant static inspection. Reference-based scene copying propagated decorative trouser texture; one targeted edit of each affected chain failed. Rejected source versions are preserved, then the selected sources were rebuilt from approved M02 v3 face/full anchors only. Seven generation/edit calls total, including two targeted edits; no animation yet. Independent cafe source geometry and pose differ modestly, so generated join review remains required. Exact paths/hashes, prompts, reviews and failures are recorded in `10_automation/runs/2026-W41/reels/M02_full_pair_static_review_2026-10-08.json`. New pair awaits user visual approval; proof and Carousel assets remain outstanding. M01 v2 remains accepted, M05 candidate/proof approvals pending. No W41 upload/publication or W37 replacement.\n\n'
status_path.write_text(status.replace('# Current Status - Mira AI Fashion Creator\n\n', '# Current Status - Mira AI Fashion Creator\n\n' + new, 1), encoding='utf-8')
print('M02 L01 v4 / L02 v3 recorded as candidates, user approval pending; no video generated.')
