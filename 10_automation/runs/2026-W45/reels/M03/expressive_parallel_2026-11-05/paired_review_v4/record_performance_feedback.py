"""Keep the exact rejection, distinct from earlier layout/source acceptance."""
import hashlib,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent;BR=P.parent;ROOT=BR.parents[5];W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
e=read(P/'edit_receipt.json');assert hashlib.sha256((ROOT/e['output']).read_bytes()).hexdigest()==e['output_sha256']
fp=P/'user_performance_feedback_2026-11-05.json'
put(fp,{'date':'2026-11-05','timezone':'Asia/Taipei','actor':'user','quote':'我不喜歡搖擺跳舞','decision':'not_accepted_performance_direction','target_path':e['output'],'target_sha256':e['output_sha256'],'context':'Direct feedback to displayed4s M03 A parallel v4.','explicit_preference':'Does not like swaying/dance performance.','assistant_interpretation':'Stop using repeated hip/shoulder sways and dance-like chains of poses to satisfy the request for larger movement. Keep distinct motivated natural actions and meaningful clothing views.','limits':'Not a rejection of parallel layout A or all larger movements, turns or walking. Preserve prior exact source-performance acceptance as historical evidence; it does not authorize continued use of the disliked performance in a new film. No claim user identified an exact gesture/timecode.','new_generation':False})
for file in ['edit_receipt.json','visual_review.json']:
    v=read(P/file);v.update(status='user_not_accepted_swaying_dance_performance',user_film_acceptance=False,feedback_receipt=rel(fp));put(P/file,v)
