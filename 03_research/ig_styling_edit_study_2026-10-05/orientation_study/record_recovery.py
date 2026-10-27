"""Record actual source retrieval and separate candidate; preserve prior failures."""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

manifest=read(HERE/'research_manifest.json')
receipt=read(HERE/'M02_parallel_angle_review_v2.json')
if receipt.get('user_approval') or manifest.get('user_video_approval'):
    raise RuntimeError('Accepted cut already recorded; preserve acceptance instead of replaying recovery status.')
assert sha(ROOT/receipt['output'])==receipt['output_sha256']=='9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569'
for item in manifest['protected_first_wave']:
    assert sha(ROOT/item['path'])==item['sha256']
assert sha(HERE.parent/'simultaneous_comparison/M02_parallel_compare_review_v4_size_matched.mp4')=='a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'
assert sha(ROOT/'10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4')=='3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989'
recoveries=[]
for letter in ('A','B'):
    folder=HERE/f'grok_{letter}_recovery_01'
    source=read(HERE/f'qa/recovery_01/{letter}/inspection_receipt.json')
    assert sha(folder/'source.mp4')==source['source_sha256']
    recoveries.append(dict(folder=folder.name,submission=read(folder/'submission.json'),
                           retrieval=read(folder/'retrieval.json'),source_sha256=source['source_sha256'],
                           source_size=source['native_size'],native_fps=source['observed_fps'],
                           native_frames=source['decoded_frames'],
                           qa_receipt=f'qa/recovery_01/{letter}/inspection_receipt.json'))
receipt['assistant_sampled_review']='Root source25+face5 per look, sourceA f72 and B f84/f108 originals, output5 checkpoints and B critical f84 checked; independent source/output review recorded separately.'
receipt['sampled_limitations']=['B tote obscures lower shirt side; A bag partly obscures side.',
                                'Actual torso turn is more side-facing than nominal30degrees; exact angle not calibrated.',
                                'A turns around2.5–3s, B around4–4.5s; native phase difference retained.',
                                'New generated facial expressions differ; no sampled obvious identity swap; all-frame identity guarantee not claimed.']
write(HERE/'M02_parallel_angle_review_v2.json',receipt)
failed=read(HERE/'qa/output_v1_failed_scan.json')
write(HERE/'M02_parallel_angle_review_v1_failed.json',dict(status='failed_technical_qa_not_for_review',
       source_file='M02_parallel_angle_review_v1.mp4',scan=failed,
       issue='144frames but container/reported24.17fps and5.96s; rejected native-clock check.',
       resolution='Separate v2 uses explicit native24fps timebase/output rate and passes144frames/6s.',
       overwrite=False,user_approval=None))
manifest.update(recorded_at_local=datetime.now(timezone(timedelta(hours=8))).isoformat(),
    status='research_angle_candidate_pending_user_visual_approval',
    send_clicks_observed=5,generation_progress_observed_attempts=4,
    recovery_authority='User ok after proposal to diagnose submission/output before continuing trial.',
    recovery_attempts=recoveries,new_video_sources_retrieved=2,
    output=receipt['output'],output_sha256=receipt['output_sha256'],
    candidate_selected_seconds=6,usable_seconds=None,
    dynamic_qa={'complete_technical_decode':True,'source_checkpoints_per_look':25,
                'face_checkpoints_per_look':5,'output_checkpoints':5,'critical_output_checks':[24,84,143],
                'independent_review':'qa/recovery_01/independent_source_review.md',
                'assistant_continuous_playback':False,'user_visual_approval':None,
                'sampled_result':'No obvious sampled identity/wardrobe jump or major library warp; full normal-playback comfort pending.'},
    source_retrieval_current='Both new result IDs progressed to completed main players and downloaded before navigation.',
    earlier_failure_cause='unknown; recovery succeeded without changing approved stills or prompts. Causes such as prompt length or page navigation not proven.',
    failure_cause=None,next_operational_gate='User normal-speed full6s review of side-information utility, scale, background and comfort.',
    B_retry_not_started_reason=None,user_video_approval=None,
    protected_first_wave_unchanged=True,accepted_parallel_v4_unchanged=True,
    accepted_paired_11_25s_unchanged=True,cloud_writes=False,publication=False,
    global_format_adoption=False,audience_metrics=None)
write(HERE/'research_manifest.json',manifest)

