"""Record the returned async layout answer without inferring film acceptance."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;ROOT=P.parents[6];BR=P.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
receipt_path=P/'user_layout_preference_2026-11-05.json'
put(receipt_path,{'date':'2026-11-05','timezone':'Asia/Taipei','actor':'user','decision':'selected_layout_A','quote':'A：左右並排，選適合欄寬的精彩動作（建議）','question':'M03 完成版你較偏好哪種排版？我會先按原本的左右並排方向繼續選段；裙裝來源正在製作，兩種排版都能使用。','question_call_id':'call_80dbd2950a7e44b1b8e6d0bb12b8e27f','scope':'M03 layout and editorial selection direction: parallel windows, select expressive poses that fit each column.','limits':'Not acceptance of unseen or displayed full-film quality, new skirt performance, physics, dissolve comfort, delivery or publication.','selected_existing_candidate':rel(P/'M03_W45_parallel_selected_review_v1.mp4'),'new_generation':False})
ed=read(P/'edit_receipt.json')
for o in ed['outputs']:assert hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest()==o['sha256']
ed.update(selected_layout='A',layout_preference_receipt=rel(receipt_path));put(P/'edit_receipt.json',ed)
v=read(P/'visual_review.json');v['layout_preference']={'question_pending':False,'selected':'A parallel selected poses','receipt':rel(receipt_path),'B':'retained optional comparison, not active direction'};put(P/'visual_review.json',v)
for path,old,new in [
 (P/'REVIEW.md','排版偏好問題尚待回覆，先依原並排方向呈現A主候選，B僅供具體比較。','使用者已明確選A左右並排、選用適合欄寬的精彩動作；排版方向已定，精確收據為 `user_layout_preference_2026-11-05.json`。A成片品質與新裙裝仍待回饋，B留存備選。'),
 (BR/'STATUS.md','排版偏好及成片未核准','使用者已選A排版方向；成片品質及發布未核准')]:
    t=path.read_text(encoding='utf-8');assert old in t or new in t;path.write_text(t.replace(old,new),encoding='utf-8')
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/name;t=p.read_text(encoding='utf-8-sig');t=t.replace('待新裙裝／成片回饋及排版偏好，非發布核准。','使用者已選A左右並排方向，新裙裝／成片品質仍待回饋，非發布核准。').replace('排版偏好與新成片待回饋，來源接受不擴成發布；','A左右並排方向已獲選，新成片品質待回饋，來源／排版接受不擴成發布；').replace('目前下一步：回看M03兩種實片候選與新裙裝，保留原並排方向作主候選。','目前下一步：回看使用者已選排版方向的M03 A並排實片與新裙裝品質，B保留備選。');p.write_text(t,encoding='utf-8')
qp=ROOT/'10_automation/runs/2026-W45/production_queue.json';q=read(qp);q.update(status='M03_layout_A_selected_film_quality_pending',active_reviews=[ed['outputs'][0]['path']],retained_alternate_reviews=[ed['outputs'][1]['path']],layout_preference_receipt=rel(receipt_path));q['next']={'model':'M03','action':'A parallel selected poses is the chosen layout. Review exact A film and new skirt quality; B retained alternate, no automatic regeneration or inferred publication approval.'};put(qp,q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';r=read(rp);s=next(x for x in r['series'] if x['series_id']=='SERIES_W45_M03');s.update(status='layout_A_selected_film_quality_pending',layout_preference_receipt=rel(receipt_path),selected_layout='A parallel selected poses')
for u in r['uses']:
    if u['usage_id']=='USE_W45_M03_PARALLEL_SELECTED_V1_20261105':u.update(status='layout_selected_film_quality_pending_user_review',layout_preference_receipt=rel(receipt_path),feedback_summary='User selected A parallel layout and expressive poses fitting the columns. Exact film/new skirt quality and publication remain unapproved; trousers source performance accepted separately.')
    if u['usage_id']=='USE_W45_M03_FULL_FRAME_SEQUENCE_V1_20261105':u.update(status='retained_alternate_not_selected_layout',feedback_summary='User chose parallel layout A; B retained as optional comparison, not rejected source performance and not publication approved.')
put(rp,r)
print(json.dumps({'layout':'A','video_files_changed':False,'film_acceptance_inferred':False,'receipt':rel(receipt_path)}))
