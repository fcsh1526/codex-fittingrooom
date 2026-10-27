"""Record completed sampling separately from playback and user film approval."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
week=ROOT/'10_automation/runs/2026-W41'
work=week/'reels/M03'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cfg=read(work/'composition_v1_config.json')
for side in ['A','B']:
    qa=work/f'{side}_attempt_01/QA/inspection.json'
    d=read(qa); d['assistant_static_dynamic_review']=cfg['source_sampled_visual_review'][side]
    d['sampled_review_scope']=cfg['source_sampled_visual_review']['scope']
    d['continuous_playback_review']=False;write(qa,d)
    p=work/f'{side}_attempt_01/contact_QA/cuff_contact_inspection.json'
    d=read(p);d['hand_cloth_visual_result']=cfg['source_sampled_visual_review'][side];write(p,d)
    p=work/f'{side}_attempt_01/browser_receipt.json';d=read(p)
    d['source_sha256']=read(qa)['source_sha256'];d['measured_native']={'size':[720,1280],'fps':24,'frames':145,'audio_streams':0}
    write(p,d)
p=work/'review_v1/composition_receipt.json';d=read(p)
d['combined_visual_QA']='25 whole-frame/5 face checkpoints and all34 join full/head windows inspected. Complete outfits, consistent scale and fixed architectural anchors remain readable. Modest independent head-height/angle separation causes intentional ghosting during0.75s blend; playback comfort pending.'
d['continuous_playback_review']=False;d['status']='sampled_QA_complete_user_playback_and_picture_approval_pending'
write(p,d)
p=week/'reels/production_manifest.json';m=read(p)
r=next(x for x in m['reels'] if x['model_profile_id']=='M03')
r['status']='film_candidate_sampled_QA_complete_user_picture_approval_pending'
r['qa'].update(status='source_contact_sampling_and_combined_join_sampling_complete',continuous_watch_done=False,user_approval=None,receipt='10_automation/runs/2026-W41/reels/M03/review_v1/composition_receipt.json')
write(p,m)
p=ROOT/'10_automation/production_requests/2026-10-08_next_five_reels.json';req=read(p)
r=next(x for x in req['slots'] if x['model']=='M03');r.update(status='film_candidate_sampled_QA_complete_user_picture_approval_pending',candidate_file=d['output_path'],film_user_approval=None)
write(p,req)
p=week/'publishing_structure.md';s=p.read_text(encoding='utf-8')
s=s.replace('M03兩套輕薄西外全身候選已生成（第一套v2留白修正、第二套v1），使用者已明確核准兩張，接續逐鏡Grok生成與驗收；','M03兩張起始圖已明確核准，已建立並選用Mira M03 v3臉／全身人物參照，兩段Grok原片已保存。11.25秒v1維持原速與0.75秒疊化，已查全身／臉部樣格、全部袖口接觸格與34格轉場；第一套實際整理兩側袖口、第二套整理相反側，與提示詞差異已記錄。成片完整播放與使用者畫面核准待完成，proof／Carousel未完成；')
p.write_text(s,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8')
entry='''## W41 M03 eleven-second pair ready for user playback — 2026-10-08

Exact two approved first frames animated separately with newly created and selected `Mira M03 v3`, built from existing approved face/full identity anchors. Both sources are720×1280/24fps/145frames/6.041667s and audio-free. All145 consecutive hand/cloth windows plus whole-frame25/face5 samples per source inspected. Visible cuff contact and small local cloth response occur; A additionally adjusts the other cuff, B uses opposite laterality and briefly presents the forearm. These variations are recorded, not claimed as exact prompt compliance. No gross face/outfit/hand/shoe/architectural collapse apparent in inspected windows.

Candidate `10_automation/runs/2026-W41/reels/M03/review_v1/2026-W41_M03_two_looks_soft_v1.mp4`:11.25s/270frames, A[0,144), B[0,144), one18-frame0.75s dissolve at output[126,144). Native source speed/pixels unchanged, no text/audio.25 whole-frame,5 face and all34 join full/head windows checked; residual intentional head ghosting during blend. Full-duration normal-speed review and user film approval remain pending. Source/compose receipts saved; no proof/Carousel completion, W41 Drive upload or IG posting claimed. M01/M02 pictures accepted; M05 film/proofs pending; M04 stills next. Old W37 assets preserved. Previously approved public Git checkpoint is synced; this later work remains local.

'''
p.write_text(s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+entry,1),encoding='utf-8')
print(json.dumps({'candidate':d['output_path'],'sha256':d['sha256'],'seconds':d['duration_seconds'],'user_film_approval':None}))
