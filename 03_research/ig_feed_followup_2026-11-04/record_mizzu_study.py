"""Register the named current Reel; leave closed-feed positions unconfirmed."""
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];W=ROOT/'10_automation/runs/2026-W45';S=HERE/'mizzu_ri_DeO_-RVvCC-'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
overview=read(S/'native_capture.json');dense=read(S/'transition_capture.json')
assert overview['url']==dense['url']=='https://www.instagram.com/reels/DeO_-RVvCC-/'
samples=overview['samples']+dense['samples'];assert all(s['rate']==1 and not s['paused'] for s in samples)
entry={'date':'2026-11-04','timezone':'Asia/Taipei','account':'mizzu_ri','url':overview['url'],'user_reference_quote':'因為關閉了，所以我不確定。不過現在開的IG分頁的第二則:mizzu_ri也是蠻有參考價值','evidence_status':'observed_original_page_native1x_dynamic_sampling','platform_label_observed':'AI 內容','reported_duration_seconds':overview['samples'][0]['d'],'overview_samples':len(overview['samples']),'transition_samples':len(dense['samples']),'review_path':rel(S/'REVIEW.md'),'candidate_parent_recipe':'foreground_reveal','candidate_variant':'overhead_rotating_foreground_occlusion_multi_look_display','method_status':'observed_reference_not_Mira_tested_or_accepted','creator_pipeline':'unknown','viewing_limits':'UI time-stamped screenshot sampling, no raw decode, no audio analysis or uninterrupted human full-film review claim.','new_Mira_still_calls':0,'new_Mira_video_jobs':0,'new_Mira_edits':0,'new_browser_tabs':0,'mark_deliverable_or_handoff_used':False,'new_publication_approval':None}
write(S/'reference_receipt.json',entry)
p=HERE/'candidate_index.json';c=read(p);c.pop('new_videos_watched_this_followup',None);c.update(status='closed_positions_unconfirmed_current_named_reference_observed',latest_user_reply=entry['user_reference_quote'],original_positions_confirmed=False,current_named_reference=entry['url'],current_named_reference_receipt=rel(S/'reference_receipt.json'),new_video_sources_observed_this_followup=1,observation_scope='User-named mizzu_ri Reel, native1x UI sampling; not a claim of uninterrupted human viewing.',next='Do not reopen1/3/5 identification unless user adds information. Use the now-observed explicit mizzu_ri reference for editorial planning.');write(p,c)
catalog=ROOT/'09_sops/mira_reel_method_catalog.md';t=catalog.read_text(encoding='utf-8');note='2026-11-04使用者另指定[mizzu_ri俯拍扇葉換裝](../03_research/ig_feed_followup_2026-11-04/mizzu_ri_DeO_-RVvCC-/REVIEW.md)：原頁約14.77秒、四段造型，頁面標AI內容；145張1倍速UI動態抽樣支持前景扇葉遮擋期間切換、人物平靜擺姿與造型選擇看點。列foreground_reveal下的旋轉前景／俯拍候選，未成Mira試作或接受、不增加成熟方法數；原作者製作流程未知。遮擋主要在上半身，不能直接解決M03褲裙下身接點；躺姿俯拍需另分鏡／缺圖及新圖核准。'
if note not in t:catalog.write_text(t.replace('# Mira Reel 製作方法庫\n','# Mira Reel 製作方法庫\n\n'+note+'\n',1),encoding='utf-8')
q=read(W/'production_queue.json');paths=q.get('reference_studies',[])
for pth in ['03_research/ig_feed_study_2026-11-04/REVIEW.md',rel(S/'REVIEW.md')]:
    if pth not in paths:paths.append(pth)
q.update(status='M03_editorial_replan_with_named_mizzu_reference',latest_reference_study=rel(S/'REVIEW.md'),reference_studies=paths,next={'model':'M03','action':'Choose viewer mechanism and storyboard before new generation, using observed original-feed3 references plus explicit mizzu overhead/foreground-wipe example. Account for lower-body change in approved trouser/skirt looks; reference is not plan approval.','reference_study':rel(S/'REVIEW.md')},active_reviews=[]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);series=next(x for x in reg['series'] if x['series_id']=='SERIES_W45_M03');series.update(status='editorial_replan_from_observed_references_no_current_accepted_film',latest_reference_study=rel(S/'REVIEW.md'),reference_study_paths=paths);write(regp,reg)
p=ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md';lines=p.read_text(encoding='utf-8').splitlines()
for i,l in enumerate(lines):
    if l.startswith('- 目前下一步：'):lines[i]='- 目前下一步：由[原首頁三筆觀察](../03_research/ig_feed_study_2026-11-04/REVIEW.md)及[使用者新指定mizzu俯拍扇葉換裝](../03_research/ig_feed_followup_2026-11-04/mizzu_ri_DeO_-RVvCC-/REVIEW.md)，選清楚的觀看機制並回M03分鏡。新來源已觀察，尚非Mira方案核准／生成；躺姿俯拍與下身遮擋不可直接套既有站姿褲裙。舊新頁1/3/5仍未確認，使用者已改指當前mizzu，不重問；不新開／額外標記分頁。既有退件與接受範圍保持。'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
for p in [ROOT/'CURRENT_STATUS.md',W/'publishing_structure.md']:
    lines=p.read_text(encoding='utf-8').splitlines();line='- 新參考：11/4已觀察使用者指定mizzu_ri俯拍扇葉四造型Reel；[具體觀察](../03_research/ig_feed_followup_2026-11-04/mizzu_ri_DeO_-RVvCC-/REVIEW.md)，僅作未經Mira實測的候選。' if p.name=='CURRENT_STATUS.md' else '- 新參考：[mizzu_ri俯拍扇葉四造型](../../../03_research/ig_feed_followup_2026-11-04/mizzu_ri_DeO_-RVvCC-/REVIEW.md)已觀察，未新增生成或方案核准。'
    if p.name=='CURRENT_STATUS.md':line=line.replace('](../03_research/','](03_research/')
    if not any(l.startswith('- 新參考：') for l in lines):lines.insert(10,line)
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for a in snap:assert hashlib.sha256((ROOT/a['snapshot_path']).read_bytes()).hexdigest()==a['sha256']
write(S/'verification.json',{'sample_count':len(samples),'all_samples_reported_1x_playing':True,'source_URL_matches_user_named_account':True,'closed_feed_positions_not_fabricated':True,'new_browser_tabs':0,'extra_tab_marks':0,'new_Mira_media':0,'approved_snapshot_count':len(snap),'approved_snapshot_hashes_unchanged':True})
print(json.dumps({'source':entry['url'],'samples':len(samples),'new_Mira_media':0,'new_tabs':0,'snapshots_unchanged':len(snap)},ensure_ascii=False))
