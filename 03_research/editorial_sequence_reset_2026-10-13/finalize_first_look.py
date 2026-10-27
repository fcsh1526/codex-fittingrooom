import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
JOB = ROOT / '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L01/reel/lunch_outing_v1'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

for shot, frames, seconds in [('A1', 54, 2.25), ('A2', 96, 4.0)]:
    folder = BASE / f'{shot}_motion_attempt_01'
    data = read(folder / 'technical_receipt.json')
    data['visual_review'] = 'sampled_frame_review_complete_user_normal_speed_review_pending'
    data['retained_interval_seconds'] = [0, seconds]
    data['retained_frames_end_exclusive'] = [0, frames]
    data['review_method'] = 'All145 thumbnails,25 larger whole-frame samples,5 face samples; native A1 frames0/30/48 or A2 frame60. No continuous normal-speed assistant playback.'
    if shot == 'A1':
        data.pop('provisional_interval_seconds', None)
        data['interval_note'] = 'Final trial retains initial step/settle through2.25s; later standing/side posing excluded. Prompt compliance remains partial.'
    else:
        data['actual_motion'] = 'Small torso adjustment toward daylight and relaxed settle; hand initially on knee moves near bench. No full sitting-down action.'
        data['identity_wardrobe_background'] = 'Recognizable identity, plain tee/navy trousers, cream lapels and brown bag retained in sampled frames. Bench/window/wall broadly stable; exact pixel lock and every native hand-contact frame not certified.'
    write(folder / 'technical_receipt.json', data)
    for target in [BASE / f'{shot}_still_receipt.json', JOB / f'{shot}_generation_receipt.json']:
        still = read(target)
        still.update(grok_uploaded=True, video_generated=True, motion_generation_count=1,
                     browser_receipt=f'03_research/editorial_sequence_reset_2026-10-13/{shot}_motion_attempt_01/browser_receipt.json',
                     motion_source_sha256=data['sha256'], user_film_approval=None)
        write(target, still)

review = {
    'status': 'sampled_frame_review_complete_user_normal_speed_review_pending',
    'method': 'All132 output thumbnails,25 larger whole-frame samples,5 face samples;23 transition/boundary samples including all18 dissolve frames.',
    'findings': 'No black/decode failures; recognizable clothing and face in sampled single-source intervals. Standing-to-seated scale, face position and bench viewpoint differ; visible double heads/body outlines during overlap. Not an invisible match.',
    'limits': 'No assistant continuous normal-speed playback. User comfort, daily-magazine impression, originality and whole-film acceptance pending. No audience or sustainable-budget conclusions.',
    'assistant_continuous_playback': False,
    'user_film_approval': None,
}
edit = read(BASE / 'first_look_edit_receipt.json')
edit['status'] = review['status']
edit['visual_review'] = review
write(BASE / 'first_look_edit_receipt.json', edit)
technical_path = BASE / 'first_look_review_v1/technical_receipt.json'
technical = read(technical_path)
technical['visual_review'] = review
write(technical_path, technical)
story = read(BASE / 'storyboard_candidate.json')
story['status'] = 'first_look_subsequence_ready_user_review_pending'
story['a2_motion_generation_count'] = 1
story['next_action'] = 'Show first-look5.5s same-outfit walk-to-seated sub-sequence for user normal-speed editorial review. Generate no B stills or motion before this evaluation.'
story['first_look_trial'] = {'file': edit['file'], 'seconds': 5.5, 'source_intervals_seconds': [[0, 2.25], [0, 4]], 'dissolve_seconds': 0.75, 'review': review, 'formal_two_look_delivery': False}
story['active_production_minutes'] = None
story['generation_wait_minutes'] = None
write(BASE / 'storyboard_candidate.json', story)

report = '''# 第一套兩鏡試片：午休的小出走

2026-10-13。狀態：抽幀檢查完成，等待使用者正常播放評估。

## 本次交付

`first_look_review_v1/M03_L01_walk_to_seated_trial_v1.mp4`：5.5秒、720×1280、24fps。第一套同一服裝的兩鏡子片段，尚非正式一人兩套Reel。

- A1採0–2.25秒；實際為一步後收腳，不是持續走過畫面。
- A2採0–4秒；已坐姿的小幅上身調整與放鬆。
- 1.50–2.25秒使用0.75秒交叉溶接。保持原速，無字、無音、無縮放或凍結。

## 檢查與限制

看過來源各145張縮圖、25張大圖、5張臉部；另查A1原尺寸0/30/48幀及A2第60幀。成片看過全部132張縮圖、25張大圖、5張臉部、含全部18張疊化幀的23張接點取樣。取樣中人物、服装与背景大致穩定，無黑幀／解碼錯誤；不宣稱逐張原尺寸接觸或背景幾何完全一致。

接點有可見雙頭與身體重影，站姿與坐姿大小、臉位置、長椅視角不一致；不是無差別軟換。正常速度的舒服度與日常雜誌感等待使用者看整段判斷，助手連續正常播放未完成。不能由技術檢查推定審美核准、流量或量產效果。

## 成本與範圍

A1兩次靜態生成（含一次姿勢修正）；A2四次靜態生成，前三版材質偏離，最後排除污染參照重建。兩鏡Grok各生成一次。主動製作／純等待時間未完整計量，留空。失敗圖與提示詞保留，不能稱為一次重試即成功的量產流程。

兩張起始圖已獲精確使用者核准；影片尚未核准。第二套B1/B2未生成。先評估本片，再決定續作或重排接點。舊W41五支交付影片於本次輸出時雜湊一致；研究檔獨立保存，無Drive／GitHub／IG寫入。

完整紀錄：`first_look_edit_receipt.json`、各鏡`browser_receipt.json`與`technical_receipt.json`、`storyboard_candidate.json`。
'''
(BASE / 'FIRST_LOOK_REVIEW.md').write_text(report, encoding='utf-8')
update = '''## M03午休小出走：第一套5.5秒試片待觀看 — 2026-10-13

A1 v2與A2 v4已分別獲使用者「可以，沿用修正版」「可以，沿用這張」核准；各以Grok單一First frame生成一次。第一套同服裝走過→坐姿子片已輸出5.5秒、原速、無字無音、0.75秒疊化；實際A1只一步後收腳，非持續短走。抽幀檢查完成，但接點人物大小／臉位置與長椅視角不同，有可見雙重輪廓。等待使用者正常播放判斷舒服度與日常雜誌感；不推定影片、帳號風格或成效核准。B1/B2第二套尚未生成，先評估子片再續作。A2材質共四次靜態生成，失敗版本保留；時間未完整計量。成片：`03_research/editorial_sequence_reset_2026-10-13/first_look_review_v1/M03_L01_walk_to_seated_trial_v1.mp4`；紀錄：同研究夾`FIRST_LOOK_REVIEW.md`與`first_look_edit_receipt.json`。舊W41五支交付影片輸出時雜湊一致，無Drive／GitHub／IG寫入。下方較早待核准／未生成項目為歷史狀態。

'''
status = ROOT / 'CURRENT_STATUS.md'
old = status.read_text(encoding='utf-8-sig')
heading, remainder = old.split('\n', 1)
status.write_text(heading + '\n\n' + update + remainder.lstrip('\n'), encoding='utf-8')
readme = BASE / 'README.md'
readme.write_text(update + readme.read_text(encoding='utf-8-sig'), encoding='utf-8')
print('Finalized receipts and current status; first-look trial awaits user viewing.')
