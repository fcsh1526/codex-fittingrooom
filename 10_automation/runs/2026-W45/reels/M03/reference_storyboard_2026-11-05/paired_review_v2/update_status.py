from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;B=P.parent;ROOT=B.parents[5];W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
film=P/'M03_W45_reference_parallel_review_v2.mp4';receipt=read(P/'edit_receipt.json');assert h(film)==receipt['film_sha256']
put(P/'user_continuation_2026-11-05.json',{'date':'2026-11-05','quote':'ok','scope':'Continue reviewing and adjusting displayed 9-second rough cut. Does not assert film or publication approval.','target_sha256':'cbf6d44706f77d0750497535ce08a14483b092ea4e2c4b2b3a81b1b5f1397e28'})
q=read(W/'production_queue.json');q.update(status='M03_reference_parallel_v2_pending_motion_review',active_reviews=[rel(film)],latest_edit_receipt=rel(P/'edit_receipt.json'),next={'model':'M03','action':'Review 8s original-speed paired candidate, particularly performance, skirt-side dwell, ending scale, and foot/hand continuity; exact film acceptance and publication remain separate.'});assert q['video_jobs_completed']==16 and q['weekly_reels_user_accepted']==2;put(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03');uid='USE_W45_M03_REFERENCE_PARALLEL_V2_20261105'
if not any(x['usage_id']==uid for x in reg['uses']):
 reg['uses'].append({'usage_id':uid,'series_id':'SERIES_W45_M03','production_date':'2026-11-05','status':'sampled_candidate_native_speed_review_pending','film_path':rel(film),'film_sha256':h(film),'receipt_path':rel(P/'edit_receipt.json'),'feedback_summary':'Original footage at original speed; skirt source starts one second later for closer approach timing. Earlier candidate preserved; full motion and user film acceptance pending.','user_acceptance_receipt':None,'publication_url':None});s['usage_ids'].append(uid)
s.update(status='reference_parallel_v2_pending_motion_review',latest_asset_receipt=rel(P/'edit_receipt.json'),current_reassessment=rel(P/'REVIEW.md'));put(regp,reg)
plan=read(B/'production_plan.json');plan['latest_trial']={'review_path':rel(P/'REVIEW.md'),'edit_receipt_path':rel(P/'edit_receipt.json'),'status':'sampled_candidate_native_speed_review_pending'};plan['missing_assets']=['原速完整動態審查、使用者成片接受與交接仍待完成。'];put(B/'production_plan.json',plan)
new='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03保留A並排及核准首圖；舊搖擺v4不採用，6.04秒natural版本依回饋退回企劃修正。使用者允許人物裁切後已做9秒初剪；後續ok接續檢查，用同一對原片將裙裝起點前移1秒、在8秒收尾，製成[雙欄v2候選](10_automation/runs/2026-W45/reels/M03/reference_storyboard_2026-11-05/paired_review_v2/REVIEW.md)。抽樣兩側末段較接近，裙裝正面全身展示少1秒、側身停留仍需評估；完整原速動態及成片接受未完成。累計七次靜態／十六支原片／兩支接受成片；M04–M05及proof／Carousel仍缺，M03未獲成片／發布核准。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');start=txt.index('W45現況：');end=txt.index('M03未獲成片／發布核准。',start)+len('M03未獲成片／發布核准。');txt=txt[:start]+new+txt[end:]
 txt=txt.replace('目前下一步：檢查M03新9秒雙欄初剪的原速表演、裙裝側停留與後半尺度差，按實際結果修整；不重貼舊6.04秒片待審。','目前下一步：檢查M03新8秒雙欄v2原速表演、裙裝側停留與末段尺度；不重貼舊6.04秒片待審。')
 txt=txt.replace('[雙欄初剪](reels/M03/reference_storyboard_2026-11-05/paired_review_v1/REVIEW.md)，原速表演及末段尺度差待檢查。','[雙欄初剪](reels/M03/reference_storyboard_2026-11-05/paired_review_v1/REVIEW.md)；後以原素材製作[8秒v2](reels/M03/reference_storyboard_2026-11-05/paired_review_v2/REVIEW.md)，原速表演仍待檢查。')
 p.write_text(txt,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snap:assert h(ROOT/item['snapshot_path'])==item['sha256']
for path,digest in [('reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4','aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb'),('reels/M02/trial_03/M02_W45_trial03_silent_review.mp4','bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67')]:assert h(W/path)==digest
assert h(B/'paired_review_v1/M03_W45_reference_parallel_review_v1.mp4')=='cbf6d44706f77d0750497535ce08a14483b092ea4e2c4b2b3a81b1b5f1397e28'
put(P/'verification.json',{'snapshots_verified':len(snap),'accepted_M01_M02_unchanged':True,'v1_unchanged':True,'new_generations':0,'publication_action':False})
print(json.dumps({'status':q['status'],'snapshots_verified':len(snap),'source_jobs':q['video_jobs_completed']}))
