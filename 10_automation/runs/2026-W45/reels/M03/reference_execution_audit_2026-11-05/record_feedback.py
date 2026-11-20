from pathlib import Path
import json
import hashlib

root = Path(__file__).resolve().parents[6]
audit = Path(__file__).resolve().parent
n = root / '10_automation/runs/2026-W45/reels/M03/natural_parallel_2026-11-05'
week = root / '10_automation/runs/2026-W45'
report_rel = (audit / 'REVIEW.md').relative_to(root).as_posix()
feedback_rel = (audit / 'user_editorial_feedback.json').relative_to(root).as_posix()
film_rel = (n / 'paired_review_v1/M03_W45_natural_parallel_review_v1.mp4').relative_to(root).as_posix()
expected = '13cd4260052fb452e396d2293874e0fa7496b0dfee868c8702e4c004621d072c'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

assert (root / 'CURRENT_STATUS.md').exists(), root
assert sha(root / film_rel) == expected
feedback = {
    'date': '2026-11-05', 'timezone': 'Asia/Taipei', 'actor': 'user',
    'quote': '這個好像沒有參考前面看過別人IG 的reel。然後好像也沒照我們工作流，然後好像也只是舊版的影像剪輯模式',
    'decision': 'editorial_and_workflow_revision_requested',
    'target_path': film_rel, 'target_sha256': expected,
    'context': 'Direct feedback to the displayed 6.041667s natural parallel candidate.',
    'assistant_diagnosis': 'Reference findings were not mapped into observable performance and framing development; no-dance preference was overconstrained into a turn-and-stand display. Existing parallel layout is not itself rejected.',
    'limits': 'No new source/still/publication approval, no explicit rejection of all source footage or A layout. The exact multi-action parallel IG reference remains unconfirmed.',
    'audit_path': report_rel, 'new_generation': False,
}
write(audit / 'user_editorial_feedback.json', feedback)

current = (root / 'CURRENT_STATUS.md').read_text(encoding='utf-8-sig')
old = 'W45現況：' + current.split('- W45現況：', 1)[1].split('\n', 1)[0]
new = 'W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03舊4秒v4因搖擺跳舞不採用；後續6.041667秒natural_parallel候選又獲使用者回饋：看不出先前IG參考、未落實工作流、仍像舊剪輯模式。現行任務改為參考到分鏡的企劃修正，撤出該片重複待審，不續做縮短／調動作等局部修剪。查核已完成，具體偏差與三階段提案見 `10_automation/runs/2026-W45/reels/M03/reference_execution_audit_2026-11-05/REVIEW.md`；新線稿與必要預檢尚待完成，未新增生成。A並排、原兩張首圖核准保留，舊片與來源不刪除。累計七次靜態／十四支原片／兩支接受成片；M04–M05及proof／Carousel仍缺，M03未獲成片／發布核准。'
for rel in ['CURRENT_STATUS.md', '10_automation/CANONICAL_WORKFLOW.md', '10_automation/MIRA_EDITORIAL_HANDOFF.md', '10_automation/runs/2026-W45/publishing_structure.md']:
    p = root / rel
    text = p.read_text(encoding='utf-8-sig')
    assert text.count(old) == 1, rel
    text = text.replace(old, new)
    if rel.endswith('publishing_structure.md'):
        text = text.replace('M03 A排版保留；現行[自然並排6.04秒候選](reels/M03/natural_parallel_2026-11-05/paired_review_v1/REVIEW.md)待品質回饋，舊v4跳舞方向不採用。', 'M03 A排版保留；自然並排6.04秒候選需企劃修正，依[參考落實檢討](reels/M03/reference_execution_audit_2026-11-05/REVIEW.md)重做連接分鏡。舊v4跳舞方向不採用。')
    if rel.endswith('MIRA_EDITORIAL_HANDOFF.md'):
        text = text.replace('待此精確新片回饋。A偏好與原首圖保持，沒有發布核准。', '使用者已回饋其參考轉用、流程及內容不足，轉入企劃修正。A偏好與原首圖保持，沒有發布核准。')
        text = text.replace('目前下一步：回看M03自然並排6.04秒候選的表演、尺度與轉身腳掌；舊搖擺v4維持不採用。IG沿用現有頁，本回合未操作IG或新增分頁。', '目前下一步：依M03參考落實檢討，完成參考機制對照的連接線稿與實際並排尺度預檢；不再重貼6.04秒片待審，不直接追加生成。舊搖擺v4維持不採用。')
    p.write_text(text, encoding='utf-8')

