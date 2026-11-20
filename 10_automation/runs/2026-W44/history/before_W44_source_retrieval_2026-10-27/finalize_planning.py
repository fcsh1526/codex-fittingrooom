"""Record the W44 planning checkpoint without approving or generating media."""
from pathlib import Path
import json, sys, subprocess, hashlib, math
R=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parent/'planning'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
series=read(P/'series_proposals.json')
registry_path=R/'04_prompts/material_pool/series_registry.json'
registry=read(registry_path)
for s in series:
 sid='W44_PROPOSAL_'+s['id']
 record={'series_id':sid,'title':s['title'],'audience_question':s['question'],'relationship':s['answer'],'status':'proposed_awaiting_user_review','adopted_date':None,'source_material_ids':s['source_material_ids'],'usage_ids':[],'proposal_paths':['10_automation/runs/2026-W44/planning/series_proposals.json'],'content_week':'2026-W44','model_id':s['model'],'look_ids':s['look_ids'],'note':'W41 older material re-reviewed with current supplementary seasonal research; no W44 raw Perplexity report available. No new media or adoption approval.'}
 registry['series']=[v for v in registry['series'] if v['series_id']!=sid]+[record]
weather={'check_id':'WX_W44_20261027','checked_date':'2026-10-27','timezone':'Asia/Taipei','regions':['台北','台中','高雄'],'source':'https://www.cwa.gov.tw/Data/fcst_pdf/W53.pdf','issued_at':'2026-10-27T11:00:00+08:00','target_dates':['2026-10-27','2026-11-01'],'receipt_path':'10_automation/runs/2026-W44/planning/research_receipt.json','status':'checked_for_planning_recheck_before_publication','actual_publication_dates':None}
registry['weather_checks']=[v for v in registry['weather_checks'] if v.get('check_id')!=weather['check_id']]+[weather]
registry['updated_date']='2026-10-27';write(registry_path,registry)
subprocess.run([sys.executable,str(R/'10_automation/build_material_pool.py'),'--as-of','2026-10-27','--window-weeks','3'],cwd=R,check=True,capture_output=True)
# Keep builder's honest scope while pointing to the separate current weather research.
pool=R/'04_prompts/material_pool/CURRENT_POOL.md'
text=pool.read_text(encoding='utf-8')
text=text.replace('目前天氣：本次未查；發布日期、網址與成效未知者留空。','目前天氣：索引重建本身未查天氣；W44企劃已另於2026-10-27核對氣象署逐日縣市預報，見 `../../10_automation/runs/2026-W44/planning/research_receipt.json` 及registry的WX_W44_20261027。發布前須重查；實際發布日期、網址與成效留空。')
pool.write_text(text,encoding='utf-8')
for file,heading,entry in [
 ('CURRENT_STATUS.md','## W44新週企劃與同步預演待審 — 2026-10-27',
  '使用者已啟動新一週製作，要求確認企劃／分鏡及必要預演後才生成起始圖。本週原先缺publishing_structure，現已建立[W44待審發布結構](10_automation/runs/2026-W44/publishing_structure.md)及[五系列、十套、線稿與同步預演](10_automation/runs/2026-W44/planning/review.html)。維持五位各兩套；01 M02薄層次採兩套連續路線，02格紋並排，03短程出差，04下班赴約，05秋色點綴。全部為提案，尚無企劃／新圖核准。\n\n素材池按10/27、近三週重建：W42–W44缺原始CSV、近期來源候選0，保留W41舊20筆重審。Perplexity公開索引Web不可讀且本機DNS無法解析；補充秋季品牌／媒體內容不冒稱完整W44週報。已查氣象署10/27 11:00逐日縣市預報，來源及限制見W44 planning/research_receipt.json。五位face/full檔案存在；未重新核准身份。01預演由同份shared_space產生俯視／相機投影，屬未測量的示意場地與骨架，不是實際Grok軌道／步態或閃爍舒適度通過。\n\n下一步：請使用者審五系列／兩套／線稿與01雙路徑，再做所選系列首張native9:16全身候選。五份結構檢查無錯誤但ready_for_generation=false；未生成AI照片或新動態、未外部交付或發文。W43核准影片、原M03五套快步／曲線／閃爍改善範圍保留。此檢查點本機保存，尚未納入GitHub同步。'),
 ('10_automation/MIRA_EDITORIAL_HANDOFF.md','## W44新週企劃已建立，待審 — 2026-10-27',
  '使用者本輪已啟動新週；原先缺檔已補為[W44待審規劃](runs/2026-W44/publishing_structure.md)，[線稿與同步預演入口](runs/2026-W44/planning/review.html)。五位各兩套、五支Reel與每套雙surface規格保留，尚未生成新圖。W42–W44原始週報缺少／Perplexity索引無法取得，素材池已刷新至10/27；W41舊材料＋補充季節訊號／逐日天氣形成五個待審編輯提案，不能當完整本週新趨勢。\n\n01 M02薄層次路線有共同場地與相機投影預演；屬本週新設計，不是原M03五套第二版修復。其餘選題及缺圖見W44；五位雙參照存在，所有新起始圖須待本輪企劃確認並逐張審。下一步只審具體提案，再開始第一張候選。以下W44缺檔／10/16快照描述為本輪之前狀態，以此檢查點取代。尚未同步本次企劃到GitHub。')]:
 path=R/file;t=path.read_text(encoding='utf-8-sig')
 if heading not in t:
  first,rest=t.split('\n',1);path.write_text(first+'\n\n'+heading+'\n\n'+entry+'\n'+rest,encoding='utf-8')
results=[]
for s in series:
 plan=P/f"series_{s['id']}/production_plan.json"
 result=subprocess.run([sys.executable,str(R/'11_skills/mira-reel-director/scripts/plan.py'),'validate',str(plan),'--project-root',str(R)],capture_output=True,text=True,encoding='utf-8',cwd=R)
 data=json.loads(result.stdout);write(plan.parent/'validation.json',data)
 assert not data['errors'],data
 assert data['ready_for_generation'] is False
 results.append({'series':s['id'],'errors':len(data['errors']),'status':data['status'],'ready_for_generation':data['ready_for_generation']})
# All clock samples must keep the schematic full figure inside the frame.
space=read(P/'shared_space.json');samples=[q for r in space['routes'] for q in r['projected_samples']]
assert all(0<q['person_height_fraction']<1 for q in samples)
assert len(series)==5 and len({s['model'] for s in series})==5
assert all(len(s['looks'])==2 for s in series)
write(P/'validation_summary.json',{'date':'2026-10-27','plan_checks':results,'quota_check':'5 series, M01–M05 each once, 10 complete looks','visual_review':'All five line boards and synchronized projection contact sheet visually inspected; clothing color and seated-pose diagrams corrected. HTML interactive playback has not been browser-executed by the assistant.','shared_space':'Common source hash and both declared view dependencies checked by plan validator; human viewed first/middle/end projection contact sheet. No actual video/Grok motion or physical foot-contact validation.','ai_stills_generated':0,'approval':'pending; no user approval inferred'})
print(json.dumps(results))
