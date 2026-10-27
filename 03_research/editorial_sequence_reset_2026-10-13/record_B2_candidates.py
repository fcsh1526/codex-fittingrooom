from pathlib import Path
import csv
import hashlib
import json
import shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
JOB = ROOT / '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1'
GENERATED = Path('C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

names = [
    ('v1', 'M03_L02_B2_departure_candidate_v1_material_failed.png', 'exec-b556566b-cd22-404a-98d6-efdfc3428407.png', 'B2_prompt_v1.txt', 'material_pattern_deviation'),
    ('v2', 'M03_L02_B2_departure_candidate_v2_material_failed.png', 'exec-ebb21a34-948e-437e-b817-7ccf0b061c1f.png', 'B2_material_correction_v2.txt', 'single_material_edit_failed'),
    ('v3', 'M03_L02_B2_departure_candidate_v3_material_failed.png', 'exec-37c98768-c3d0-4fd6-a15e-b11cd2e80e73.png', 'B2_clean_inputs_replan_v3.txt', 'wardrobe_reference_rebuild_pattern_persists'),
    ('v4', 'M03_L02_B2_departure_candidate_v4_clean.png', 'exec-9733e581-c0a5-4f74-8e81-638aebf5c98f.png', 'B2_identity_only_replan_v4.txt', 'assistant_static_candidate_user_visual_approval_pending'),
]
rows = []
for version, name, original, prompt, status in names:
    path = JOB / name
    if not path.exists():
        shutil.copyfile(GENERATED / original, path)
    shutil.copyfile(BASE / prompt, JOB / prompt)
    rows.append({'version': version, 'file': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'native_pixels': list(Image.open(path).size), 'original_generated_name': original, 'prompt': (JOB / prompt).relative_to(ROOT).as_posix(), 'status': status, 'framing_transform': 'none'})

plan = read(BASE / 'B2_reference_plan.json')
receipt = {
    'date': '2026-10-13', 'look_id': '2026-W41-004-L02', 'model': 'M03', 'shot': 'B2',
    'tool': 'built-in image_gen', 'status': 'v4_candidate_user_visual_approval_pending',
    'generation_count': 4, 'targeted_material_edits': 1, 'input_replans': 2,
    'attempt_accounting': 'Initial B2+one single-material correction retained ornamental tee pattern. Rebuild dropping scene pixels but retaining weekly wardrobe still retained pattern. Final fresh rebuild uses only approved identity anchors and written wardrobe/scene. All four calls preserved; not a one-retry sustainable production success.',
    'candidates': rows, 'user_approval': None, 'grok_uploaded': False, 'video_generated': False,
    'reference_plan': plan,
    'references_v1': [p['path'] for p in plan['references']],
    'references_v2': [rows[0]['file'], plan['references'][2]['path']],
    'references_v3': [p['path'] for p in plan['references'][:3]],
    'references_v4': [p['path'] for p in plan['references'][:2]],
    'assistant_static_review': 'Clean v4 recognizable M03 and ordinary body proportions. Navy open blazer, one-fold cuffs, plain heather-gray cotton tee, cream straight trousers, black low-heel loafers, black shoulder bag and studs readable. Same lunch-window/bench/gray-wall/daylight logic but recreated geometry is not a match-keyframe. Full head and front shoe visible; rear shoe partly occluded naturally. Light grounded on tiled floor. Actual pose is more near-frontal than planned lateral departure, one hand holds shoulder strap instead of both arms relaxed; wider black bag differs from previous exact weekly photo. These deviations remain explicit for user review and subsequent motion planning.',
    'proof_view_generated': False, 'formal_full_proof_carousel_complete': False,
    'active_minutes': None, 'generation_wait_minutes': None,
    'production_note': 'Pattern repetition and four calls are a repeatability issue. Fresh identity-only strategy preserves written look but does not certify pixel-exact weekly garment/accessory construction. User approval required; no B1 derivative or Grok before approval.'
}
write(BASE / 'B2_still_receipt.json', receipt)
write(JOB / 'B2_generation_receipt.json', receipt)
plan.update(status=receipt['status'], generated_candidate=rows[-1]['file'], generation_count=4, new_still_approved=False, grok_uploaded=False)
write(BASE / 'B2_reference_plan.json', plan)
fields = ['file', 'model_consistency', 'body_proportion_consistency', 'reader_relatability', 'outfit_clarity', 'ai_realism', 'commerce_value', 'scene_lighting_integration', 'outfit_continuity', 'expression_liveliness', 'pose_variation', 'canva_frame_fit', 'publishable', 'status', 'notes']
with (JOB / 'review_sheet.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({'file': row['file'], 'publishable': 'pending' if row['version']=='v4' else 'no', 'status': row['status'], 'notes': receipt['assistant_static_review'] if row['version']=='v4' else 'Tee ornamental pattern differs from plain cotton wardrobe; not sent to Grok.'})
story = read(BASE / 'storyboard_candidate.json')
story.update(status='first_look_direction_accepted_B2_v4_still_pending_visual_approval', b2_still_generation_count=4, b2_candidate=rows[-1], next_action='User visual approval of exact B2v4; then derive B1 seated with this L02 lock plus clean A2 scene/framing reference. No Grok before each exact still approval.')
write(BASE / 'storyboard_candidate.json', story)
update = '''## M03午休小出走：第二套全身v4待核准 — 2026-10-13

第一套方向已獲「這個方向可以」接受，續作同一午休片段。第二套B2全身候選共4次靜態生成：首版及一次材質修正、一次保留服裝參照重建仍出花紋；v4只用核准人物雙參照＋文字服裝／場景，已回到素面灰棉T。新圖待使用者精確視覺核准，不能推定沿用。實際為較正面的短步起點、一手扶黑包帶；黑包輪廓比舊週圖寬、場景重新建立，與原側向／雙手放鬆計畫不完全一致。檔案：`10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1/M03_L02_B2_departure_candidate_v4_clean.png`；所有候選／提示詞／雜湊／限制見同夾`B2_generation_receipt.json`與研究夾`B2_still_receipt.json`。尚未做B1坐姿、未上傳Grok；核准B2後才用其第二套鎖定圖製作B1。四次耗費列入研究，未宣稱量產成功。無舊交付影片、Drive、IG或GitHub寫入。下方為歷史進度。

'''
status = ROOT / 'CURRENT_STATUS.md'
head, rest = status.read_text(encoding='utf-8-sig').split('\n', 1)
status.write_text(head + '\n\n' + update + rest.lstrip('\n'), encoding='utf-8')
readme = BASE / 'README.md'
readme.write_text(update + readme.read_text(encoding='utf-8-sig'), encoding='utf-8')
report = BASE / 'FIRST_LOOK_REVIEW.md'
report.write_text('> 更新2026-10-13：使用者回覆「這個方向可以」，接受此觀看方向並續作第二套。正式整支影片仍未完成，完整正常播放自述與成效仍留空。核准範圍見`first_look_direction_acceptance_2026-10-13.json`。\n\n' + report.read_text(encoding='utf-8-sig'), encoding='utf-8')
print('Saved all4 B2 candidates, exact prompts and hashes. Clean v4 awaits visual approval; no B1/Grok submitted.')
