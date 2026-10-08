import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '10_automation/runs/2026-W41'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

folder = BASE / 'reels/M01/review_v2'
receipt = read(folder / 'composition_receipt.json')
assert hashlib.sha256((ROOT / receipt['output_path']).read_bytes()).hexdigest() == receipt['sha256']
approval = {
    'date': '2026-10-08', 'user_quote': 'ok',
    'context': 'Direct response to displayed M01 9.5s v2 cuff-correction film and specific playback/acceptance request.',
    'file': receipt['output_path'], 'sha256': receipt['sha256'],
    'scope': 'Accept this exact corrected film picture for use; not other stills, proof images, Carousel assets, other films or metrics.',
    'user_full_duration_playback_self_report': None,
    'assistant_continuous_playback_review': False,
    'status': 'user_picture_accepted',
    'prior_v1': 'Rejected and preserved; no retrospective acceptance.'
}
target = folder / 'user_picture_approval_2026-10-08.json'
if target.exists():
    raise SystemExit('Already recorded.')
write(target, approval)
approval_rel = target.relative_to(ROOT).as_posix()
receipt['user_approval'] = approval_rel
receipt['status'] = 'user_picture_accepted'
write(folder / 'composition_receipt.json', receipt)
review_path = folder / 'root_review_2026-10-08.json'
review = read(review_path)
review['user_approval'] = approval_rel
review['status'] = 'sampled_review_complete_user_picture_accepted'
write(review_path, review)
manifest_path = BASE / 'reels/production_manifest.json'
manifest = read(manifest_path)
entry = next(x for x in manifest['reels'] if x['model_profile_id'] == 'M01')
assert entry['output_path'] == receipt['output_path']
entry['qa']['user_approval'] = approval_rel
entry['qa']['status'] = 'sampled_review_complete_user_picture_accepted'
entry['status'] = 'film_picture_accepted_proof_and_carousel_incomplete'
write(manifest_path, manifest)
request_path = ROOT / '10_automation/production_requests/2026-10-08_next_five_reels.json'
request = read(request_path)
slot = next(x for x in request['slots'] if x['model'] == 'M01')
slot['status'] = entry['status']
slot['accepted_picture_file'] = receipt['output_path']
slot['user_approval'] = approval_rel
slot['final_file'] = None
write(request_path, request)
pub_path = BASE / 'publishing_structure.md'
pub = pub_path.read_text(encoding='utf-8-sig')
pub = pub.replace('逐格接觸及成片抽查已完成，待完整播放與使用者視覺核准', '逐格接觸及成片抽查已完成，使用者回覆「ok」沿用此版；完整播放自述尚無紀錄', 1)
pub = pub.replace('尚無W41最終核准成片，尚未上傳或發布', 'M01修正版畫面已核准；其proof與Carousel仍未完成，整批尚未交付、上傳或發布', 1)
pub_path.write_text(pub, encoding='utf-8')
status_path = ROOT / 'CURRENT_STATUS.md'
status = status_path.read_text(encoding='utf-8-sig')
heading = '## W41 M01 cuff-corrected v2 picture accepted; continue M02 — 2026-10-08\n\n'
text = 'User directly replies `ok` to the displayed exact9.5s M01 review_v2 cuff correction and specific acceptance request. Film SHA `936b8794070eeb32c411bb38f5ea1b902eb6f7aad4f2d86c0366c56f441a3839` is verified and preserved; exact bounded acceptance is recorded in `10_automation/runs/2026-W41/reels/M01/review_v2/user_picture_approval_2026-10-08.json`. This approves the corrected picture for use, not a reported full-duration watch, other candidates, proof stills or complete weekly delivery. Assistant continuous playback remains false. Rejected v1 and previous five W37/Drive originals remain unchanged. M01 proof/Carousel work is still incomplete; M05 film/proof approvals remain pending. Continue W41 M02 source stills from its existing whole-film storyboard, with separate user visual approval before Grok.\n\n'
status_path.write_text(status.replace('# Current Status - Mira AI Fashion Creator\n\n', '# Current Status - Mira AI Fashion Creator\n\n' + heading + text, 1), encoding='utf-8')
print('Exact M01 v2 picture acceptance recorded; remaining assets stay incomplete.')
