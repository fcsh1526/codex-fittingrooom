import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / '10_automation/runs/2026-W41'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

review = read(RUN / 'reels/M02_full_pair_static_review_2026-10-08.json')
approvals = []
target = RUN / 'reels/M02_full_pair_user_approval_2026-10-08.json'
if target.exists():
    raise SystemExit('Already recorded.')
manifest_path = RUN / 'reels/production_manifest.json'
manifest = read(manifest_path)
entry = next(x for x in manifest['reels'] if x['model_profile_id'] == 'M02')
for data in review['files']:
    file = ROOT / data['file']
    assert hashlib.sha256(file.read_bytes()).hexdigest() == data['sha256']
    approval = {'look_id': data['look_id'], 'file': data['file'], 'sha256': data['sha256'],
                'approved_on': '2026-10-08', 'user_quote': 'ok',
                'context': 'Response to displayed M02 L01 v4 / L02 v3 and pair visual approval request.',
                'scope': 'This exact full-person still as video first frame; not proof/Carousel/video acceptance.'}
    approvals.append(approval)
    receipt_path = file.parent / ('generation_receipt_v4.json' if data['look_id'].endswith('L01') else 'generation_receipt_v3.json')
    receipt = read(receipt_path)
    receipt.update(user_approval=approval, status='user_approved_full_person_first_frame')
    write(receipt_path, receipt)
    slot = next(x for x in entry['views'] if x['look_id'] == data['look_id'] and x['role'] == 'full')
    slot.update(approval=approval, source_type='native_reel_approved_still', framing_review='assistant_static_pass_user_approved', clarity_review='assistant_static_pass_user_approved')
    sheet = file.parent / 'review_sheet.csv'
    with sheet.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        fields, rows = reader.fieldnames, list(reader)
    rows[0]['status'] = 'user_approved_reel_first_frame'
    rows[0]['notes'] += ' User subsequently replies ok to this exact displayed pair; first-frame approval only.'
    with sheet.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
write(target, {'week': '2026-W41', 'model': 'M02', 'user_quote': 'ok', 'files': approvals})
review['user_approval'] = target.relative_to(ROOT).as_posix()
write(RUN / 'reels/M02_full_pair_static_review_2026-10-08.json', review)
entry['status'] = 'two_full_first_frames_user_approved_video_generation_next'
write(manifest_path, manifest)
request_path = ROOT / '10_automation/production_requests/2026-10-08_next_five_reels.json'
request = read(request_path)
next(x for x in request['slots'] if x['model'] == 'M02')['status'] = entry['status']
write(request_path, request)
pub_path = RUN / 'publishing_structure.md'
pub = pub_path.read_text(encoding='utf-8-sig').replace('第一套v4、第二套v3，待使用者分別核准', '第一套v4、第二套v3，使用者已回覆「ok」核准為起始圖；逐鏡影片生成與驗收待完成', 1)
pub_path.write_text(pub, encoding='utf-8')
sync_path = ROOT / '10_automation/production_requests/W41_git_sync_pending_2026-10-08.json'
sync = read(sync_path)
sync['user_approval'] = {'date': '2026-10-08', 'user_quote': 'ok', 'context': 'Direct reply to explicit public GitHub sync question describing this W41 checkpoint, media, prompts, review/browser records and production programs.', 'scope': 'The concrete W41 checkpoint previously described; not general authorization to publish unrelated local records.'}
sync['status'] = 'user_approved_public_sync_push_pending'
write(sync_path, sync)
status_path = ROOT / 'CURRENT_STATUS.md'
status = status_path.read_text(encoding='utf-8-sig')
new = '## W41 M02 full pair approved; Grok generation next — 2026-10-08\n\nUser replies `ok` to the displayed exact M02 L01 v4/L02 v3 still pair and approval request. Both hashes are verified and separately recorded in `10_automation/runs/2026-W41/reels/M02_full_pair_user_approval_2026-10-08.json`; only these full-person first frames are accepted, not proof/Carousel/video. Proceed with selected saved M02 v3 identity and each own first frame, fixed full-person camera, one short forward step and settle, audio off; inspect actual output and join before presenting a film. The same direct response follows the explicit question authorizing public GitHub synchronization of the concrete328-file W41 checkpoint; bounded authorization is saved in its sync receipt and a normal push is pending. No broader unrelated-record publication is authorized.\n\n'
status_path.write_text(status.replace('# Current Status - Mira AI Fashion Creator\n\n', '# Current Status - Mira AI Fashion Creator\n\n' + new, 1), encoding='utf-8')
print('Exact M02 pair acceptance and bounded public checkpoint authorization recorded.')
