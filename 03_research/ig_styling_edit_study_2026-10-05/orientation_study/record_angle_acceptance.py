"""Record exact user-approved angle cut and its native staggered turns."""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def insert_after_title(path,marker,note):
    text=path.read_text(encoding='utf-8-sig')
    if marker not in text:
        path.write_text(text.replace('\n\n','\n\n'+note+'\n\n',1),encoding='utf-8')

receipt=read(HERE/'M02_parallel_angle_review_v2.json')
manifest=read(HERE/'research_manifest.json')
expected='9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569'
assert receipt['output_sha256']==expected==sha(ROOT/receipt['output'])
for r in manifest['protected_first_wave']:
    assert sha(ROOT/r['path'])==r['sha256']
assert sha(HERE.parent/'simultaneous_comparison/M02_parallel_compare_review_v4_size_matched.mp4')=='a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'
assert sha(ROOT/'10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4')=='3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989'
approval_path=HERE/'user_approval_angle_v2.json'
approval=read(approval_path) if approval_path.exists() else dict(
    decision='accepted_clean_picture_track',
    user_reply='恩 ，不錯。一開始兩邊沒有同步轉身，但是再看第二次後反而覺得不錯',
    recorded_at_local=datetime.now(timezone(timedelta(hours=8))).isoformat(),
    context='Direct feedback on the complete6s angle-v2 preview. User explicitly mentions a second viewing.',
    output_path=receipt['output'],output_sha256=expected,
    scope='This exact independent research cut, including its native staggered turns.',
    user_feedback={'first_impression':'Noticed the sides did not turn synchronously.',
                   'second_impression':'Felt the result was good after looking again.',
                   'reported_second_viewing':True,
                   'full_duration_and_playback_speed_explicitly_confirmed':False},
    action_timing_decision='Retain the native A-earlier/B-later turns; do not retime to synchronize this accepted cut.',
    assistant_continuous_review_claimed=False,account_wide_style_adoption=False,
    first_wave_replacement_authorized=False,cloud_upload_performed=False,
    publication_performed=False,audience_performance=None)
assert approval['output_sha256']==expected
write(approval_path,approval)
receipt.update(status='accepted_research_clean_picture_track',user_approval=approval,
               accepted_picture_seconds=6,publishable=False)
write(HERE/'M02_parallel_angle_review_v2.json',receipt)
manifest.update(status='accepted_research_clean_picture_track',user_video_approval=approval,
                accepted_picture_seconds=6,
                next_operational_gate='Preserve this accepted cut; continue comparative camera/edit research from each clothing topic. Publication/music/interface assembly and IG metrics remain separate.',
                global_format_adoption=False,cloud_writes=False,publication=False)
manifest['dynamic_qa']['user_visual_approval']='user_approval_angle_v2.json'
manifest['dynamic_qa']['user_reported_second_viewing']=True
manifest['dynamic_qa']['user_explicit_full_duration_speed_confirmation']=False
write(HERE/'research_manifest.json',manifest)

note='''## 此版已核准（2026-10-05）

使用者原話：「恩 ，不錯。一開始兩邊沒有同步轉身，但是再看第二次後反而覺得不錯」。核准精確6秒 `M02_parallel_angle_review_v2.mp4`，SHA256 `9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569`；收據 `user_approval_angle_v2.json`。保留A先轉、B後轉的原生節奏，不改速強制同步。

使用者明示第二次觀看，未逐項確認完整時長、播放速度或每項QA。此支乾淨研究畫面已accepted；下方待核准描述是歷史。錯開動作可列為後續同框的可選手法，沒有固定秒差或五位通用格式決定；也未證明IG留存或曝光。包遮住部分襯衫側邊、实际偏側向、尺寸與姿態的暫時差異仍保留。

原五支第一波、核准同框v4與11.25秒配對D均核對雜湊一致；没有雲端寫入、替換或發布。音樂與發布版另行確認。'''
for name in ('README.md','REVIEW.md'):
    insert_after_title(HERE/name,'## 此版已核准（2026-10-05）',note)

