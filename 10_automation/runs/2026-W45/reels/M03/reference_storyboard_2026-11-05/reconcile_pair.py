from pathlib import Path
import hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent;ROOT=B.parents[5];W=ROOT/'10_automation/runs/2026-W45';P=B/'paired_review_v1';R=B/'L02_trial_01'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
movie=P/'M03_W45_reference_parallel_review_v1.mp4';receipt=read(P/'edit_receipt.json');assert sha(movie)==receipt['output_sha256']
sub=read(R/'submission.json');sub.update(status='downloaded_sampled',uuid='b6178fd0-12ed-4dc0-b3f8-3835f5c58e39',provider_first_reported='1499ae56-08c0-4503-b88f-898a373738e0',provider_identity_reported=['26e03f42-2907-488c-b75c-239a2a19b9c8','15c720b2-46b6-45e0-a150-60290e3290e6'],provider_settings_reported='10s,720p,9:16, no last/keyframes',internal_call_directly_observed=False);put(R/'submission.json',sub)
shot=read(R/'shot_plan.json');shot.update(status='downloaded_sampled',new_jobs_submitted=1,new_jobs_completed=1,output_uuid=sub['uuid'],technical_review=rel(R/'technical_review.json'));put(R/'shot_plan.json',shot)
plan=read(B/'production_plan.json');plan['generation_scope'].update(submitted=2,completed=2,status='two_sources_combined_rough_cut',new_stills_planned=0);plan['latest_trial']={'review_path':rel(P/'REVIEW.md'),'edit_receipt_path':rel(P/'edit_receipt.json'),'status':'rough_cut_sampled_pending_complete_motion_review'};plan['missing_assets']=['原速完整動態審查及雙欄末段尺度差仍待確認；新成片尚未獲接受或發布核准。'];put(B/'production_plan.json',plan)
q=read(W/'production_queue.json'); assert q['video_jobs_completed'] in (15,16)
q.update(status='M03_reference_parallel_rough_cut_sampled',video_jobs_submitted=16,video_jobs_completed=16,active_reviews=[rel(movie)],active_trial=rel(R/'submission.json'),latest_edit_receipt=rel(P/'edit_receipt.json'),next={'model':'M03','action':'Review 9s parallel rough cut at native speed, particularly unequal approach scale and skirt-side dwell; revise if necessary before film acceptance and handoff.'});put(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03')
for use in [{'usage_id':'USE_W45_M03_REFERENCE_L02_20261105','status':'source_sampled','film_path':read(R/'technical_review.json')['silent_path'],'source_asset_id':sub['uuid'],'source_sha256':sha(R/'source.mp4'),'receipt_path':rel(R/'submission.json'),'feedback_summary':'Skirt source after user allowed person cropping; side turn and approach are visible; full-speed motion acceptance pending.'},{'usage_id':'USE_W45_M03_REFERENCE_PARALLEL_V1_20261105','status':'rough_cut_sampled_pending_complete_motion_review','film_path':rel(movie),'film_sha256':sha(movie),'receipt_path':rel(P/'edit_receipt.json'),'feedback_summary':'9s parallel: original speeds, late subject scale differs; user permitted cropping only, no film or publication acceptance.'}]:
 if not any(x['usage_id']==use['usage_id'] for x in reg['uses']):
  use.update(series_id='SERIES_W45_M03',production_date='2026-11-05',user_acceptance_receipt=None,publication_url=None);reg['uses'].append(use);s['usage_ids'].append(use['usage_id'])
s.update(status='reference_parallel_rough_cut_sampled',latest_asset_receipt=rel(P/'edit_receipt.json'),current_reassessment=rel(P/'REVIEW.md'));put(regp,reg)
new='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03保留A並排及核准首圖；舊搖擺v4不採用，6.04秒natural版本依使用者回饋退回企劃修正。使用者確認人物可裁切並指示繼續後，新增一支裙裝來源，完成[9秒雙欄初剪](10_automation/runs/2026-W45/reels/M03/reference_storyboard_2026-11-05/paired_review_v1/REVIEW.md)。抽樣可見褲裝較早走近、後半兩側人物尺度差增加，原速整片與表演仍須檢查；裁切許可不等於成片接受。累計七次靜態／十六支原片／兩支接受成片；M04–M05及proof／Carousel仍缺，M03未獲成片／發布核准。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');start=txt.index('W45現況：');end=txt.index('M03未獲成片／發布核准。',start)+len('M03未獲成片／發布核准。');txt=txt[:start]+new+txt[end:]
 txt=txt.replace('目前下一步：檢視新L01完整10.04秒來源的表演，先用現有片解決末段雙欄裁頭／手及終點，未通過前不延伸裙裝；不重貼舊6.04秒片待審。','目前下一步：檢查M03新9秒雙欄初剪的原速表演、裙裝側停留與後半尺度差，按實際結果修整；不重貼舊6.04秒片待審。')
 txt=txt.replace('[新分鏡](reels/M03/reference_storyboard_2026-11-05/REVIEW.md)已獲ok並完成一次[褲裝實片](reels/M03/reference_storyboard_2026-11-05/L01_trial_01/REVIEW.md)；末段雙欄裁頭／手待調整，不批次生成裙裝。','[新分鏡](reels/M03/reference_storyboard_2026-11-05/REVIEW.md)已獲ok；使用者允許人物裁切後完成[雙欄初剪](reels/M03/reference_storyboard_2026-11-05/paired_review_v1/REVIEW.md)，原速表演及末段尺度差待檢查。')
 txt=txt.replace('七次靜態／十五支原片，M01／M02共兩支接受成片；M03新來源尚未接受，舊自然並排維持企劃修正。','七次靜態／十六支原片，M01／M02共兩支接受成片；M03新雙欄初剪尚未接受，舊自然並排維持企劃修正。');p.write_text(txt,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for x in snap:assert sha(ROOT/x['snapshot_path'])==x['sha256']
for path,digest in [('reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4','aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb'),('reels/M02/trial_03/M02_W45_trial03_silent_review.mp4','bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67')]:assert sha(W/path)==digest
put(P/'verification.json',{'protected_snapshots':len(snap),'accepted_M01_M02_unchanged':True,'new_video_sources':1,'new_stills':0,'new_IG_operations':0,'publication':False,'rough_cut_sha256':sha(movie)})
print(json.dumps({'status':q['status'],'video_jobs_completed':q['video_jobs_completed'],'protected_snapshots':len(snap)}))
