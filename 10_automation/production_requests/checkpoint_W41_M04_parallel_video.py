"""Record actual inspection without inferring full playback or film approval."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
week=ROOT/'10_automation/runs/2026-W41';work=week/'reels/M04'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cfg=read(work/'parallel_composition_v1_config.json')
for x in cfg['sources']:
    side=x['role'];qa=work/f'{side}_attempt_01/QA/inspection.json';d=read(qa)
    assert d['source_sha256']==x['sha256']
    d.update(assistant_static_dynamic_review=x['observed_action'],sampled_review_scope=cfg['sampled_review_scope'],continuous_playback_review=False);write(qa,d)
    qa=work/f'{side}_attempt_01/contact_QA/strap_contact_inspection.json';d=read(qa)
    d['hand_strap_visual_result']=x['observed_action'];write(qa,d)
    qa=work/f'{side}_attempt_01/browser_receipt.json';d=read(qa)
    d.update(source_sha256=x['sha256'],measured_native={'size':[720,1280],'fps':24,'frames':145,'audio_streams':0});write(qa,d)
p=work/'review_v1/composition_receipt.json';d=read(p)
assert hashlib.sha256((ROOT/d['output_path']).read_bytes()).hexdigest()==d['sha256']
d.update(combined_sampled_visual_review='25 whole-frame and five windows for each face inspected; all144 combined-frame thumbnails checked for panel bounds. Hair, hands, both shoes, bag and skirt remain contained. Close opening head/waist/shoe positions; independent head tilts and gesture timing preserved. Stable architectural anchors in inspected frames.',all_frame_panel_bound_review='completed via six consecutive thumbnail sheets; not full-detail all-frame identity review',continuous_playback_review=False,status='sampled_QA_complete_user_playback_and_film_approval_pending')
write(p,d)
p=work/'review_v1/bounds_QA/inspection.json';v=read(p);v['all_frame_bound_visual_review']='completed; no subject clipping apparent in all144 thumbnails';write(p,v)
p=work/'review_v1/technical_QA/inspection.json';v=read(p);v['assistant_static_dynamic_review']=d['combined_sampled_visual_review'];write(p,v)
p=week/'reels/production_manifest.json';m=read(p);r=next(x for x in m['reels'] if x['model_profile_id']=='M04')
r['status']='film_candidate_sampled_QA_complete_user_picture_approval_pending'
r['identity']['saved_reference_name']='Mira M04 v3'
r['qa'].update(status='source_strap_contact_and_combined_panel_inspection_complete',continuous_watch_done=False,user_approval=None,receipt='10_automation/runs/2026-W41/reels/M04/review_v1/composition_receipt.json')
r['music']['clean_master']=d['output_path'];r['candidate_file']=d['output_path']
r['video_sources']=[{'role':x['role'],'look_id':x['look_id'],'path':x['path'],'sha256':x['sha256'],'browser_receipt':f'10_automation/runs/2026-W41/reels/M04/{x["role"]}_attempt_01/browser_receipt.json'} for x in cfg['sources']]
r['parallel_composition']={'duration_seconds':6,'native_speed':True,'forced_synchronization':False,'transition':'none; simultaneous panels','config':'10_automation/runs/2026-W41/reels/M04/parallel_composition_v1_config.json'}
write(p,m)
p=ROOT/'10_automation/production_requests/2026-10-08_next_five_reels.json';v=read(p);r=next(x for x in v['slots'] if x['model']=='M04');r.update(status='film_candidate_sampled_QA_complete_user_picture_approval_pending',candidate_file=d['output_path'],film_user_approval=None);write(p,v)
p=week/'reels/batch_storyboard.json';v=read(p)
for r in v['films']:
    if r.get('model_profile_id',r.get('model'))=='M04':
        r['executed_film_candidate']={'file':d['output_path'],'seconds':6,'observed_actions':[x['observed_action'] for x in cfg['sources']],'continuous_playback_review':False,'user_video_approval':None}
write(p,v)
p=week/'publishing_structure.md';s=p.read_text(encoding='utf-8');s=s.replace('接續分別送Grok；第一套實際起姿左手在褲袋，動畫需自然抽出再碰肩帶。','已建立Mira M04 v3參照並分別生成；六秒左右版已合成，原速無字無音，已檢視各側全部肩帶接觸格、成片144格邊界與兩側臉部樣格。實際第一套雙手、第二套右手跨身整理肩帶，與原規劃差異已記錄；成片完整播放與使用者畫面核准待完成。');p.write_text(s,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8');entry='''## W41 fifth Reel: M04 six-second parallel candidate ready — 2026-10-08

Approved exactv2 first frames animated separately with saved `Mira M04 v3` face/full reference. Each actual source720×1280/24fps/145frames/audio0. Source25 whole-frame/5face windows and all145 shoulder/hand/bag windows inspected. Actual A uses both hands, B uses right hand across torso; visible contact and small bag response, recorded as variations from planned single left hand.

Candidate `10_automation/runs/2026-W41/reels/M04/review_v1/2026-W41_M04_two_looks_parallel_v1.mp4` is6s/144frames/720×1280/24fps/audio0; both source intervals[0,144). Fixed background-only crops[168,115,551,1175] proportionally placed in equal352×974 panels at[4,152] and[364,152]. No internal shot change, speed edit or forced synchronization.25 combined samples, each face5 and all144 bound thumbnails inspected; complete person, hands, bag and skirt stay contained. Normal-speed full playback and user film approval remain pending.

Five film candidates now exist. M01/M02 picture-approved; M03/M04/M05 film approvals pending. Proof/Carousel gaps remain open; no W41 Drive delivery or IG posting claimed. Previous batch preserved. Second download recovered through the actual Grok Download button after media helper navigated old tab toMP4 and stalled; no regeneration. All later work local, outside previous bounded public Git checkpoint.

''';p.write_text(s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+entry,1),encoding='utf-8')
print(json.dumps({'candidate':d['output_path'],'sha256':d['sha256'],'seconds':6,'film_approval':None}))
