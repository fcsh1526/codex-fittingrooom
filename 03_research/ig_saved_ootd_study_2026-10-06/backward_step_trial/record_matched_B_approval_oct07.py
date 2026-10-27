import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = next(p for p in BASE.parents if (p / '10_automation').is_dir())
JOB = ROOT / '10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/body_distance_matched_start_v2'
ASSET = JOB / '2026-W37-001-L02_M02_body_distance_matched_start_candidate_v3.png'
EXPECTED = 'f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6'

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

assert hashlib.sha256(ASSET.read_bytes()).hexdigest() == EXPECTED
for name in ('M02_start_v3_face.png', 'M02_start_v3_full.png'):
    assert (ROOT / '02_brand/reference_models' / name).is_file()
approval_path = JOB / 'visual_approval_v3_2026-10-07.json'
approval = {
    'date': '2026-10-07', 'user_reply': 'OK',
    'context': 'Direct reply to selected v3 face/outfit/composition approval question and next-step Grok generation proposal.',
    'asset': ASSET.relative_to(ROOT).as_posix(), 'sha256': EXPECTED,
    'scope': 'Individual starting-still visual approval for the new matched L02 B shot.',
    'video_approval': False, 'global_format_adoption': False, 'cloud_replacement_authorized': False,
}
save(approval_path, approval)
receipt_path = JOB / 'generation_receipt_v3.json'
receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
receipt.update(status='user_visual_approved', user_approval=approval_path.relative_to(ROOT).as_posix())
save(receipt_path, receipt)
with (JOB / 'review_sheet.csv').open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    columns, rows = reader.fieldnames, list(reader)
for row in rows:
    if row['filename'] == ASSET.name:
        row['status'] = 'user_visual_approved_for_matched_B_first_frame'
        row['notes'] += ' User OK 2026-10-07; exact asset SHA recorded. Video QA remains separate.'
with (JOB / 'review_sheet.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
manifest_path = BASE / 'trial_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['status'] = 'matched_B_v3_user_still_approved_grok_security_verification_pending'
manifest['matched_second_start'].update(status='user_visual_approved', user_visual_approval=approval_path.relative_to(ROOT).as_posix())
manifest['grok_current_gate'] = {'date': '2026-10-07', 'status': 'security_verification_pending', 'new_B_send_clicks': 0, 'new_B_source_retrieved': False}
save(manifest_path, manifest)
note = '\n\n### 2026-10-07：新 B v3 已核准\n\n使用者 `OK` 核准精確 v3 起始圖（SHA `'+EXPECTED+'`）的臉、服裝與構圖。此核准只含靜態，尚無新 B 來源或成片核准。下一步固定鏡位走近，以實際 A/B 18 對交疊幀選接點，保留原速及 0.75 秒疊化。Grok 目前待安全驗證，尚未送生成；原五支發布檔與研究成片保留。\n'
for name in ('README.md', 'revised_storyboard_v3.md'):
    with (BASE / name).open('a', encoding='utf-8') as f:
        f.write(note)
status_path = ROOT / 'CURRENT_STATUS.md'
text = status_path.read_text(encoding='utf-8')
text = text.replace('# Current Status - Mira AI Fashion Creator\n\n', '# Current Status - Mira AI Fashion Creator\n\n## Matched B v3 still approved; Grok safety verification pending — 2026-10-07\n\nUser `OK` individually approves selected matched L02 v3, SHA `'+EXPECTED+'`; approval receipt stored beside the still. Approved M02 v3 face/full exist. New B generation has not been submitted: one Grok tab is on the safety verification page, handed to the user. Routine local approval/shot/join preparation continues; actual new B motion and full two-look comfort remain untested. Original A and old B sources, failed v1 diagnostic, first-wave five and accepted research versions are preserved. No cloud write, publication or global format decision. Older pending-still notes below are historical.\n\n', 1)
status_path.write_text(text, encoding='utf-8')
publish_path = ROOT / '10_automation/runs/2026-W37/publishing_structure.md'
text = publish_path.read_text(encoding='utf-8-sig')
text = text.replace('# W37 Publishing Structure\n\n', '# W37 Publishing Structure\n\n**M02距離研究續作（2026-10-07）：** 使用者 `OK` 已核准 matched B v3 起始圖，精確雜湊與核准收據在其 L02 素材資料夾。新 B 尚未送生成，Grok 安全驗證待使用者完成；之後按真實動態檢查 18 對交疊幀，再試原速／0.75 秒疊化。未核准成片、未替換原五支、未上傳或發布。下方待静態核准為歷史。\n\n', 1)
publish_path.write_text(text, encoding='utf-8')
print(json.dumps({'approved_sha256': EXPECTED, 'identity_files_exist': True, 'new_B_submitted': False}, ensure_ascii=False))
