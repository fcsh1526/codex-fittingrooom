import json
from pathlib import Path

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
reels = run / 'reels'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

approval = dict(date='2026-10-02', reply='ok', reviewer='user',
    context='Direct reply to embedded M01 soft-transition complete preview and explicit adoption question.',
    scope='Complete clean picture track with0.75-second overlap; no music or publication approval.')
record_path = reels / 'M01_two_looks_soft_review_v2_01.json'
record = load(record_path)
record['status'] = 'user_accepted_clean_picture_track'
record['qa'].update(continuous_watch_done=True, continuous_review_reviewer='user',
    user_approval='ok', approval_date='2026-10-02', approval_evidence=approval)
save(record_path, record)

manifest_path = reels / 'production_manifest.json'
manifest = load(manifest_path)
entry = next(r for r in manifest['reels'] if r['model_profile_id'] == 'M01')
entry['status'] = 'user_accepted_clean_picture_track'
entry['qa'].update(status='user_accepted_complete_picture_track', continuous_watch_done=True,
    continuous_review_reviewer='user', user_approval='ok', approval_date='2026-10-02', approval_evidence=approval)
entry['music']['clean_master'] = entry['output_path']
caption_paths = {'M02': 'pilot_M02/M02_instagram_caption_draft.md', 'M05': 'M05_instagram_caption_draft.md'}
for item in manifest['reels']:
    model = item['model_profile_id']
    if model in caption_paths:
        item['caption_path'] = (reels / caption_paths[model]).relative_to(root).as_posix()
    assert (root / item['output_path']).is_file(), model
    assert (root / item['caption_path']).is_file(), model
    assert item['qa']['user_approval'], model
manifest['picture_delivery'] = dict(status='five_user_accepted_clean_picture_tracks', date='2026-10-02',
    handoff_path=(reels / 'W37_REEL_HANDOFF.md').relative_to(root).as_posix(),
    music_complete=False, published=False, carousel_complete='not_asserted')
save(manifest_path, manifest)

header = '# W37 Reel 交付清單\n\n更新：2026-10-02。五支乾淨畫面已由使用者核准；每支一位模特兒、兩套穿搭，720×1280，無畫面文字、無音樂。尚未在Instagram發布。\n\n'
table = '| 主題（內部模特兒） | 已核准影片 | 貼文內文草稿 |\n| --- | --- | --- |\n'
for item in sorted(manifest['reels'], key=lambda x: x['model_profile_id']):
    video = (root / item['output_path']).as_posix()
    caption = (root / item['caption_path']).as_posix()
    table += f"| {item['theme']}（{item['model_profile_id']}） | [開啟影片](<{video}>) | [開啟內文](<{caption}>) |\n"
notes = '''
## 使用這份交付

1. 從上表取得選定影片；內部模特兒代碼不用放在公開內容。
2. 在Instagram編輯器選音樂，完整播放聲畫後再完成最後組裝；記錄音樂來源與使用範圍。
3. 選無字封面，在Instagram預覽確認裁切；目前影片不用加字。
4. 使用對應貼文內文草稿，發布後記錄網址與時間。
5. 發布後24小時、72小時及第7天補回洞察；缺少欄位留空。

## 已定案的後續製作方式

先定整支視覺主題，再設計能銜接的鏡頭，最後生成起始圖。鏡頭數依穿搭資訊決定。所有後續切換預設約0.75秒柔和交疊，人物動作與來源速度保持原樣；交付不烙字。

M01新版約6.71秒、一次0.75秒交疊；M03為8.75秒、三次0.75秒交疊。M02／M04／M05保留先前已核准版本，沒有宣稱它們已套用新轉場。

這是Reel畫面的交付，不代表全部Carousel完成、帳號成效驗證或四週試行已開始。正式比較從實際發布起算；主動工時與生成等待沒有完整測量，維持空值。
'''
(reels / 'W37_REEL_HANDOFF.md').write_text(header + table + notes, encoding='utf-8')

for path, heading, note in [
    (root / 'CURRENT_STATUS.md', '# Current Status - Mira AI Fashion Creator',
     '\n\n## Five W37 Reel picture tracks accepted — 2026-10-02\n\nUser replied `ok` to the complete M01 soft-transition preview. M01 `reels/videos/M01_two_looks_soft_review_v2_01.mp4` now joins accepted M02/M03/M04/M05 picture tracks. All five exact files and caption drafts are linked in `10_automation/runs/2026-W37/reels/W37_REEL_HANDOFF.md`; manifest caption paths forM02/M05 completed. Video-only delivery is accepted, with no text/audio. Music, IG assembly/cover cropping, publication and performance measurement remain open. All subsequent transitions use approximately0.75-second dissolves with actions/source speed unchanged; prior accepted exports preserved. Carousel completion is not claimed. Earlier M01 pending notes below are historical.\n'),
    (run / 'publishing_structure.md', '# W37 Publishing Structure',
     '\n\n**五支Reel畫面交付（2026-10-02）：** 使用者對M01柔和轉場新版回覆「ok」，五支完整兩套画面均核准。影片與貼文草稿集中於 `reels/W37_REEL_HANDOFF.md`。目前皆無字無音，音樂／IG最後組裝與發布另行處理；Carousel與四週成效尚未完成。未再擴大製作。後續所有切換約0.75秒交疊的規則繼續適用。下方待M01確認為歷史狀態。\n')
]:
    text = path.read_text(encoding='utf-8-sig')
    assert text.startswith(heading)
    path.write_text(text.replace(heading, heading+note, 1), encoding='utf-8')

caption_path = reels / 'M01_instagram_caption_draft.md'
text = caption_path.read_text(encoding='utf-8-sig').replace('（使用者完整動態核准待回覆）', '（2026-10-02使用者對完整新版回覆「ok」，畫面沿用）')
caption_path.write_text(text, encoding='utf-8')
with (reels / 'M01_storyboard_v1.md').open('a', encoding='utf-8') as stream:
    stream.write('\n## 新版完整畫面核准｜2026-10-02\n\n使用者對0.75秒交疊新版完整預覽回覆「ok」，此版乾淨畫面沿用；音樂與IG最後組裝／發布未完成。\n')
gate_path = reels / 'REEL_RELEASE_GATE_2026-09-30.md'
lines = gate_path.read_text(encoding='utf-8-sig').splitlines()
for i, line in enumerate(lines):
    if line.startswith('更新：'):
        lines[i] = '更新：2026-10-02。五支Reel乾淨畫面均獲使用者核准；集中交付在 `W37_REEL_HANDOFF.md`。'
    if line.startswith('| M01／'):
        lines[i] = '| M01／復古 T 字帶鞋日常化 | `videos/M01_two_looks_soft_review_v2_01.mp4`，約6.71秒、0.75秒交疊、720×1280、無字無音；兩套全身＋鞋面proof齊備 | 全161幀解碼與12個時間點抽查完成；2026-10-02使用者對完整新版回覆「ok」，畫面沿用 | 音樂與使用範圍、IG最後組裝與發布；內文已準備 |'
    if line.startswith('## 下一段製作順序'):
        lines[i] = '## 下一段交接'
    if line.startswith('3. 補齊M01'):
        lines[i] = '3. M01完整畫面已核准；由 `W37_REEL_HANDOFF.md` 取得五支影片與內文，接續音樂／封面裁切／IG發布與成效紀錄。'
gate_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('M01 acceptance saved. Five existing videos and five caption files verified; consolidated handoff ready.')
