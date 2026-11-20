"""Reconcile the exact M03 review and approvals without changing approved snapshots."""
import csv,hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
pair=HERE/'paired_review_v1';edit=read(pair/'edit_receipt.json')
assert edit['output_sha256']=='40f4644211ab5cac5f42a4be4bd361f66349df35f70e76bc94e7ddee4a62b6f3'
assert sha(pair/edit['output_file'])==edit['output_sha256']
approvals={}
for name in ['M01_L01','M01_L02','M03_L01','M03_L02']:
    p=W/f'approvals/{name}_still_approval_2026-11-04.json';r=read(p)
    target=r.get('asset_path',r.get('target_path'))
    if target is None:target=r['path']
    expected=r.get('target_sha256',r.get('sha256'))
    assert sha(ROOT/target)==expected,name
    approvals[name]=(p,r,target)
snapshot=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for a in snapshot:assert sha(ROOT/a['snapshot_path'])==a['sha256']
for trial in ['L01_trial_01','L01_trial_02','L02_trial_01']:
    integrity=read(HERE/trial/'prompt_integrity.json');assert integrity['prompt_match_whitespace_normalized']
    s=read(HERE/trial/'submission.json');assert s['video_asset_id'] in integrity['post_url']
    assert any(s['video_asset_id'] in v['src'] for v in integrity['media'])

v1={"date":"2026-11-04","result":"selected_for_exact_source_frames_0_96_and_user_whole_film_review","sampled_seconds":[i*.5 for i in range(13)],"observations":["In sampled selected 0–4 s, complete hair/shoes remain visible and no forward/retreat translation of trial01 is seen.","Smile develops into a laugh with small shoulder/head movement, hands low. Late head tilt after about4.25 s is excluded from the selected range.","Clothing and office scene remain broadly coherent in samples; these observations are not a zero-error physical certification."],"full_file_decode":"completed","continuous_human_visual_review":False,"native_ui_observation":"Exact source post observed playing at1x; intermittent observations only, not uninterrupted visual review.","user_acceptance":None,"publication_approval":None}
write(HERE/'L01_trial_02/visual_review.json',v1)
v2={"date":"2026-11-04","result":"selected_as_coherent_approach_variant_for_user_film_review_not_camera_only_success","sampled_seconds":[i*.5 for i in range(21)],"observations":["Full outfit and sneakers readable initially; two small forward steps appear around2.5–3.5 s.","Framing tightens during about3–5 s, reaching head-to-mid-thigh medium by about5 s. This combines subject movement and framing change, not the requested stationary actor with camera-only approach.","Shoe cropping begins around3.5 s in source; by then the initial full look has had about2.75 s clear after the dissolve. Planned3.25 s hold and exact camera calibration were not achieved.","Head stays complete, medium lapels/cream neckline/waist/bag readable. Sampled medium has no obvious extreme head enlargement; precise lens/body reconstruction unverified.","Natural mouth/expression changes retained; small-step foot physics need native-speed user review."],"continuous_human_visual_review":False,"native_ui_observation":"Exact source post playing at1x observed intermittently; not uninterrupted visual review.","user_acceptance":None,"publication_approval":None}
write(HERE/'L02_trial_01/visual_review.json',v2)
for trial in ['L01_trial_02','L02_trial_01']:
    p=HERE/trial/'submission.json';s=read(p);s['status']='selected_source_for_paired_v1_user_review';s['paired_review']=rel(pair/edit['output_file']);write(p,s)

