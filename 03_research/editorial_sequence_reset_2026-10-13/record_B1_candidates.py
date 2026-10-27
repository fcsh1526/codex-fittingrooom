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

versions = [
    ('v1', 'M03_L02_B1_seated_candidate_v1_material_failed.png', 'exec-edd9a2fe-45c2-48e6-894c-ff505e13c770.png', 'B1_prompt_v1.txt', 'ornamental_tee_deviation'),
    ('v2', 'M03_L02_B1_seated_candidate_v2_material_failed.png', 'exec-01fc3644-2253-411e-bf6b-bf5969a21591.png', 'B1_material_correction_v2.txt', 'single_material_edit_failed'),
    ('v3', 'M03_L02_B1_seated_candidate_v3_material_framing_failed.png', 'exec-33366858-6ef3-4432-879b-8af3e3af6697.png', 'B1_clean_inputs_replan_v3.txt', 'material_and_full_seated_framing_deviation'),
    ('v4', 'M03_L02_B1_seated_candidate_v4_clean.png', 'exec-11d1a0f5-a77d-4236-a65d-15403e3a0b6c.png', 'B1_identity_only_replan_v4.txt', 'assistant_static_candidate_user_visual_approval_pending'),
]
rows = []
for version, name, original, prompt, status in versions:
    path = JOB / name
    if not path.exists():
        shutil.copyfile(GENERATED / original, path)
    shutil.copyfile(BASE / prompt, JOB / prompt)
    rows.append({'version': version, 'file': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'native_pixels': list(Image.open(path).size), 'original_generated_name': original, 'prompt': (JOB / prompt).relative_to(ROOT).as_posix(), 'status': status, 'framing_transform': 'none'})
plan = read(BASE / 'B1_reference_plan.json')
receipt = {
    'date': '2026-10-13', 'look_id': '2026-W41-004-L02', 'model': 'M03', 'shot': 'B1',
    'tool': 'built-in image_gen', 'status': 'v4_candidate_user_visual_approval_pending',
    'candidates': rows, 'generation_count': 4, 'targeted_material_edits': 1, 'input_replans': 2,
    'attempt_accounting': 'Initial B1 uses approved B2 wardrobe and late A2 framing, but tee gains motif. One material-only edit fails. Rebuild excluding A2 pixels but retaining B2 still has motif and becomes full seated. Final rebuild uses only identity anchors and written approved B2 wardrobe plus head-through-knees scene. All4 calls retained; no one-retry production success claimed.',
    'references_v1': [r['path'] for r in plan['references']],
    'references_v2': [rows[0]['file']],
    'references_v3': [plan['references'][2]['path'], plan['references'][3]['path'], plan['references'][0]['path']],
    'references_v4': [plan['references'][2]['path'], plan['references'][3]['path']],
    'wardrobe_authority': 'B2_user_approval_2026-10-13.json; final prompt states approved navy blazer/plain gray tee/cream trousers/black tapered shoulder bag. Rebuilt written wardrobe is not pixel-identical garment certification.',
    'assistant_static_review': 'Clean v4 plain heather-gray cotton tee, open navy lapels/one-fold cuffs, cream trousers, silver studs and broad black shoulder bag visible. Recognizable M03/hair, natural seat support/crossed leg and near-knee/bench hands. Native vertical head-through-knees proof; shoes outside frame are not certified from this view. Actual head/upper body somewhat larger and slightly right of late A2 focus; bench/window geometry recreated, not exact match. A2→B1 and B1→B2 comfort require combined-film review, no two-keyframe scene morph.',
    'user_approval': None, 'grok_uploaded': False, 'video_generated': False,
    'active_minutes': None, 'generation_wait_minutes': None,
    'formal_full_proof_carousel_complete': False,
}
write(BASE / 'B1_still_receipt.json', receipt)
write(JOB / 'B1_generation_receipt.json', receipt)
plan.update(status=receipt['status'], candidate=rows[-1]['file'], generation_count=4)
write(BASE / 'B1_reference_plan.json', plan)
sheet = JOB / 'review_sheet.csv'
with sheet.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fields, existing = reader.fieldnames, list(reader)
existing = [r for r in existing if '_B1_' not in r['file']]
for r in rows:
    existing.append({'file': r['file'], 'publishable': 'pending' if r['version']=='v4' else 'no', 'status': r['status'], 'notes': receipt['assistant_static_review'] if r['version']=='v4' else 'Material/framing differs from locked plain tee and seated proof plan; no Grok.'})
with sheet.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(existing)
story = read(BASE / 'storyboard_candidate.json')
story.update(status='B2_approved_motion_submission_recovery_B1_v4_pending_visual_approval', b1_candidate=rows[-1], b1_still_generation_count=4, next_action='User exact B1v4 approval before its Grok. Finish verifying actual B2 submission/result and source QA independently; then assemble A1→A2→B1→B2 after both B clips have usable intervals.')
write(BASE / 'storyboard_candidate.json', story)
update = '''## M03午休小出走：第二套坐姿v4待核准，處理全身動態 — 2026-10-13

B2v4已由使用者「可以，沿用最後這張」核准。B1坐姿共4次靜態生成：初版與一次材質修正出花紋、一次乾淨服裝參照重建仍偏材質與全身坐姿；v4只用核准人物雙參照＋文字第二套服裝，回到素面灰棉T與中景。新圖待精確視覺核准，未上傳Grok。B1v4頭部／上身較A2晚段稍大與稍偏右、窗框長椅重新建立，整支柔和度未驗證。檔案在W41-004-L02/reel/lunch_outing_v1/M03_L02_B1_seated_candidate_v4_clean.png；4次候選／提示詞／雜湊見同夾B1_generation_receipt.json與研究B1_still_receipt.json。B2送出一度無可見新影片；保留畫面、重新整理一次後以新鮮可及性索引恢復正確First frame＋Mira M03 v3＋720p/6s/9:16/無音訊。實際進度以B2_motion_attempt_01/browser_receipt.json為準，不將按下送出當作生成成功。未組正式四鏡片，未修改既有交付或外部發布。下方為歷史進度。

'''
status = ROOT / 'CURRENT_STATUS.md'
head, rest = status.read_text(encoding='utf-8-sig').split('\n', 1)
status.write_text(head + '\n\n' + update + rest.lstrip('\n'), encoding='utf-8')
readme = BASE / 'README.md'
readme.write_text(update + readme.read_text(encoding='utf-8-sig'), encoding='utf-8')
print('Saved all4 B1 candidates; clean v4 awaiting exact approval. B2 generation not presumed from click.')
