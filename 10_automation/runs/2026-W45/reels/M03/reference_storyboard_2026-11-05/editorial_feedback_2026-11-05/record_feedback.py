from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent; B=P.parent; ROOT=B.parents[5]; W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
v1=B/'paired_review_v1/M03_W45_reference_parallel_review_v1.mp4';v2=B/'paired_review_v2/M03_W45_reference_parallel_review_v2.mp4'
assert h(v1)=='cbf6d44706f77d0750497535ce08a14483b092ea4e2c4b2b3a81b1b5f1397e28'
assert h(v2)=='e47629d64faac82d0aade06ab729af623eea6992851af04cc0ec31f7efd519eb'
f={'date':'2026-11-05','actor':'user','quote':'不行，新剪的不行。上一版比較好。這一型態左右比較的，好像沒辦法像其他IG帳號的reel','target_rejected':rel(v2),'target_rejected_sha256':h(v2),'preferred_over_rejected':rel(v1),'preferred_sha256':h(v1),'scope':'v2 rejected; v1 relative preference, not film or publication acceptance. Concern about whether this comparison format can feel like referenced IG Reels; no universal prohibition inferred.'}
put(P/'user_feedback.json',f)
for file,status in [('paired_review_v2/edit_receipt.json','user_rejected'),('paired_review_v1/edit_receipt.json','user_preferred_to_v2_not_film_approved')]:
 p=B/file;x=read(p);x.update(status=status,latest_feedback_receipt=rel(P/'user_feedback.json'));put(p,x)
q=read(W/'production_queue.json');q.update(status='M03_user_rejected_v2_preferred_v1_editorial_reassessment',active_reviews=[],latest_performance_feedback=rel(P/'user_feedback.json'),latest_edit_receipt=rel(B/'paired_review_v1/edit_receipt.json'),next={'model':'M03','action':'Develop clear shared comparison beats and reference-specific acting, evaluate existing sources before any new material. Preserve v1 as relative favorite, not published.'});assert q['video_jobs_completed']==16 and q['weekly_reels_user_accepted']==2;put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp);s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03')
for uid,status,summary in [('USE_W45_M03_REFERENCE_PARALLEL_V1_20261105','user_preferred_to_v2_not_film_approved','User prefers v1 over v2 but raises wider concern about split-screen IG feel; no publication approval.'),('USE_W45_M03_REFERENCE_PARALLEL_V2_20261105','user_rejected','User rejects new 8s recut; prefers previous 9s version and questions whether this comparison feels like IG references.')]:
 u=next(x for x in reg['uses'] if x['usage_id']==uid);u.update(status=status,feedback_summary=summary,latest_feedback_receipt=rel(P/'user_feedback.json'))
s.update(status=q['status'],current_reassessment=rel(P/'REVIEW.md'),latest_performance_feedback=rel(P/'user_feedback.json'));put(rp,reg)
plan=read(B/'production_plan.json');plan['latest_trial']={'review_path':rel(P/'REVIEW.md'),'feedback_path':rel(P/'user_feedback.json'),'status':q['status']};plan['missing_assets']=['重新設計有共同觀看節奏的動作並評估素材，完整動態審查及成片接受尚待完成。'];put(B/'production_plan.json',plan)
new='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03保留A並排及核准首圖；使用者否決最新8秒v2，表示較喜歡先前9秒v1，並質疑目前左右比較未達其他IG Reel的感受。這是相對偏好，不等於v1可發布。已重新對照先前Kubo雙欄與leeharin姿態抽樣，發現既有記錄對Kubo取樣範圍的敘述不完整；下步回到共同觀看節奏與表演設計，先評現有素材，詳見 `10_automation/runs/2026-W45/reels/M03/reference_storyboard_2026-11-05/editorial_feedback_2026-11-05/REVIEW.md`。累計七次靜態／十六支原片／兩支接受成片；M04–M05及proof／Carousel仍缺，M03未獲成片／發布核准。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');start=txt.index('W45現況：');end=txt.index('M03未獲成片／發布核准。',start)+len('M03未獲成片／發布核准。');txt=txt[:start]+new+txt[end:]
 txt=txt.replace('目前下一步：檢查M03新8秒雙欄v2原速表演、裙裝側停留與末段尺度；不重貼舊6.04秒片待審。','目前下一步：依使用者否決8秒v2及對IG感受的回饋，回到共同觀看節奏與表演設計，先評既有素材；9秒v1相對較好但非發布核准。')
 txt=txt.replace('後以原素材製作[8秒v2](reels/M03/reference_storyboard_2026-11-05/paired_review_v2/REVIEW.md)，原速表演仍待檢查。','後以原素材製作[8秒v2](reels/M03/reference_storyboard_2026-11-05/paired_review_v2/REVIEW.md)遭否決，9秒v1相對較好；[回饋及參考對照](reels/M03/reference_storyboard_2026-11-05/editorial_feedback_2026-11-05/REVIEW.md)記錄後續設計。')
 p.write_text(txt,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snap:assert h(ROOT/item['snapshot_path'])==item['sha256']
for path,digest in [('reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4','aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb'),('reels/M02/trial_03/M02_W45_trial03_silent_review.mp4','bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67')]:assert h(W/path)==digest
put(P/'verification.json',{'snapshots_verified':len(snap),'both_new_versions_preserved':True,'accepted_M01_M02_unchanged':True,'new_generation':0,'IG_operations':0,'publication':False})
print(json.dumps({'status':q['status'],'snapshots_verified':len(snap)}))