note='最新使用者回饋：「我不喜歡搖擺跳舞」。此精確4秒v4不採用，撤出待審；停止沿連續搖肩、擺臀／節奏換姿微調。A並排排版偏好仍有效，改由自然情境與明確單次動作規劃，不把舊來源接受擴為此表演方向核准。\n\n'
p=P/'REVIEW.md';t=p.read_text(encoding='utf-8')
if note not in t:t=t.replace('\n\n','\n\n'+note,1);p.write_text(t,encoding='utf-8')
plan=BR/'NATURAL_PERFORMANCE_REPLAN_2026-11-05.md'
plan.write_text('''# M03 表演改案｜自然拍攝，沿用A並排

狀態：依最新回饋整理的執行草案，未生成、未聲稱新片已核准。精確回饋見 `paired_review_v4/user_performance_feedback_2026-11-05.json`。

觀眾仍看同件海軍藍柔肩西外，深褲／皮鞋與淺色A字裙／球鞋的輪廓和正式感差異。使用者不喜歡搖擺跳舞；明顯動作幅度仍可保留，不回退為只有微晃的站姿片。

下一版情境為出發前請朋友拍一張穿搭照。人物自然等候鏡頭準備，聽見鏡頭這邊的朋友招呼後抬眼、短暫微笑，順勢側身一次讓西外側線與下身輪廓可讀，再回到舒服站姿。注意對象是拍攝者。這是助理提出的動機與動作，不冒稱使用者已指定這段情節。

先按每側單一約6秒連續來源規劃；不用4秒片的內部多段拼接，不預設兩側動作逐秒同步。固定鏡頭、完整頭鞋、相同人物尺度，手臂自然近身；先做實際欄寬預檢。禁止把連續左右擺臀、搖肩、反覆扭腰或舞蹈式手勢串接當成增加活力的手段。單次自然轉身、落腳和表情反應仍可選。

素材先評估既有兩張已核准M03首圖；沒有新增道具、人物或場景需求，不先補圖。這兩支10秒來源的連續換姿已受新回饋限制，不繼續靠抽取搖擺段來重剪。若生成新來源，另列精確輸入、次數／額度與原速品質檢查；本回合沒有提交生成、費用或新圖片。

成功判準：觀眾能讀出等待拍照、回應拍攝者與一次側身展示，肢體隨事件改變而非持續節奏搖擺；兩套衣服在實際並排中可讀，手腳與頭身自然，表情不維持誇張固定笑容。逐鏡、接點、整片與使用者接受分開記錄。
''',encoding='utf-8')
qp=W/'production_queue.json';q=read(qp);q.update(status='M03_performance_rejected_natural_action_replan',active_reviews=[],latest_performance_feedback=rel(fp),latest_editorial_proposal=rel(plan));q['next']={'model':'M03','action':'Use natural motivated single-action performance and selected parallel layout; draft replan recorded, no repeated swaying/dance recut or automatic generation.'};put(qp,q)
rp=ROOT/'04_prompts/material_pool/series_registry.json';r=read(rp);s=next(x for x in r['series'] if x['series_id']=='SERIES_W45_M03');s.update(status='parallel_layout_retained_dance_performance_not_accepted',latest_performance_feedback=rel(fp),latest_editorial_proposal=rel(plan))
u=next(x for x in r['uses'] if x['usage_id']=='USE_W45_M03_PARALLEL_SELECTED_V4_20261105');u.update(status='user_not_accepted_swaying_dance_performance',feedback_receipt=rel(fp),feedback_summary='User: 我不喜歡搖擺跳舞. Exact4s v4 not accepted. Preserve A layout preference; replan natural motivated actions, do not continue dance-like pose chains. Earlier trousers source acceptance remains historical, not current-film approval.')
put(rp,r)
current='W45現況：M01精確10.25秒與M02 trial03已接受，尚無新交接／發布。M03使用者對4秒A v4明確回饋「我不喜歡搖擺跳舞」，此版不採用並撤出待審；停止連續搖擺／舞蹈式換姿的微調。A左右並排偏好及兩張首圖核准保留；褲裝trial02舊來源接受是歷史範圍，不擴成現行表演／成片核准。已整理自然情境、回應拍攝者與單次明顯轉向的草案，未送新生成。舊原片、各剪輯與B比較均保留，不自動重開待審。累計七次靜態／十二支原片／兩支接受成片；M04–M05與proof／Carousel仍缺。詳M03 expressive_parallel_2026-11-05/NATURAL_PERFORMANCE_REPLAN_2026-11-05.md。'
for name in ['CURRENT_STATUS.md','10_automation/CANONICAL_WORKFLOW.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W45/publishing_structure.md']:
    p=ROOT/name;lines=p.read_text(encoding='utf-8-sig').splitlines()
    for i,line in enumerate(lines):
        if 'W45現況：' in line:lines[i]=line.split('W45現況：')[0]+current
        elif line.startswith('- 11/5完整換姿：'):lines[i]='- 11/5完整換姿：使用者「我不喜歡搖擺跳舞」，4秒v4不採用，停止同類連續換姿微調。A排版保留；[自然表演改案草稿](runs/2026-W45/reels/M03/expressive_parallel_2026-11-05/NATURAL_PERFORMANCE_REPLAN_2026-11-05.md)未生成。'
        elif line.startswith('- 目前下一步：'):lines[i]='- 目前下一步：依M03最新不喜歡搖擺跳舞的回饋，改以自然情境與單次明顯行動設計A並排，不重貼被否決v4；原片與接受歷史保留。IG沿用現有頁，不新開分頁。'
        elif line.startswith('2. M01／M02接受保留。'):lines[i]='2. M01／M02接受保留。M03 A排版保留、4秒v4因搖擺跳舞不採用；先依[自然表演草案](reels/M03/expressive_parallel_2026-11-05/NATURAL_PERFORMANCE_REPLAN_2026-11-05.md)重新規劃，不重開v4待審或列可發布。'
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
# Persist the user's new general performance preference ahead of older hip-sway examples.
rule='2026-11-05表演偏好：使用者明確表示「我不喜歡搖擺跳舞」。後續以有情境目的的自然動作設計，停止用連續擺臀、搖肩或舞蹈式換姿增加活力；動作幅度可以明顯，單次轉身、短步、自然笑容與入出畫依內容選用。此最新偏好優先於10/29列舉擺臀等舊候選，不否定A並排或所有大幅動作。精確回饋：`10_automation/runs/2026-W45/reels/M03/expressive_parallel_2026-11-05/paired_review_v4/user_performance_feedback_2026-11-05.json`。'
for name in ['10_automation/CANONICAL_WORKFLOW.md','09_sops/mira_reel_production_sop.md']:
    p=ROOT/name;t=p.read_text(encoding='utf-8-sig')
    if rule not in t:t=t.replace('\n\n','\n\n'+rule+'\n\n',1);p.write_text(t,encoding='utf-8')
p=BR/'STATUS.md';p.write_text('''# M03 換姿研究｜有效狀態

2026-11-05。使用者最新回饋「我不喜歡搖擺跳舞」。4秒A v4不採用，已撤出待審；停止用搖擺／連續換姿繼續剪短微調。

A並排排版與兩張首圖核准保留。褲裝trial02來源曾接受的收據保留為歷史，不據此繼續使用使用者不喜歡的表演方向。舊影片均保留，不刪檔、不重開待審、不列發布。

[自然表演改案](NATURAL_PERFORMANCE_REPLAN_2026-11-05.md)為助理草案，未生成。動作仍可明顯，但需有情境、注意對象與連貫反應。本回合零新增圖片／影片生成；M01／M02接受不受影響。
''',encoding='utf-8')
print(json.dumps({'feedback_recorded':True,'v4_removed_from_active_reviews':True,'parallel_layout_retained':True,'new_generation':False}))
