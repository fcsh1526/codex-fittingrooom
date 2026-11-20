from pathlib import Path
import hashlib,json,csv
P=Path(__file__).resolve().parent;ROOT=P.parents[5];W=ROOT/'10_automation/runs/2026-W45';I=W/'generated_images/2026-W45-004/looks/2026-W45-004-L01/reel'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
film=P/'M04_W45_floral_single_review_v1.mp4';edit=read(P/'edit_receipt.json');assert h(film)==edit['film_sha256'];tech=read(P/'technical_review.json')
status='M04_single_floral_review_v1_pending_user_motion_review'
sub=read(P/'S01_submission.json');sub.update(status='downloaded_sampled_used_in_initial_edit',source_sha256=tech['source_sha256'],technical_review=rel(P/'technical_review.json'),edit_receipt=rel(P/'edit_receipt.json'));put(P/'S01_submission.json',sub)
receipt=read(I/'generation_receipt_face_v2.json');receipt.update(status='user_approved_for_motion',user_visual_approval='10_automation/runs/2026-W45/approvals/M04_L01_face_v2_still_approval_2026-11-06.json');put(I/'generation_receipt_face_v2.json',receipt)
sheet=I/'review_sheet.csv'
with sheet.open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
for row in rows:
 if row['candidate_file'].endswith('face_v2.png'):row.update(status='user_approved_for_motion',notes='User ok on 2026-11-06 confirms exact face-v2 starting still; no motion/full-film/publication approval inferred.')
with sheet.open('w',encoding='utf-8',newline='') as f:writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
q=read(W/'production_queue.json');assert q['builtin_image_calls']==9 and q['video_jobs_completed'] in (16,17) and q['weekly_reels_user_accepted']==2
q.update(status=status,video_jobs_submitted=17,video_jobs_completed=17,active_reviews=[rel(film)],active_trial=rel(P/'S01_submission.json'),latest_edit_receipt=rel(P/'edit_receipt.json'),latest_editorial_proposal=rel(P/'execution_plan.json'),next={'model':'M04','action':'Review exact8.54s full/detail/full initial cut at native speed, particularly face, motif consistency and both0.75s ghosted joins. Parallel editing remains paused.'});put(W/'production_queue.json',q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(rp);s=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M04');uid='USE_W45_M04_FLORAL_SINGLE_V1_20261106'
if not any(x['usage_id']==uid for x in reg['uses']):
 reg['uses'].append({'usage_id':uid,'series_id':'SERIES_W45_M04','production_date':'2026-11-06','status':status,'film_path':rel(film),'film_sha256':h(film),'source_asset_id':sub['uuid'],'source_sha256':tech['source_sha256'],'receipt_path':rel(P/'edit_receipt.json'),'feedback_summary':'One exact approved face-v2 still animated once. Full/detail/full8.54s original-speed initial cut, two0.75s dissolves with visible ghosting, digital motif detail at2x. Source and motion acceptance remain separate; no publication approval.','user_acceptance_receipt':None,'publication_url':None});s['usage_ids'].append(uid)
s.update(status=status,latest_asset_receipt=rel(P/'edit_receipt.json'),current_reassessment=rel(P/'REVIEW.md'),still_approval_receipts=['10_automation/runs/2026-W45/approvals/M04_L01_face_v2_still_approval_2026-11-06.json']);reg['updated_date']='2026-11-06';put(rp,reg)
execution=read(P/'execution_plan.json');execution.update(status=status,source_uuid=sub['uuid'],source_jobs_completed=1,source_sha256=tech['source_sha256'],observed_execution={'S01':{'execution_mode':'reuse_clip','source_frames':[0,96]},'S02':{'execution_mode':'reuse_clip','source_frames':[96,174],'crop':[185,250,360,640]},'S03':{'execution_mode':'reuse_clip','source_frames':[174,241]}},actual_film_seconds=205/24,observed_deviations=['window-look and sideways step not clear','digital detail crop replaces separately generated close source','film shorter due available unique footage and two dissolves','visible scale ghosting during joins']);put(P/'execution_plan.json',execution)
new='W45現況：左右比較剪輯依使用者指示暫停；記得的優秀雙欄參考不是Kubo，確切帳號未識別。M03的8秒v2退回，9秒v1相對較好但未接受發布。M04首圖face_v2已於11/6獲ok，使用同一精確核准圖及身份參照生成一支10.041667秒來源，組成[8.541667秒單畫面全身→花卉細節→全身初剪](10_automation/runs/2026-W45/reels/M04/production_2026-11-06/REVIEW.md)。細節為同原片2倍裁切，兩處0.75秒接點有明顯景別疊影；原速完整動態及成片接受尚待完成。累計九次靜態／十七支原片，M01／M02兩支已接受；M05及十套proof／Carousel未完成，無本週新交接或發布。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
 p=ROOT/name;txt=p.read_text(encoding='utf-8-sig');start=txt.index('W45現況：');stop=txt.index('\n',start);txt=txt[:start]+new+txt[stop:];txt=txt.replace('更新：2026-11-05','更新：2026-11-06',1)
 txt=txt.replace('目前下一步：左右比較剪輯暫停，轉做M04單畫面花卉穿搭，首圖逐張核准後才進影片；記得的參考不是Kubo。','目前下一步：M04 face_v2圖已核准；檢視新8.54秒單畫面初剪的表演、花紋和兩處接點疊影。左右比較仍暫停。')
 txt=txt.replace('九次靜態／十六支原片，M01／M02共兩支接受成片；','九次靜態／十七支原片，M01／M02共兩支接受成片；')
 txt=txt.replace('| M04 | 深底花卉只放上衣，下身素色；再讀花色與衣料 | 1 | 2 | 10秒 | [M04](planning/M04/SHOT_CARDS.md) |','| M04 | 深底花卉只放上衣，下身素色；再讀花色 | 1 | 2 | 初剪8.54秒 | [M04初剪](reels/M04/production_2026-11-06/REVIEW.md) |')
 p.write_text(txt,encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for item in snap:assert h(ROOT/item['snapshot_path'])==item['sha256']
for path,digest in [('reels/M01/paired_review_v1/M01_W45_two_looks_review_v1.mp4','aa1a657e88480a966226bdbf72ea3e5c46346290df154408d376ebcc2b27a2fb'),('reels/M02/trial_03/M02_W45_trial03_silent_review.mp4','bf1828d34ce61ac76e82d1573a49e85d8403d5a5ae9be9bb8be46c16fa114b67')]:assert h(W/path)==digest
put(P/'verification.json',{'date':'2026-11-06','immutable_snapshots_verified':len(snap),'accepted_M01_M02_preserved':True,'new_source_jobs':1,'new_stills':0,'source_sha256':tech['source_sha256'],'film_sha256':h(film),'publication_action':False,'IG_operations':0,'parallel_still_paused':True})
print(json.dumps({'status':status,'video_jobs_completed':17,'protected_snapshots':len(snap),'film_sha256':h(film)}))
