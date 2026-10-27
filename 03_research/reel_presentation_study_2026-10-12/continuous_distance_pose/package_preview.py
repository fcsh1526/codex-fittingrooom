from pathlib import Path
import hashlib
import json
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
sys.path.insert(0, str(ROOT / '10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

source = OUT / 'A_attempt_02/source.mp4'
preview = OUT / 'M03_continuous_distance_pose_A_v1.mp4'
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
result = subprocess.run([ffmpeg, '-hide_banner', '-y', '-i', str(source),
    '-map', '0:v:0', '-c:v', 'copy', '-an', '-movflags', '+faststart', str(preview)],
    capture_output=True, text=True, encoding='utf-8', errors='replace', check=True)
(OUT / 'preview_remux_log.txt').write_text(result.stderr, encoding='utf-8')
check = subprocess.run([ffmpeg, '-hide_banner', '-i', str(preview)], capture_output=True, text=True, encoding='utf-8', errors='replace')
assert 'Video: h264' in check.stderr and 'Audio:' not in check.stderr
decoded = scan(preview)
assert decoded['decoded_frames'] == 241
assert decoded['metadata']['size'] == (720, 1280) or decoded['metadata']['size'] == [720, 1280]
assert decoded['metadata']['fps'] == 24

protected = json.loads((ROOT / '10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8-sig'))
unchanged = []
for reel in protected['reels']:
    actual = sha(ROOT / reel['source_path'])
    assert actual == reel['sha256'], reel['model']
    unchanged.append({'model': reel['model'], 'source_path': reel['source_path'], 'sha256': actual, 'unchanged': True})

observations = {
    'review_method': 'All 241 whole-frame thumbnails covered; 25 larger whole-frame samples and five native face windows inspected. Not continuous normal-speed playback.',
    'motion': 'Near start; backward walking reveals shoes by about 2.5-3 seconds; full stance by about 3.3 seconds; turns toward side around 3.7-5 seconds; side hold through about 6.7 seconds; returns front around 7-8 seconds; front settle to end.',
    'background': 'Originally blank right wall stays blank in reviewed frames; no new window architecture detected. Left window, bench and floor broadly stable.',
    'identity_and_clothes': 'Recognizable face/hair and ivory blazer, white tee, navy trousers retained in reviewed views.',
    'hands_feet_bag': 'No obvious deformation seen at reviewed scales; far-side bag occlusion occurs during side stance and bag returns in front stance. Every frame was not separately reviewed as a native-resolution foot/bag crop.',
    'framing': 'Near start intentionally excludes lower legs; full outfit and shoes contained after retreat. No obvious source cut or zoom in reviewed geometry.',
    'limits': 'Actual side turn is deeper than planned oblique angle. Comfort, hold duration and normal-speed movement await user viewing; no success-rate claim.'
}
technical = OUT / 'A_attempt_02/technical_receipt.json'
receipt = json.loads(technical.read_text(encoding='utf-8'))
receipt['visual_review'] = 'sampled_review_candidate_usable_user_playback_pending'
receipt['review_observations'] = observations
receipt['continuous_playback'] = False
receipt['user_film_approval'] = None
save(technical, receipt)

save(OUT / 'preview_receipt.json', {
    'status': 'single_look_motion_preview_ready_user_review_pending',
    'source': source.relative_to(ROOT).as_posix(), 'source_sha256': sha(source),
    'preview': preview.relative_to(ROOT).as_posix(), 'preview_sha256': sha(preview),
    'processing': 'Video stream copy; remove all audio; faststart. No retime, crop, freeze, reverse, added text or transition.',
    'audio_streams_verified': 0, 'scan': decoded,
    'review_observations': observations, 'user_film_approval': None,
    'second_look': 'Planned only; depends on first-look playback and actual full-frame endpoint.',
    'original_five_w41_reels': unchanged,
    'external_mutations': {'drive': False, 'github': False, 'instagram': False}
})
story_path = OUT / 'storyboard.json'
story = json.loads(story_path.read_text(encoding='utf-8'))
story.update({'status': 'single_look_A_trial_ready_user_review_pending', 'grok_submission': True,
    'attempts': [{'id': 'A_attempt_01', 'result': 'rejected_new_windows_on_blank_right_wall'},
                 {'id': 'A_attempt_02', 'result': 'sampled_candidate_usable_user_playback_pending'}],
    'preview': preview.relative_to(ROOT).as_posix(), 'user_film_approval': None,
    'second_look_status': 'planned_pending_first_look_motion_review'})
save(story_path, story)

review = '''# M03 固定鏡頭・連續距離與姿態試片 A

這是第一套的單鏡動作試驗，尚未組成包含兩套的正式 Reel。

- 影片：`M03_continuous_distance_pose_A_v1.mp4`；720×1280、24fps、241幀，約10.04秒，無字無音。
- 動作：近距離起點 → 退至全身 → 側身 → 回正。人物走動改變距離，鏡頭保持固定。
- 第一輪：右側素牆長出窗戶，退件並保留原始檔及證據。
- 第二輪：沿用同一張使用者核准起始圖，強化素牆限制；抽查中未再出現新窗。
- 已檢視全部241幀的縮圖、25張較大的全畫面、5個原生臉部窗口；尚未由助手完整正常速度播放，也尚未獲使用者影片核准。
- 側身角度比原規劃更深；鞋包未逐幀以原生局部放大驗收。先由使用者觀看正常速度的舒服度與停留，再規劃第二套銜接。
- 後製只複製原影片串流、移除音訊及整理播放器索引，未改速度或人物動作。
- 第二套及0.75秒疊化尚未執行。原已交付五支影片的雜湊驗證未變，未上傳或覆蓋 Drive。

首輪送出前曾遇429自動審查回應，等待後在同一分頁恢復操作並正常生成；沒有改用其他瀏覽器繞過。
'''
(OUT / 'REVIEW.md').write_text(review, encoding='utf-8')
with (OUT / 'storyboard.md').open('a', encoding='utf-8') as f:
    f.write('\n\n## 實際執行結果（2026-10-12）\n\n使用者已核准精確近距離起始圖，核准見 `A_still_user_approval.json`。先前429中斷已在等待後於原分頁恢復。A1完成但因右牆新窗退件；同圖一次針對背景重試A2完成。A2的全部縮圖與關鍵畫面檢視可作觀看候選，正常速度舒服度與使用者影片核准仍待確認。乾淨10秒預覽、處理與保留原五支影片驗證見 `preview_receipt.json`；完整限制見 `REVIEW.md`。第二套仍只在規劃階段。\n')
status = ROOT / 'CURRENT_STATUS.md'
old = status.read_text(encoding='utf-8-sig')
heading = '# Current Status - Mira AI Fashion Creator\n'
assert old.startswith(heading)
entry = '''
## M03 continuous distance/pose A trial ready for user viewing — 2026-10-12

User approved the exact L01 near start. Grok A1 completed but was rejected for new windows on the blank right wall. One targeted same-still retry A2 completed; inspected frames retain the blank wall and show actual retreat to full outfit, side turn and return front. Clean single-look preview `03_research/reel_presentation_study_2026-10-12/continuous_distance_pose/M03_continuous_distance_pose_A_v1.mp4`:720×1280,24fps,241frames/~10.04s, video stream copied, audio removed, no text/retime/crop. All-frame thumbnails plus25 whole samples and5 native face windows reviewed; assistant continuous playback and user film approval remain pending. Deeper-than-planned side angle, hold comfort and native foot/bag details remain review limits. Second look and0.75s transition are planned, not generated/assembled. See `REVIEW.md` and `preview_receipt.json` in the same folder. Original five W41 delivered local films hash-verified unchanged; no Drive/GitHub/IG mutation. Earlier pending upload/still notes below are historical.

'''
status.write_text(heading + entry + old[len(heading):], encoding='utf-8')
print(json.dumps({'preview': str(preview), 'seconds': decoded['decoded_seconds'], 'audio_streams': 0, 'protected_films': len(unchanged)}, ensure_ascii=False))
