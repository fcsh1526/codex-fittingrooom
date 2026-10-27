from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
JOB = ROOT / '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

receipt = read(BASE / 'B2_still_receipt.json')
candidate = receipt['candidates'][-1]
assert hashlib.sha256((ROOT / candidate['file']).read_bytes()).hexdigest() == candidate['sha256']
approval = {'date': '2026-10-13', 'user_quote': '可以，沿用最後這張', 'question_context': 'Explicit answer to latest B2v4 full-person face/navy blazer/plain gray tee/cream trousers/one hand on black shoulder-bag question.', 'file': candidate['file'], 'sha256': candidate['sha256'], 'scope': 'Exact B2v4 still and its L02 wardrobe/bag as scene lock only. No B1 still, motion or whole-film approval.'}
write(BASE / 'B2_user_approval_2026-10-13.json', approval)
write(JOB / 'B2_user_approval_2026-10-13.json', approval)
receipt.update(status='v4_user_visual_approved', user_approval=approval)
receipt['candidates'][-1]['status'] = 'user_visual_approved'
write(BASE / 'B2_still_receipt.json', receipt)
write(JOB / 'B2_generation_receipt.json', receipt)
sheet = JOB / 'review_sheet.csv'
with sheet.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields, rows = reader.fieldnames, list(reader)
for row in rows:
    if row['file'] == candidate['file']:
        row['status'] = 'user_visual_approved'
        row['notes'] += ' User approved exact v4 incl. bag-holding pose; publishable production score not inferred.'
with sheet.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
plan = read(BASE / 'B2_reference_plan.json')
plan.update(status='v4_user_visual_approved', new_still_approved=True, user_approval=approval)
write(BASE / 'B2_reference_plan.json', plan)

prompt = '''Create one native vertical 9:16 seated styling-proof photograph for the next moment in an approachable lunch-break fashion story: a lightweight blazer over a cotton tee with straight trousers.

Image 1 locks the approved second outfit and black shoulder bag. Image 2 locks the seated framing, slight forward lean, crossed-leg pose, hand resting positions, window, chunky wooden bench, gray wall and left daylight from the preceding shot; preserve its face and waist positions for a gentle cut. Images 3 and 4 anchor the same woman's identity and ordinary proportions, mid 30s look, well-maintained.

Replace all first-outfit clothes in Image 2 with Image 1's open navy single-breasted blazer, cuffs folded once, plain light-gray cotton crewneck tee tucked into cream high-waisted straight trousers, small silver studs and the same black shoulder bag on image-right. Keep the bag supported at her hip; hands simply rest by knee and bench without gripping or adjusting clothes. Preserve the smooth plain cotton surface and natural folds.

Match the head-through-knees view and seat contact, relaxed attentive expression, brown wavy hair, near-frontal readable face. Use a full-frame mirrorless, level seated-chest-height 50mm view, natural skin and coherent left daylight. One person; no text, logos, ornamental patterns or new scene props.'''
motion = '''Use the selected Mira M03 v3 identity reference. Animate only the exact approved full-person First frame in the second outfit: open navy blazer, plain light-gray crewneck cotton tee, cream straight trousers, black low-heel loafers and black shoulder bag. With the camera completely fixed, she completes one small natural step diagonally toward image-right, then settles without a new pose or turn. Keep her near-frontal recognizable face and complete head and shoes inside the frame. The hand already supporting the black bag strap stays gently in place; the other arm swings only slightly. Normal everyday movement, no slow-motion styling or change of speed. Preserve face, hair, clothing cuts/colors/cuffs, bag, shoe form and the window, bench, wall and tiled floor. No camera move, zoom, sit-down action, outfit change, added text or audio.'''
for name, text in [('B1_prompt_v1.txt', prompt), ('B2_motion_prompt_v1.txt', motion)]:
    (BASE / name).write_text(text + '\n', encoding='utf-8')
    (JOB / name).write_text(text + '\n', encoding='utf-8')
refs = [candidate['file'], '03_research/editorial_sequence_reset_2026-10-13/A2_motion_attempt_01/qa/frame_090.png', '02_brand/reference_models/M03_start_v3_face.png', '02_brand/reference_models/M03_start_v3_full.png']
write(BASE / 'B1_reference_plan.json', {'date': '2026-10-13', 'look_id': '2026-W41-004-L02', 'shot': 'B1', 'status': 'planned_not_generated', 'prompt': 'B1_prompt_v1.txt', 'references': [{'path': p, 'sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()} for p in refs], 'scene_frame_note': 'A2 source frame90 at3.75s within retained0–4s interval. Framing/pose authority only, not L01 wardrobe authority; not an exact4s endpoint.', 'user_approval': None, 'grok_uploaded': False})
story = read(BASE / 'storyboard_candidate.json')
story.update(status='B2_v4_approved_B1_still_next_B2_motion_authorized', b2_approval=approval, next_action='Generate B1 seated exact L02 wardrobe with A2 late framing; user approval before its Grok submission. Independently animate approved B2v4 once using First frame and saved identity; inspect actual step, bag hand and background.')
write(BASE / 'storyboard_candidate.json', story)
update = '''## M03午休小出走：第二套全身已核准，坐姿續作 — 2026-10-13

使用者明確回覆「可以，沿用最後這張」，核准B2v4深藍西外／素面淺灰棉T／奶油白褲與一手扶黑肩包的全身起始圖；記錄在研究及週次素材夾`B2_user_approval_2026-10-13.json`。B1坐姿將用此核准服裝／包鎖定圖與第一套A2保留區間內3.75秒抽幀的視角、坐姿、頭腰位置生成；新圖仍待核准。B2可獨立以單一First frame測一步向右，維持扶包手、不加轉身與鏡頭動作；未生成前不填成功。最終順序仍走過A→坐姿A→坐姿B→離開B，原速無字、約0.75秒疊化。正式整片尚未完成，舊交付與外部發布保持原始紀錄。下方為歷史進度。

'''
status = ROOT / 'CURRENT_STATUS.md'
head, rest = status.read_text(encoding='utf-8-sig').split('\n', 1)
status.write_text(head + '\n\n' + update + rest.lstrip('\n'), encoding='utf-8')
readme = BASE / 'README.md'
readme.write_text(update + readme.read_text(encoding='utf-8-sig'), encoding='utf-8')
print('Exact B2 v4 approval recorded. B1 prompt words:', len(prompt.split()))