queue = read(week / 'production_queue.json')
queue.update(status='M03_reference_to_storyboard_revision_required', active_reviews=[], active_trial=None,
             latest_editorial_proposal=report_rel, latest_performance_feedback=feedback_rel,
             next={'model': 'M03', 'action': 'Create reference-mapped connected storyboard and actual-panel preflight from the corrective brief. Do not recut/re-present the 6s candidate or automatically generate.'})
write(week / 'production_queue.json', queue)

plan = read(n / 'production_plan.json')
plan.update(status='editorial_revision_required_after_user_feedback', latest_feedback=feedback_rel, superseding_editorial_brief=report_rel)
write(n / 'production_plan.json', plan)
for filename in ['edit_receipt.json', 'visual_review.json']:
    p = n / 'paired_review_v1' / filename
    data = read(p)
    data.update(status='user_feedback_requires_editorial_revision', latest_user_feedback=feedback_rel)
    write(p, data)

notice = '最新：使用者指出此片沒有落實先前IG參考與工作流、仍像舊版剪輯。轉入[企劃修正](../../reference_execution_audit_2026-11-05/REVIEW.md)，不再列成片待審；本頁以下為原製作紀錄。A排版與原首圖核准保留。\n\n'
p = n / 'paired_review_v1/REVIEW.md'
text = p.read_text(encoding='utf-8-sig')
heading, body = text.split('\n\n', 1)
p.write_text(heading + '\n\n' + notice + body, encoding='utf-8')
(n / 'STATUS.md').write_text('# M03 自然並排｜有效狀態\n\n2026-11-05。6.04秒候選收到參考轉用／工作流／舊版模式的修正回饋，現行任務為[參考到分鏡的企劃修正](../reference_execution_audit_2026-11-05/REVIEW.md)。原候選與兩支來源保留，不重貼待審、不追加生成。A並排、兩張首圖與M01／M02既有接受保留。新增生成0，沒有新成片／發布核准。\n', encoding='utf-8')

registry_path = root / '04_prompts/material_pool/series_registry.json'
registry = read(registry_path)
series = next(s for s in registry['series'] if s['series_id'] == 'SERIES_W45_M03')
series.update(status='reference_to_storyboard_revision_required', current_reassessment=report_rel,
              latest_editorial_proposal=report_rel, latest_performance_feedback=feedback_rel)
use = next(u for u in registry['uses'] if u['usage_id'] == 'USE_W45_M03_NATURAL_PARALLEL_V1_20261105')
use.update(status='user_feedback_requires_editorial_revision', latest_feedback_receipt=feedback_rel,
           feedback_summary='User finds IG reference learning and workflow execution missing; still resembles the old edit. Returned to editorial/storyboard revision. Existing A layout and approved stills remain; no film or publication acceptance.')
write(registry_path, registry)

protected = {
    'reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4': 'aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb',
    'reels/M02/trial_03/M02_W45_trial03_silent_review.mp4': 'bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67',
}
for rel, digest in protected.items():
    assert sha(week / rel) == digest, rel
assert sha(root / film_rel) == expected
write(audit / 'verification.json', {'date': '2026-11-05', 'film_unchanged': True, 'accepted_M01_M02_unchanged': True, 'new_still_calls': 0, 'new_video_jobs': 0, 'active_review_removed': True, 'next': 'connected storyboard and reference mapping; not new generation', 'files_are_local_only': True})
print('Feedback recorded; active state reconciled; film and accepted M01/M02 hashes unchanged.')
