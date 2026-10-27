import json
from pathlib import Path

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
reels = run / 'reels'
approval = {
    'date': '2026-10-02',
    'reply': '還ok',
    'reviewer': 'user',
    'context': 'Reply after embedded complete 8.75-second video and request to review all three transitions, person and background.',
    'scope': 'Selected complete two-look picture track; no music, publication, account-wide style or audience-performance approval.'
}

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

record_path = reels / 'M03_two_looks_soft_review_v1_01.json'
record = read_json(record_path)
assert (root / record['output_path']).is_file()
record['status'] = 'user_accepted_clean_picture_track'
record['qa'].update(continuous_watch_done=True, continuous_review_reviewer='user',
    user_approval='還ok', approval_date='2026-10-02', approval_evidence=approval)
record['qa']['open_issues_at_review_request'] = record['qa'].pop('open_issues', [])
record['qa']['open_issues'] = []
record['qa']['remaining_delivery_steps'] = ['Music selection and usage evidence', 'Final Instagram assembly and publication']
record['first_transition_basis'] += ' Complete three-transition picture track subsequently accepted by user on2026-10-02 (還ok).'
write_json(record_path, record)

manifest_path = reels / 'production_manifest.json'
manifest = read_json(manifest_path)
entry = next(x for x in manifest['reels'] if x['model_profile_id'] == 'M03')
entry['status'] = 'user_accepted_clean_picture_track'
entry['qa'].update(status='user_accepted_complete_picture_track', continuous_watch_done=True,
    continuous_review_reviewer='user', user_approval='還ok', approval_date='2026-10-02', approval_evidence=approval)
entry['music']['clean_master'] = entry['output_path']
write_json(manifest_path, manifest)

delivery_path = reels / 'M03_delivery.md'
text = delivery_path.read_text(encoding='utf-8-sig')
text = text.replace('完整使用者核准待回覆。', '2026-10-02使用者看完整預覽後回覆「還ok」，此版乾淨畫面沿用。')
text = text.replace('新增兩個接點及整片仍須正常播放驗收。', '新增兩個接點及整片已於2026-10-02收到使用者「還ok」回覆；核准範圍僅此支畫面。')
delivery_path.write_text(text, encoding='utf-8')
caption_path = reels / 'M03_instagram_caption_draft.md'
text = caption_path.read_text(encoding='utf-8-sig').replace('完整使用者視覺核准待回覆。', '2026-10-02使用者回覆「還ok」，乾淨畫面沿用。')
caption_path.write_text(text, encoding='utf-8')

for path, heading, update in [
    (root / 'CURRENT_STATUS.md', '# Current Status - Mira AI Fashion Creator',
     '\n\n## M03 complete picture track accepted — 2026-10-02\n\nUser replied `還ok` after the embedded complete8.75-second two-look film and explicit full-film review question. Selected `reels/videos/M03_two_looks_soft_review_v1_01.mp4` is accepted as the clean picture track, including its three0.75-second dissolves. Source actions unchanged; no text/audio. User visual review is recorded separately from assistant sampled QA. This acceptance does not establish global style or audience performance. M02/M05/M04/M03 now have accepted picture tracks; M01 complete video still needs user review. Music, IG assembly and publication remain open. Earlier pending notes below are historical.\n'),
    (run / 'publishing_structure.md', '# W37 Publishing Structure',
     '\n\n**M03完整畫面核准（2026-10-02）：** 使用者看8.75秒完整預覽後回覆「還ok」。沿用 `reels/videos/M03_two_looks_soft_review_v1_01.mp4`：兩套四鏡、三個0.75秒交疊、原動作速度、無字無音。核准只涵蓋此支畫面，不代表帳號通用風格、成效或發布授權。M02／M05／M04／M03畫面已核准，M01完整影片仍待確認；音樂與IG最後組裝／發布未完成。下方待核准紀錄為歷史狀態。\n')
]:
    text = path.read_text(encoding='utf-8-sig')
    assert text.startswith(heading)
    path.write_text(text.replace(heading, heading + update, 1), encoding='utf-8')

story_path = reels / 'M03_storyboard_v1.md'
with story_path.open('a', encoding='utf-8') as output:
    output.write('\n## 完整預覽回覆｜2026-10-02\n\n使用者對8.75秒完整兩套預覽回覆「還ok」，沿用此版三個0.75秒交疊的乾淨畫面。此單片核准不設定其他影片的轉場或鏡頭數；音樂、IG最後組裝與發布另行處理。上文待回覆為當時紀錄。\n')

gate_path = reels / 'REEL_RELEASE_GATE_2026-09-30.md'
lines = gate_path.read_text(encoding='utf-8-sig').splitlines()
for i, line in enumerate(lines):
    if line.startswith('更新：'):
        lines[i] = '更新：2026-10-02。保留檔名，以下狀態已納入M03完整畫面核准。'
    if line.startswith('| M03／'):
        lines[i] = '| M03／麂皮與皮革一件亮點 | 四張起始圖已核准；`videos/M03_two_looks_soft_review_v1_01.mp4`，8.75秒、720×1280、無字無音，三個0.75秒交疊 | 全210幀解碼與16個時間點抽查完成；2026-10-02使用者對完整預覽回覆「還ok」，此版畫面沿用 | 音樂與使用範圍紀錄、IG最後組裝與發布；素材、提示詞與內文已分開整理 |'
    if line.startswith('## 現有三支的發布交接'):
        lines[i] = '## 原先三支的發布交接'
    if line.startswith('2. M03完整播放'):
        lines[i] = '2. M03完整畫面已沿用；製作交接在 `M03_delivery.md`。本次0.75秒交疊不自動套用其他影片。'
gate_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('M03 acceptance recorded; M01 remains pending. No video files changed.')
