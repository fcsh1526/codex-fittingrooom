from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(__file__).resolve().parent
JOB = ROOT / '10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

p = BASE / 'B2_motion_attempt_01/technical_receipt.json'
qa = read(p)
qa.update(visual_review='sampled_source_candidate_whole_film_review_pending',
          review_method='All145 frame thumbnails,25 larger whole-frame samples,5 face samples and native frames18/54/72 viewed. No assistant continuous normal-speed playback.',
          actual_motion='Short mainly forward step followed by settle, arm swing and a shallow body-angle change; later ankle-crossed pose. Not requested sustained diagonal departure. Prompt compliance partial.',
          identity_wardrobe_background='Recognizable M03, plain gray tee, navy lapels/cuffs, cream trousers, shoe and bag forms broadly retained. Holding hand remains at strap in sampled frames; window/bench/wall broadly stable. No gross instantaneous morph observed; native contact/geometry every frame not certified.',
          provisional_interval_seconds=[0,3.0],
          interval_note='Candidate initial short-step/settle interval, not final trim. Exact interval and closing editorial purpose depend on B1→B2 joint review; do not label actual footage walking away.',
          motion_prompt_compliance='partial', user_film_approval=None, assistant_continuous_playback=False)
write(p, qa)
for p in [BASE / 'B2_still_receipt.json', JOB / 'B2_generation_receipt.json']:
    data = read(p)
    data.update(grok_uploaded=True, video_generated=True, confirmed_motion_result_count=1,
                total_server_generation_count=None, motion_source=qa['source'], motion_source_sha256=qa['sha256'],
                motion_review='B2_motion_attempt_01/technical_receipt.json', user_film_approval=None)
    write(p, data)
browser_path = BASE / 'B2_motion_attempt_01/browser_receipt.json'
browser = read(browser_path)
browser['note'] = 'Historical first locator send had no visible job confirmation; one reload and fresh accessibility-index submission produced one confirmed downloadable result. First action server billing/count unknown; only one result verified.'
browser['ui_recovery'] = 'One reload, unrelated Loop modal dismissed, rebuilt same authorized draft. Fresh accessibility-index send visibly cleared input, opened result post, and provided downloadable video. No private APIs or guessed downloads.'
write(browser_path, browser)
story = read(BASE / 'storyboard_candidate.json')
story.update(status='B2_source_reviewed_B1_v4_pending_visual_approval', b2_confirmed_motion_result_count=1,
             b2_motion_source=qa['source'], b2_provisional_interval_seconds=[0,3],
             b2_actual_motion=qa['actual_motion'],
             next_action='Wait for exact user visual approval of clean B1v4. Then animate B1 with First frame and M03 reference, inspect source, and assemble four-shot two-look trial. B2 initial step/settle is provisional, no sustained departure claimed. Whole-film acceptance pending.')
write(BASE / 'storyboard_candidate.json', story)
update = '''## M03午休小出走：第三鏡坐姿待核准，全身動態已檢查 — 2026-10-13

B2全身v4已核准並生成可下載影片：6.04秒、720×1280、24fps，來源存研究`B2_motion_attempt_01/source.mp4`。首次定位送出無可見生成；重新整理一次、關閉誤入的循環視窗，改用新鮮可及性索引後建立實際post並下載，只確認1個結果，前次是否計費留空。已看全部145張縮圖、25張大圖、5張臉部及18/54/72原尺寸幀；取樣臉／服裝／扶包手／窗框長椅大致穩定。實際是偏向前方的短步＋站姿變化，非計畫持續斜向離開；0–3秒僅候選，待相鄰鏡頭整片檢查後定剪點。B1坐姿v4回到素面灰棉T、深藍西外與奶油白褲／黑包，新圖正待精確視覺核准，未上傳Grok。核准後生成坐姿動態再組四鏡；目前不能宣稱正式影片、完整播放或成效通過。B1及B2各4次靜態生成的失敗證據、提示詞與雜湊保留；無舊交付影片／Drive／IG／GitHub寫入。下方為歷史進度。

'''
status = ROOT / 'CURRENT_STATUS.md'
head, rest = status.read_text(encoding='utf-8-sig').split('\n',1)
status.write_text(head + '\n\n' + update + rest.lstrip('\n'), encoding='utf-8')
readme = BASE / 'README.md'
readme.write_text(update + readme.read_text(encoding='utf-8-sig'), encoding='utf-8')
print('B2 source reviewed; final trim pending. B1v4 still waits for exact user approval.')