review={"date":"2026-11-04","status":"whole_film_candidate_pending_user_review","film_path":rel(pair/edit['output_file']),"film_sha256":edit['output_sha256'],"duration_seconds":10.5,"frame_count":252,"fps":24,"raster":[720,1280],"viewer_purpose":"Same navy soft blazer, charcoal work trousers versus cream A-line skirt/sneakers, then readable neckline/lapels in medium.","source_A":"L01_trial_02 [0,96)","source_B":"L02_trial_01 [0,174)","reviewed_samples":{"whole_film":"22 frames at0.5 s intervals plus finalframe","join":"3.0–4.25 s, every2frames inside18frame overlap","approach":"5.5–9.0 s at0.25 s intervals","proof":"L02 source f144 inspected at native720x1280"},"observations":["Work trouser and skirt/sneaker silhouettes visibly differ; full-person size broadly matches outside expression movement.","3.25–4.0 s dissolve retains double facial contours, hands and trouser/skirt transparency. This is a visible transition limitation, not marked seamless.","L02 supplies a continuous approach to medium, including small subject steps. Not a camera-only method validation.","Late medium preserves full hair and readable blazer neckline/waist/bag in sampled frames."],"technical":{"full_decode":"completed","native_source_mapping":"234 unblended frames checked, encoder-loss tolerance passed","speed":1,"retiming":False,"freeze":False,"crop":False,"text":False,"audio":False},"continuous_human_visual_review":False,"native_dynamic_review_status":"required before publish-ready; UI1x source observations and sampled sequence only, no uninterrupted assistant full-film visual review claimed","user_film_acceptance":None,"publication_approval":None,"external_delivery":None,"next":"Present exact candidate for normal-speed user review; no additional generation queued for this M03 mechanism."}
write(pair/'visual_review.json',review)
(pair/'REVIEW.md').write_text('''# W45 M03｜同件西外，工作到赴約

2026-11-04。精確10.5秒、252格、720×1280／24fps、無音原速審閱版，尚待使用者整片接受，未交接或發布。

- 0–3.25秒：直褲完整造型與站姿笑容；來源L01 trial02[0,96)，不用前進再退回的trial01。
- 3.25–4秒：一次0.75秒疊化換裙裝。臉、手與裙褲有短暫雙輪廓／透明重疊，原速舒適度待看。
- 4–約6.75秒：淺裙與球鞋完整可讀；其後走近並連續變為中景，約8.25秒起看領片、內搭、腰與肩包。

L02實際含小步走近，沒有達成「人物不動、純相機推近」；它是本片可審的合理表演變體，不列精準相機控制或站姿機制成功。L01修正版抽樣站位較穩，未宣稱零腳部誤差。

已完成原檔／整片解碼、無音影格等同性、234個非疊化影格來源對應及整片／接點／靠近的畫面抽樣。Grok精確網址、媒體UUID與可見prompt逐一對齊。工具解碼、抽樣、間歇1倍速來源觀測，均不冒充連續人工全片動態審查；該項與使用者接受仍待完成。

中景服裝核對影格來自L02原片第144格，沒有生成新圖、裁切或放大；血緣見proof_frame_lineage.json。這不補成獨立Carousel，也不自動新增新圖／發布核准。

本輪新增一張L02首圖、三支原片（L01一次失敗＋一次修正、L02一次）。W45累計七次內建靜態呼叫、八支原片、兩支接受影片；M03為第三支審閱候選。M04–M05／十套proof和Carousel仍有缺件。

影片：M03_W45_two_looks_review_v1.mp4  
SHA256：40f4644211ab5cac5f42a4be4bd361f66349df35f70e76bc94e7ddee4a62b6f3
''',encoding='utf-8')

q=read(W/'production_queue.json')
q.update(status='M01_M02_accepted_M03_paired_v1_pending_user_review',stills_generated=7,builtin_image_calls=7,video_jobs_submitted=8,video_jobs_completed=8,weekly_reels_user_accepted=2,stills_note='Seven builtin still calls: M02 two, M01 two, M03 L01 two including framing correction and L02 one. Five exact look sources approved, not seven complete looks; proofs/Carousels incomplete.')
q['next']={'model':'M03','action':'Review exact10.5s paired_v1 at native speed, including3.25–4s dissolve and subject approach. Both new stills approved; do not reopen those gates. M04–M05 follow queue.'}
q['active_reviews']=[{'model':'M03','scope':'exact whole film10.5s paired_v1','receipt':'reels/M03/paired_review_v1/visual_review.json','answer':None}]
write(W/'production_queue.json',q)

