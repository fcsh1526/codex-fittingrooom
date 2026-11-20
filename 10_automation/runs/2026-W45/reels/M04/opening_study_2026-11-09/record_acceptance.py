from pathlib import Path
import json,hashlib
ROOT=Path.cwd();P=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
clip=P/'A_existing_source_opening_rough_v1.mp4'
edit=read(P/'rough_cut_receipt.json')
actual=hashlib.sha256(clip.read_bytes()).hexdigest()
assert actual==edit['output_sha256'],'Displayed file changed; do not attach acceptance.'
receipt={'actor':'user','decision':'approved','scope':'opening_appeal_and_continued_viewing','recorded_at':'2026-11-09','quote':'有，可以','preceding_question':'不靠上面的情節說明，你看到第三秒時，還想繼續看她嗎？','asset':clip.relative_to(ROOT).as_posix(),'target_sha256':actual,'seconds':5,'source_frames_half_open':edit['source_frames_half_open'],'interpretation':'User confirms the displayed A opening makes them want to continue watching; adopt this exact opening.','not_inferred':['IG audience retention results','Cause attributable separately to crop or start time','General repeatability','Full native-speed physical QA','Publication/handoff authorization for this version','Approval of B or C concepts'],'preserve_exact_edit':True}
rp=P/'user_opening_acceptance.json';put(rp,receipt)
edit['user_acceptance']={'scope':receipt['scope'],'receipt':rp.relative_to(ROOT).as_posix(),'quote':receipt['quote']};put(P/'rough_cut_receipt.json',edit)
plan=read(P/'opening_plan.json');plan['status']='A_opening_appeal_user_accepted';plan['selected_opening']='A';plan['selected_asset']=clip.relative_to(ROOT).as_posix();plan['acceptance_receipt']=rp.relative_to(ROOT).as_posix();plan['remaining_scope']='Preserve accepted opening; complete full-film motion/end review before release handoff. B/C remain proposals.';put(P/'opening_plan.json',plan)
qpath=ROOT/'10_automation/runs/2026-W45/production_queue.json';q=read(qpath)
q['status']='M04_A_opening_appeal_accepted_full_film_review_pending'
q['active_reviews']=[]
q['latest_performance_feedback']=rp.relative_to(ROOT).as_posix()
q['accepted_opening']={'asset':clip.relative_to(ROOT).as_posix(),'sha256':actual,'receipt':rp.relative_to(ROOT).as_posix()}
q['next']={'model':'M04','action':'Keep the exact accepted 5s A opening. Complete native-speed whole-film face/limb/clothing and ending review; do not reopen opening preference or regenerate merely for variety. Release approval remains separate.'}
assert q['weekly_reels_user_accepted']==2
put(qpath,q)
handoff={'date':'2026-11-09','model':'M04','content_week':'2026-W45','candidate':clip.relative_to(ROOT).as_posix(),'sha256':actual,'opening_appeal':'user_accepted','full_decode':True,'sampled_frames':'49 source frames reviewed in prior work; not native-speed continuous viewing','native_speed_full_film_visual_qa':'pending','whole_film_release_approval':'not_recorded','ready_for_release_handoff':False,'external_handoff_performed':False,'next':'Finish full-film physical and ending review while preserving accepted opening.','no_new_generation':True}
put(P/'handoff_readiness.json',handoff)
note='''
## 使用者回饋更新｜2026-11-09

使用者對「不靠情節說明，看到第三秒時是否仍想繼續看」回覆「有，可以」。A五秒精確版本的開場吸引力已接受，保留目前起點、構圖與原速節奏，不再重問同一項觀看偏好。收據：`user_opening_acceptance.json`，雜湊與剪輯收據一致。此前文中的待使用者回饋狀態於此範圍內已解除。

接下來檢查完整動態與收尾；不為湊長度加鏡頭，不直接套入B/C。這次接受不表示已取得IG成效、證明哪一個剪輯變因造成改善，或獲得發布授權。發布準備記錄見`handoff_readiness.json`，尚未交外部發布區。
'''
review=P/'REVIEW.md';t=review.read_text(encoding='utf-8')
if '## 使用者回饋更新｜2026-11-09' not in t:review.write_text(t+note,encoding='utf-8')
update='2026-11-09最新回饋：使用者對M04五秒A開場回覆「有，可以」，確認看到第三秒仍願意繼續看。精確版本已鎖定，開場吸引力已接受；不重開同項偏好確認。接續完整動態／收尾檢查，尚未推定成片發布核准。收據：`10_automation/runs/2026-W45/reels/M04/opening_study_2026-11-09/user_opening_acceptance.json`。以下較早的開場待回饋狀態僅在本範圍被取代。\n\n'
for rel in ['10_automation/CANONICAL_WORKFLOW.md','CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/rel;t=p.read_text(encoding='utf-8-sig')
    if update not in t:
        title,tail=t.split('\n',1);p.write_text(title+'\n\n'+update+tail.lstrip('\n'),encoding='utf-8')
print(json.dumps({'opening_acceptance_saved':True,'sha256':actual,'media_modified':False,'publication_performed':False},ensure_ascii=False))
