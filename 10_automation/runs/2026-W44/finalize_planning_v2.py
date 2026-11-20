from pathlib import Path
import json, subprocess, sys
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;P=RUN/'planning'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
series=read(P/'series_proposals.json');rp=R/'04_prompts/material_pool/series_registry.json';registry=read(rp)
for s in series:
 sid='W44_PROPOSAL_'+s['id']
 record={'series_id':sid,'title':s['title'],'audience_question':s['question'],'relationship':s['answer'],'status':'proposed_awaiting_user_review','adopted_date':None,'source_material_ids':s['source_material_ids'],'usage_ids':[],'proposal_paths':['10_automation/runs/2026-W44/planning/series_proposals.json'],'superseded_proposal_paths':['10_automation/runs/2026-W44/history/before_W44_source_retrieval_2026-10-27/planning/series_proposals.json'],'content_week':'2026-W44','source_weeks':sorted({'2026-'+x.split('-')[0] for x in s['source_rows']}),'model_id':s['model'],'look_ids':s['look_ids'],'version':'v2_source_verified','note':'已取得W42–W44三週來源共60筆，完整搭配仍為編輯提案。未生成新AI圖或取得新企劃核准。'}
 registry['series']=[v for v in registry['series'] if v['series_id']!=sid]+[record]
registry['updated_date']='2026-10-27';write(rp,registry)
subprocess.run([sys.executable,str(R/'10_automation/build_material_pool.py'),'--as-of','2026-10-27','--window-weeks','3'],cwd=R,check=True,capture_output=True)
pool=R/'04_prompts/material_pool/CURRENT_POOL.md';t=pool.read_text(encoding='utf-8')
t=t.replace('目前天氣：本次未查；發布日期、網址與成效未知者留空。','目前天氣：索引重建本身未查；W44企劃已於2026-10-27核對氣象署逐日預報，收據見 `../../10_automation/runs/2026-W44/planning/research_receipt.json`。發布前重查，實際發布日期、網址與成效留空。')
t+='\n## W44來源補正（2026-10-27）\n\n使用者提供直接週報頁後，瀏覽器及允許的直接下載均成功；W42–W44各20列／5個來源方向，原始CSV與頁面內CSV逐列一致。先前缺週與舊企劃已被W44 v2取代，詳 `../../10_automation/runs/2026-W44/source_retrieval_correction.json`。網頁讀取工具或受限環境的DNS失敗不是未發布證據。\n'
pool.write_text(t,encoding='utf-8')
heading='## W44來源連線已補正，三週60筆、新版企劃待審 — 2026-10-27'
body='使用者提供W44直接網址後，瀏覽器成功讀到報告；經允許的直接網路存取已保存公開索引、W42／W43／W44原始CSV與HTML，三週各20列、5個來源方向，CSV與報告內資料逐列一致。素材池重建為近三週60筆候選、缺週0。前次工具讀取／受限環境DNS失敗不代表週報未發布，下方「缺三週、近期0」與W41舊材料提案為已取代的歷史狀態。\n\n[W44企劃v2](10_automation/runs/2026-W44/publishing_structure.md)／[五組新版線稿與01同步預演](10_automation/runs/2026-W44/planning/review.html)：M02紫色外搭工作日／週末、M01細肩帶洋裝白天疊穿、M04短程出差同雙低筒鞋配裙／褲、M03下班赴約紅包／紅腰帶、M05襯衫長褲加方巾。五位各兩套、五支Reel及每套full/proof與獨立Carousel A/B/C規格不變。W44新資料與W43棕丹寧／月牙包、W42膝長裙／平底鞋重新組合；沒有直接採納上游系列卡，功能主張不由AI圖推定。\n\n舊稿完整保存在W44 history/before_W44_source_retrieval_2026-10-27；來源下載與修正收據source_retrieval_correction.json。01幾何沿用為新服裝設計提案，不是原M03五套影片的曲線／閃爍修復。五份計畫結構檢查無錯誤、ready_for_generation=false；等待使用者確認v2企劃／分鏡／必要預演後才生成首張候選。未新增AI照片／動態、上傳／發文或排程。HTML滑桿尚未在瀏覽器執行驗證；線稿與同步投影關鍵圖已目視。此新企劃本機保存，尚未GitHub同步。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md']:
 path=R/name;t=path.read_text(encoding='utf-8-sig')
 if heading not in t:
  first,rest=t.split('\n',1);entry=body
  if name.startswith('10_automation/'):entry=entry.replace('(10_automation/runs/','(runs/')
  path.write_text(first+'\n\n'+heading+'\n\n'+entry+'\n'+rest,encoding='utf-8')
canonical=R/'10_automation/CANONICAL_WORKFLOW.md';t=canonical.read_text(encoding='utf-8-sig')
note='- W44 source correction and planning v2,2026-10-27: the user-provided W44 report loads in the browser. Public index plus W42/W43/W44 original CSV/report files are now saved and verified at20 rows each,60 current material candidates,no missing weeks. Earlier web-reader/restricted-shell DNS failure did not prove missing publication; use browser verification and an authorized direct retrieval before declaring a source absent. W44 publishing_structure and source-backed v2 boards/previs are proposed,not approved; no new AI stills or motion. See runs/2026-W44/source_retrieval_correction.json. Earlier audit statements about the10/16 pool snapshot/no W44 run are superseded by this scoped planning checkpoint.\n'
if note not in t:
 t=t.replace('## Standard Weekly Production Contract',note+'\n## Standard Weekly Production Contract');canonical.write_text(t,encoding='utf-8')
results=[]
for s in series:
 plan=P/f"series_{s['id']}/production_plan.json"
 res=subprocess.run([sys.executable,str(R/'11_skills/mira-reel-director/scripts/plan.py'),'validate',str(plan),'--project-root',str(R)],capture_output=True,text=True,encoding='utf-8',cwd=R)
 data=json.loads(res.stdout);write(plan.parent/'validation.json',data)
 assert not data['errors'],data
 assert data['ready_for_generation'] is False
 results.append({'series':s['id'],'errors':0,'status':data['status'],'ready_for_generation':False})
assert len(series)==5 and len({s['model'] for s in series})==5 and all(len(s['looks'])==2 for s in series)
write(P/'validation_summary.json',{'date':'2026-10-27','version':'v2_source_verified','plan_checks':results,'source_rows':{'2026-W42':20,'2026-W43':20,'2026-W44':20},'quota':'5 series; M01–M05 each once; 10 complete looks','visual_review':'Five revised line boards inspected, including dresses and layering, lower-leg proof, red bag/belt and scarf side-knot schematics. Shared-space contact sheet reviewed. Interactive HTML playback not browser-executed; local file protocol access was blocked.','ai_stills_generated':0,'approval':'pending; user correction about source connectivity is not plan approval'})
print(json.dumps(results))