p=W/'asset_requirements.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=list(r.fieldnames);rows=list(r)
if 'evidence_path' not in fields:fields.append('evidence_path')
for r in rows:
    name=r['model']+'_'+r['look_id'].split('-')[-1]
    if name in approvals and r['surface']=='reel' and r['role']=='A_full_9x16':
        r.update(status='user_still_approved',evidence_path=rel(approvals[name][0]),reuse_candidate=approvals[name][2])
    if r['look_id']=='2026-W45-003-L02' and r['surface']=='reel' and r['role'] in ['styling_proof','medium_S03']:
        r.update(status='exact_video_frame_candidate_film_review_pending',evidence_path=rel(pair/'proof_frame_lineage.json'),reuse_candidate=rel(pair/'L02_styling_proof_source_f144.png'))
with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp)
series=next(s for s in reg['series'] if s['series_id']=='SERIES_W45_M03')
series.update(status='paired_v1_whole_film_pending_user_review',latest_asset_receipt=rel(pair/'visual_review.json'),still_approval_receipts=[rel(approvals[n][0]) for n in ['M03_L01','M03_L02']],execution_reconciliation=rel(HERE/'preflight_2026-11-04/EXECUTION_RECONCILIATION.md'))
usage='USE_W45_M03_PAIRED_V1_20261104'
if usage not in series['usage_ids']:series['usage_ids'].append(usage)
uses=reg['uses'] if 'uses' in reg else reg['usages']
entry={'usage_id':usage,'series_id':'SERIES_W45_M03','content_week':'2026-W45','source_weeks':['2026-W44','2026-W45'],'production_date':'2026-11-04','model_profile_id':'M03','look_ids':['2026-W45-003-L01','2026-W45-003-L02'],'film_path':rel(pair/edit['output_file']),'film_sha256':edit['output_sha256'],'receipt_path':rel(pair/'edit_receipt.json'),'status':'whole_film_candidate_pending_user_review','feedback_summary':'Exact stills approved; L01trial01 not selected due to approach/retreat, trial02 selected. L02 includes subject approach, not camera-only success.0.75s ghosting and continuous full-film QA gap disclosed.','publication_date':None,'post_url':None,'metrics':None}
old=next((x for x in uses if x['usage_id']==usage),None)
if old:old.update(entry)
else:uses.append(entry)
write(regp,reg)

