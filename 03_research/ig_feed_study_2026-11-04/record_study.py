"""Register observed references without promoting them to tested Mira methods."""
import json,hashlib,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];W=ROOT/'10_automation/runs/2026-W45'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rel(p):return p.relative_to(ROOT).as_posix()
refs=[]
for folder,mechanism in [('01_momoko','garment_tease_to_outfit_reveal_front_back_accessory_and_approach'),('02_leeharin','pose_and_attitude_continuity_across_two_looks'),('03_slowand','daily_drink_turn_and_outer_layer_sequence')]:
    m=read(HERE/folder/'native_capture.json');samples=m['samples']
    assert samples and all(s['rate']==1 and not s['paused'] for s in samples)
    refs.append({'reference_id':folder,'account':m['account'],'url':m['url'],'observed_date':'2026-11-04','source_entry':'Existing Instagram homepage tab4, initial feed order; not latest-feed chronology claim.','evidence_status':'observed_original_page_native1x_screenshot_sampling','reported_duration_seconds':samples[0]['d'],'sample_count':len(samples),'sample_min_t':min(s['t'] for s in samples),'sample_max_t':max(s['t'] for s in samples),'candidate_mechanism':mechanism,'evidence_path':rel(HERE/folder/'native_capture.json'),'review_path':rel(HERE/'REVIEW.md'),'limits':m.get('limits','UI sampling across a loop, not uninterrupted human visual/audio review or frame-accurate cuts.'),'audio_analysis':False,'AI_or_human_classification':'not_established','Mira_proposal_approved':False,'Mira_tested':False,'Mira_accepted':False,'publication_outcome':None})
write(HERE/'references.json',{'date':'2026-11-04','timezone':'Asia/Taipei','task_scope':'Observe first few posts on already-open IG homepage;3bounded sources','reference_count':3,'references':refs,'new_Mira_still_calls':0,'new_Mira_video_jobs':0,'new_Mira_edits':0,'engagement_actions':[]})
catalog=ROOT/'09_sops/mira_reel_method_catalog.md';text=catalog.read_text(encoding='utf-8')
note='2026-11-04新增實際原頁觀察：[原開IG首頁前三篇](../03_research/ig_feed_study_2026-11-04/REVIEW.md)。momoko_takasaki的造型揭示／正背配件／靠近、leeharin.xoxo的兩套姿態與態度銜接、slow.and首段的持杯日常與外搭。三筆均為原頁1倍速動態抽樣，第三篇視窗局部與未看完整輪播限制保留；不判真人／AI、不推成效。可見的展示態度也能成立觀看目的，不強制編故事。列為已觀察候選，尚未形成新Mira方案核准／試作／方法接受，不增加既有五方法計數，約0.75秒接點與一片一模特兒規則保留。'
if note not in text:catalog.write_text(text.replace('# Mira Reel 製作方法庫\n','# Mira Reel 製作方法庫\n\n'+note+'\n',1),encoding='utf-8')
q=read(W/'production_queue.json');q.update(status='M03_editorial_replan_from_observed_feed_references',latest_reference_study=rel(HERE/'REVIEW.md'),next={'model':'M03','action':'Use the3actually observed feed references to choose a legible viewer experience/attitude or daily action, reconnect to approved navy blazer trouser/skirt content, then storyboard before further generation. Research is not plan/still/video approval.','reference_study':rel(HERE/'REVIEW.md')},active_reviews=[]);write(W/'production_queue.json',q)
regp=ROOT/'04_prompts/material_pool/series_registry.json';reg=read(regp);s=next(s for s in reg['series'] if s['series_id']=='SERIES_W45_M03');s.update(status='editorial_replan_with_observed_feed_references_no_current_accepted_film',latest_reference_study=rel(HERE/'REVIEW.md'));write(regp,reg)
sentence='11/4後續已實際打開原開IG首頁前三篇（momoko_takasaki／leeharin.xoxo／slow.and首段），保存原頁1倍速抽樣與具體觀察；已區分展示態度、姿態換裝及日常活動三種可借機制，沒有新生成或方法核准。'
for p in [ROOT/'10_automation/CANONICAL_WORKFLOW.md',ROOT/'CURRENT_STATUS.md',W/'publishing_structure.md']:
    lines=p.read_text(encoding='utf-8').splitlines()
    for i,l in enumerate(lines):
        matches=(p.name=='CANONICAL_WORKFLOW.md' and l.startswith('現況與交接採短版有效摘要')) or (p.name=='CURRENT_STATUS.md' and l.startswith('- W45現況：')) or (p.name=='publishing_structure.md' and l.startswith('來源完整W45 v2企劃'))
        if matches and sentence not in l:lines[i]=l+' '+sentence
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=ROOT/'10_automation/MIRA_EDITORIAL_HANDOFF.md';lines=p.read_text(encoding='utf-8').splitlines()
for i,l in enumerate(lines):
    if l.startswith('- 目前下一步：'):lines[i]='- 目前下一步：由[這輪實際IG三筆觀察](../03_research/ig_feed_study_2026-11-04/REVIEW.md)選清楚的展示態度或日常活動，接回M03同件西外／褲裙看點，先重整連接分鏡。這次來源已看且限制已記，尚非新方案核准；沒有自動生成或待看片。M03既有退件、首圖及M01／M02接受範圍保持。'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
snap=read(W/'approvals/user_planning_approval_2026-11-03.json')['artifacts']
for a in snap:assert hashlib.sha256((ROOT/a['snapshot_path']).read_bytes()).hexdigest()==a['sha256']
write(HERE/'verification.json',{'reference_count':3,'original_page_screenshot_samples':sum(r['sample_count'] for r in refs),'all_samples_reported_native1x_playing':True,'approved_snapshot_count':len(snap),'approved_snapshot_hashes_unchanged':True,'new_Mira_media':0,'user_publishing_or_method_approval':None})
print(json.dumps({'references':[(r['account'],r['sample_count'],r['reported_duration_seconds']) for r in refs],'total_samples':sum(r['sample_count'] for r in refs),'new_Mira_media':0,'snapshot_count':len(snap)},ensure_ascii=False))