review='''# M02 正面到側向同框試片：v2驗收

精確檔案：M02_parallel_angle_review_v2.mp4；SHA256：9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569。

兩段新Grok來源各720×1280、24fps、145幀，前144幀原速同時播放，成片6秒。固定相同窗口[135,0,490,1280]，各欄影像352×920、座標[4,180]；沒有追蹤縮放、動作同步、定格、倒放或文字音訊。此片沒有內部切鏡；後續新增切換仍約0.75秒疊化。

## 已完成

- 真正新結果A a720b96e-1dd6-4bbe-935c-a6f737114f57、B40176b8d-5bef-4711-a606-edf85d93a9d9，均停留結果頁直到完成及取片。保留先前失敗；根因未證實。
- 完整技術解碼；來源各25個全身抽查、5個臉部窗；原大圖轉向與包／裙襬最寬點；成片首／四分之一／中／四分之三／尾與f24、f84關鍵邊界抽查。
- 抽樣未見明顯換臉、服裝跳變或圖書館幾何扭曲，裙襬與包完整留在欄內。左右共同尺度適合這次來源，不沿用上版左欄3.69%修正。
- 原五支第一波、11.25秒配對D、核准6秒同框v4雜湊全部保持一致，沒有雲端寫入或發布。

## 實際內容與限制

轉向增加袖型、外層衣長和裙身側輪廓。實際比名義30度更側向，不能標定精確角度。A約2.5–3秒完成轉向、B約4–4.5秒，保留原生時間差。兩個包都遮住部分襯衫，B托特尤其遮下半側邊，不能宣稱完整展示側邊垂墜。

第一次匯出v1報24.17fps／5.96秒，未通過技術時序驗收；保留原檔與失敗記錄。獨立v2使用來源24fps時間基準與輸出率，144幀／6秒通過。此修正是匯出時序，人物動作與選片未改。

助手抽樣驗收與完整技術解碼已完成；沒有宣稱助手連續播放通過。使用者完整正常播放、視覺核准、可發版本與IG成效仍未取得。這是新角度的研究候選，不是通用格式或第一波替換。
'''
(HERE/'REVIEW.md').write_text(review,encoding='utf-8')

readme=HERE/'README.md'
text=readme.read_text(encoding='utf-8-sig')
heading='## 生成恢復與新候選（2026-10-05）'
new='''
## 生成恢復與新候選（2026-10-05）

使用者授權繼續診斷後，新畫布重新上傳相同核准full master，實際選Mira M02 v3與First frame、6秒／720p／9:16／音訊關閉，原提示詞不變。A/B各一次受控提交均建立新post、出現進度並完成，停留至取片後才離頁。兩段新來源已保存；先前失敗根因仍未知，不能據此斷言是離頁或提示長度造成。

獨立6秒候選 `M02_parallel_angle_review_v2.mp4` 完成，SHA256 `9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569`。共同固定窗口與等比例尺寸，保留原動作／速度、無字無音、無片內切換；完整技術解碼與來源／成片抽查見 `REVIEW.md`。实际偏側向而非已校準30度，A/B轉向不同時，包局部遮住側襯衫，以上限制保留。v1匯出時序失敗另留記錄；v2通過144幀／24fps／6秒。

使用者完整播放核准待回覆。沒有助手連續驗收、通用格式或曝光效果宣稱。原五支、核准v4與11.25秒配對D完整保留；未上傳、未替換或發布。下面「狀態」為先前失敗的歷史紀錄。
'''
if heading not in text:
    text=text.replace('## 狀態',new+'\n## 先前狀態（歷史）',1)
    readme.write_text(text,encoding='utf-8')

status=ROOT/'CURRENT_STATUS.md'
text=status.read_text(encoding='utf-8-sig')
note='''## Grok recovery succeeded; new M02 angle candidate pending user review — 2026-10-05

User authorized submission/output diagnosis after the unavailable-source report. One fresh A and one B submission, same approved masters/prompts and actual Mira M02 v3/First-frame/6s/720p/9:16/audio-off, each reached progress, completed and downloaded before leaving. Exact new sources: A a720b96e-1dd6-4bbe-935c-a6f737114f57, B40176b8d-5bef-4711-a606-edf85d93a9d9; each720×1280/24fps/145frames. Earlier failures preserved, cause unknown. Separate `03_research/ig_styling_edit_study_2026-10-05/orientation_study/M02_parallel_angle_review_v2.mp4`, SHA256 `9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569`, selects[0,144) each for6s parallel native motion. Same fresh fixed[135,0,490,1280] windows→352×920 rectangles; no historical A shrink, tracking, retime, text/audio or interior switch. Source25+face5 per look and output5+critical boundaries sampled, complete technical decode passes. Actual turn more side-facing than requested; A/B phase differs, bags partly hide shirt side. Independent review saved; assistant continuous pass/user approval/global adoption/IG effects not claimed. First v1 export failed native clock24.17fps/5.96s, retained; explicit24fps v2 passes. Protected first-wave five, acceptedv4 and11.25s paired hashes match; no cloud writes/publication. Next gate: user normal-speed full6s comfort/content review. Earlier unresolved note below is historical.

'''
if note.split('\n')[0] not in text:
    status.write_text(text.replace('\n\n','\n\n'+note,1),encoding='utf-8')

publishing=ROOT/'10_automation/runs/2026-W37/publishing_structure.md'
text=publishing.read_text(encoding='utf-8-sig')
pub='''**角度試片取片恢復（2026-10-05，待使用者完整播放核准）：** 相同核准圖／人物參照／提示詞，A/B各一次新提交都完成並下載；先前失敗根因仍未知。獨立6秒 `orientation_study/M02_parallel_angle_review_v2.mp4` 原速左右同框，新增側向袖型與裙身輪廓，實際轉向較大且不同時，包遮部分側襯衫。來源各25+臉5與成片5+關鍵邊界抽查、完整解碼完成，未宣稱助手連續播放通過／可發／曝光成效。原五支、核准v4、11.25秒配對D雜湊保留；未上傳、未覆蓋、未發布。下方「取片未解」是歷史。

'''
if '**角度試片取片恢復' not in text:
    publishing.write_text(text.replace('\n\n','\n\n'+pub,1),encoding='utf-8')
print(json.dumps(dict(status=manifest['status'],output=receipt['output'],protected_media_unchanged=True,cloud_writes=False),ensure_ascii=False))