sentence='W45現況：M01精確10.25秒片與M02 trial03已接受，無新增交接／發布。M03兩張精確首圖均已核准（L01「採用修正版」、L02「採用這張」），新10.5秒兩套審閱版已剪好，待原速整片觀看與使用者接受。L01原走近再退片未選，站位修正版入片；L02實際包含小步走近，不冒稱純相機推近成功。3.25–4秒疊化短暫疊影保留；連續人工全片動態QA未補寫。累計七次內建靜態／八支原片／兩支接受片，M04–M05與十套proof／Carousel仍缺。'
p=ROOT/'10_automation/CANONICAL_WORKFLOW.md';text=p.read_text(encoding='utf-8');lines=text.splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('現況與交接採短版有效摘要'));lines[idx]='現況與交接採短版有效摘要，歷史備份於 `10_automation/history/`。'+sentence+'精確結果見 `runs/2026-W45/reels/M03/paired_review_v1/REVIEW.md`；核對網址／媒體UUID／prompt，解碼抽樣與接受分記。';p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';text=p.read_text(encoding='utf-8');lines=text.splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('- W45：'));lines[idx]='- '+sentence+' [M03審閱紀錄](10_automation/runs/2026-W45/reels/M03/paired_review_v1/REVIEW.md)。';p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md';text=p.read_text(encoding='utf-8');lines=text.splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('先讀 [主工作流]'));lines[idx]='先讀 [主工作流](CANONICAL_WORKFLOW.md)、[CURRENT_STATUS](../CURRENT_STATUS.md)、當週發布結構，再讀本頁與精確收據。'+sentence+'最近已交付發布區仍是W44。';idx=next(i for i,l in enumerate(lines) if l.startswith('- 目前下一步：'));lines[idx]='- 目前下一步：展示[M03精確10.5秒兩套審閱版](runs/2026-W45/reels/M03/paired_review_v1/REVIEW.md)，待原速動態／整片回饋；兩張首圖已核准，不重開新圖問題。M01與M02已接受，不重生；M04–M05與proof／Carousel依隊列。';p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=W/'publishing_structure.md';lines=p.read_text(encoding='utf-8').splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('來源完整W45 v2企劃'));lines[idx]='來源完整W45 v2企劃已確認。'+sentence+' W44原交付保留。';idx=next(i for i,l in enumerate(lines) if l.startswith('2. [M02 trial03]'));lines[idx]='2. [M02 trial03](reels/M02/trial_03/REVIEW.md)與[M01 10.25秒片](reels/M01/paired_review_v1/REVIEW.md)均已接受，不重生；[M03 10.5秒兩套審閱版](reels/M03/paired_review_v1/REVIEW.md)已剪，待原速／整片接受。M03兩張首圖核准收據在approvals；L01約95%原圖及前進再退的trial01未選。';idx=next(i for i,l in enumerate(lines) if l.startswith('5. 原速逐鏡'));lines[idx]='5. 原速逐鏡／接點／整片、使用者接受、交接與發文分開。七次內建靜態／八支原片；M01與M02共兩支影片接受，M03待看。完整連續人工原速QA沒有補寫通過，十套proof／Carousel未完成，沒有實際IG發文。';p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=W/'planning/M03/SHOT_CARDS.md';lines=p.read_text(encoding='utf-8').splitlines();idx=next(i for i,l in enumerate(lines) if l.startswith('狀態：'));lines[idx]='狀態：11/3企劃及11/4兩張精確首圖均核准；現有[10.5秒兩套審閱版](../../reels/M03/paired_review_v1/REVIEW.md)，待原速／整片接受。L01 trial02取0–4秒；L02 trial01取0–7.25秒，一次0.75秒疊化。L02連續全身到中景實際含人物走近；原v2三鏡時程為企劃歷史，實際剪輯以下方執行收據為準。';lines += ['', '## 11/4實際執行', '', '同套L02全身與中景合為連續來源；[共享時鐘預演／差異](../../reels/M03/preflight_2026-11-04/EXECUTION_RECONCILIATION.md)。原v2快照不改。全片0–3.25秒褲裝清晰、3.25–4秒疊化、4–約6.75秒裙裝全身、約8.25秒起中景；兩次源片足夠讀衣，L01一次走位修正另計。後段是合理走近變體，未證明純相機推近。疊影與完整連續動態QA缺項在REVIEW中保留。'];p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=HERE/'preflight_2026-11-04/EXECUTION_RECONCILIATION.md';text=p.read_text(encoding='utf-8');text+='''
## 實際結果補記

原「各只一次」記錄初始請求界線。L01 trial01因約1–3秒前進再退未選，助理已說明並另做一次只改表演走位的trial02，改以固定雙腳、表情肩膀反應；抽樣站位較穩。沒有第三次同機制請求。L02只一次，生成實際含人物小步走近，未達成純相機推近與精確3.25秒時點；連續中景可讀，作本片合理變體候選，不列該機制成功。沒有新增中景圖或靠後製裁切放大。

實際剪輯L01 trial02[0,96)、L02 trial01[0,174)，18格疊化在全片[78,96)／3.25–4秒，252格10.5秒。近景約8.25秒後穩定，較原預演8.5秒略早。已抽樣完整影片／接點／靠近並技術解碼，連續人工原速審查與使用者整片接受仍待完成，未交接發布。
''';p.write_text(text,encoding='utf-8')
verification={'date':'2026-11-04','approved_snapshot_count':len(snapshot),'approved_snapshot_hashes_unchanged':True,'exact_still_approvals_verified':list(approvals),'source_url_media_prompt_checks':3,'paired_film_sha256':edit['output_sha256'],'source_mapping':read(pair/'source_mapping_check.json'),'counts':{'builtin_still_calls':7,'video_sources':8,'accepted_films':2},'continuous_full_film_visual_review':False,'publication_approval':None}
write(pair/'record_verification.json',verification)
print(json.dumps(verification,ensure_ascii=False))
