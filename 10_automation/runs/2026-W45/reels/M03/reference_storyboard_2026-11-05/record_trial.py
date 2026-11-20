"""Reconcile the completed single-source experiment without changing accepted films."""
from pathlib import Path
import json,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
B=Path(__file__).resolve().parent;ROOT=B.parents[5];P=B/'L01_trial_01';W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
t=read(P/'technical_review.json');sub=read(P/'submission.json')
assert sub['uuid']=='fad9518f-bbd0-4f68-a9c3-0351bb7b3440'
assert sha(P/'source.mp4')==t['source_sha256']
status='source_trial_review_ready_panel_framing_requires_revision'
qa={'date':'2026-11-05','status':status,'source_uuid':sub['uuid'],'source_sha256':t['source_sha256'],
 'reference_development':'partially_observed: waist stance, deeper side/back angle, return and approach',
 'prompt_deviations':['side/back rather than three-quarter','small pivot rather than clear diagonal travelling step','more than two approach steps','end tighter than head-through-knees'],
 'planned_panel_fit':'failed: hair near top at7.75–8s; clear hair and hand clipping from sampled8.25s; severe9–10s',
 'sampled_body_continuity':'No obvious disconnected hand or shoe found in reviewed samples; not proof of zero sliding or temporal naturalness.',
 'native_speed_continuous_review':False,'browser_playback_evidence':'browser_playback_samples.json',
 'user_source_acceptance':None,'user_full_film_acceptance':None,'publication_approval':None,
 'next':'Review exact full source performance; compare existing-source framing/endpoint locally before any skirt generation or retry.'}
put(P/'visual_review.json',qa)
sub.update(status=status,review_receipt=rel(P/'visual_review.json'));put(P/'submission.json',sub)
shot=read(P/'shot_plan.json');shot.update(status=status,new_jobs_submitted=1,new_jobs_completed=1,output_uuid=sub['uuid'],provider_controls_evidence=rel(P/'provider_report.txt'),actual_media=t);put(P/'shot_plan.json',shot)
plan=read(B/'production_plan.json');plan['status']='in_review'
plan['generation_scope'].update(submitted=1,completed=1,status=status,first_test='Completed exact L01 once; L02 and retries not submitted.')
plan['missing_assets']=['單側實片已完成；原案雙欄末段裁頭／手，取景與完整原速動態尚未通過。']
plan['latest_trial']={'receipt_path':rel(P/'submission.json'),'review_path':rel(P/'REVIEW.md'),'status':status}
put(B/'production_plan.json',plan)

rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp)
s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03');uid='USE_W45_M03_REFERENCE_L01_TRIAL01_20261105'
new_use=not any(x['usage_id']==uid for x in reg['uses'])
if new_use:
 reg['uses'].append({'usage_id':uid,'series_id':'SERIES_W45_M03','production_date':'2026-11-05','status':status,
  'film_path':t['silent_path'],'film_sha256':t['silent_sha256'],'source_asset_id':sub['uuid'],'source_sha256':t['source_sha256'],
  'receipt_path':rel(P/'submission.json'),'feedback_summary':'Assistant: three-stage presentation partly visible; deeper side turn and excessive approach cause late hair/hand clipping in proposed narrow panel. Exact source awaits user feedback; no second look or publication approval.',
  'user_acceptance_receipt':None,'publication_url':None})
 s['usage_ids'].append(uid)
s.update(status=status,latest_asset_receipt=rel(P/'submission.json'),current_reassessment=rel(P/'REVIEW.md'))
reg['updated_date']='2026-11-05';put(rp,reg)
q=read(W/'production_queue.json')
if new_use:
 assert q['video_jobs_submitted']==14 and q['video_jobs_completed']==14
 q['video_jobs_submitted']+=1;q['video_jobs_completed']+=1
q.update(status='M03_'+status,active_reviews=[t['silent_path']],active_trial=rel(P/'submission.json'),
 next={'model':'M03','action':'Review exact10.04s L01 trial performance; fix actual panel framing/endpoint with existing source before L02 or further generation.'})