status_note='''## M02 angle-v2 accepted; native staggered turns retained — 2026-10-05

User feedback on the exact6s angle-v2: `恩 ，不錯。一開始兩邊沒有同步轉身，但是再看第二次後反而覺得不錯`. Accepted clean picture at `03_research/ig_styling_edit_study_2026-10-05/orientation_study/M02_parallel_angle_review_v2.mp4`, SHA256 `9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569`. User reports second viewing and favorable reassessment of staggered turns; retain original action/time phase. No forced synchronization, retime, text/audio or file replacement. Approval/receipt/manifest/README/REVIEW updated; optional staggered-motion lesson added to Reel SOP, not a fixed delay or global format. Full-duration/speed self-report and assistant continuous pass not inferred. Bag obstruction and uncalibrated side-facing angle remain. Protected first-wave five, acceptedv4 and11.25s paired hashes verified unchanged; no cloud write/publication/IG effect. Prior pending notes below are historical.'''
insert_after_title(ROOT/'CURRENT_STATUS.md','## M02 angle-v2 accepted; native staggered turns retained',status_note)

pub_note='''**M02側向同框v2畫面核准（2026-10-05）：** 使用者評「不錯」，指出初看未同步轉身、第二次看反而覺得不錯。核准精確6秒 `orientation_study/M02_parallel_angle_review_v2.mp4`；SHA256及原話見 `user_approval_angle_v2.json`。保留A先／B後的原動作、速度與無字無音。可選錯開節奏不定固定秒差，不推定五位通用格式或IG成效。原五支、同框v4、11.25秒配對D雜湊保留；未上傳、未替換或發布。下方待核准為歷史。'''
insert_after_title(ROOT/'10_automation/runs/2026-W37/publishing_structure.md','**M02側向同框v2畫面核准',pub_note)

handoff=ROOT/'10_automation/runs/2026-W37/reels/W37_REEL_HANDOFF.md'
text=handoff.read_text(encoding='utf-8-sig')
section='''## 新增本機研究版：M02正面到側向同框（2026-10-05已核准）

[6秒側向同框v2](../../../../03_research/ig_styling_edit_study_2026-10-05/orientation_study/M02_parallel_angle_review_v2.mp4)：原生A先轉、B後轉，增加袖型與裙身輪廓；共同固定尺寸，原動作／速度、無字無音、無片內切鏡。使用者初看注意不同步，第二次看評為不錯，核准此支研究畫面；精確檔案與原話見同資料夾 `user_approval_angle_v2.json`。

保留包遮部分側襯衫與兩套轉向時間差。未上傳、未替換上方第一波五支、未發布；音樂與發布版另外組裝。此核准未指定全部五位採同框或固定轉向時間差。

'''
if section.split('\n')[0] not in text:
    handoff.write_text(text.replace('## 發布方法',section+'## 發布方法',1),encoding='utf-8')

sop=ROOT/'09_sops/mira_reel_production_sop.md'
text=sop.read_text(encoding='utf-8-sig')
lesson='''2026-10-05側向同框v2補記：使用者核准6秒 `orientation_study/M02_parallel_angle_review_v2.mp4`，原話指出初看兩邊未同步轉身、再看第二次反而覺得不錯。本例保留A較早、B較晚的原生轉向；同框可容許動作錯開，作為依次觀看兩套的可選節奏。此解釋是編輯推論，使用者沒有說明注意力機制；不得據此固定秒差、強制每支錯開、宣稱留存更好或改速製造同步。兩邊仍需服裝清楚、共同觀看角度與相近尺度；本例側向偏大，包遮部分側襯衫的限制仍記錄。核准範圍只含精確研究畫面，原五支發布影片保持原版。\n\n'''
if '2026-10-05側向同框v2補記' not in text:
    marker='### 2026-10-05 M02核准的兩段連續鏡頭選項'
    sop.write_text(text.replace(marker,lesson+marker,1),encoding='utf-8')
print(json.dumps(dict(status=receipt['status'],native_staggered_turns_retained=True,
                      protected_media_unchanged=True,cloud_write=False),ensure_ascii=False))