assert q['builtin_image_calls']==7 and q['weekly_reels_user_accepted']==2
put(W/'production_queue.json',q)

new='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03保留A並排及原核准首圖；舊搖擺v4不採用、6.04秒natural版本依使用者回饋退回企劃修正。使用者已對新9秒連接分鏡／節奏示意回覆ok，現完成一次L01褲裝10.041667秒實片：腰側起勢→側向展示→回正靠近已部分呈現，但側轉偏深、走近超過預期，原雙欄窗口8.25秒起抽樣明顯裁頭／手。完整原片供表演檢視，尚未延伸裙裝或重抽；先用現有片檢查取景／終點。精確結果見 `10_automation/runs/2026-W45/reels/M03/reference_storyboard_2026-11-05/L01_trial_01/REVIEW.md`。累計七次靜態／十五支原片／兩支接受成片；M04–M05及proof／Carousel仍缺，M03未獲成片／發布核准。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');start=txt.index('W45現況：');end=txt.index('M03未獲成片／發布核准。',start)+len('M03未獲成片／發布核准。');txt=txt[:start]+new+txt[end:]
 txt=txt.replace('目前下一步：M03新9秒線稿／構圖節奏示意已完成，檢視具體內容發展與末段靠近／輕抬鏡後，先單側測試；不重貼舊6.04秒片待審。','目前下一步：檢視新L01完整10.04秒來源的表演，先用現有片解決末段雙欄裁頭／手及終點，未通過前不延伸裙裝；不重貼舊6.04秒片待審。')
 txt=txt.replace('[新9秒分鏡與預檢](reels/M03/reference_storyboard_2026-11-05/REVIEW.md)已完成，先看具體內容發展及靠近取景，再做單側測試。','[新分鏡](reels/M03/reference_storyboard_2026-11-05/REVIEW.md)已獲ok並完成一次[褲裝實片](reels/M03/reference_storyboard_2026-11-05/L01_trial_01/REVIEW.md)；末段雙欄裁頭／手待調整，不批次生成裙裝。')
 txt=txt.replace('七次靜態／十四支原片，M01／M02共兩支接受成片；M03自然並排未接受。','七次靜態／十五支原片，M01／M02共兩支接受成片；M03新來源尚未接受，舊自然並排維持企劃修正。')
 p.write_text(txt,encoding='utf-8')
p=B/'REVIEW.md';txt=p.read_text(encoding='utf-8')
notice='> 最新進度：使用者對下列已展示分鏡／示意回覆「ok」後，已完成一次L01來源；內容發展部分成立，但末段超出原雙欄範圍。詳 [單側實測](L01_trial_01/REVIEW.md)。下文「未生成／待線稿回饋」為製作前紀錄，由本段及精確新收據取代。\n\n'
if notice not in txt:txt=txt.replace('2026-11-05。',notice+'2026-11-05。',1);p.write_text(txt,encoding='utf-8')

snapshots=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snapshots:assert sha(ROOT/item['snapshot_path'])==item['sha256']
protected={'reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4':'aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb','reels/M02/trial_03/M02_W45_trial03_silent_review.mp4':'bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67','reels/M03/natural_parallel_2026-11-05/paired_review_v1/M03_W45_natural_parallel_review_v1.mp4':'13cd4260052fb452e396d2293874e0fa7496b0dfee868c8702e4c004621d072c'}
for name,digest in protected.items():assert sha(W/name)==digest
put(P/'verification.json',{'date':'2026-11-05','immutable_snapshots_verified':len(snapshots),'accepted_films_unchanged':True,'old_M03_unchanged':True,'new_Grok_jobs':1,'new_stills':0,'weekly_source_jobs':q['video_jobs_completed'],'weekly_accepted_reels':2,'source_sha256':t['source_sha256'],'review_sha256':t['silent_sha256'],'new_IG_tabs':0,'IG_operations':0,'new_service_or_purchase':False,'publication_action':False})
print(json.dumps({'status':status,'source_jobs':q['video_jobs_completed'],'protected_snapshots':len(snapshots),'source_uuid':sub['uuid']}))
