import hashlib, json
from pathlib import Path

root=Path(__file__).resolve().parents[2]
base=root/'10_automation/runs/2026-W41'
folder=base/'reels/M02/review_v2'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=folder/'user_picture_approval_2026-10-08.json'
if target.exists(): raise SystemExit('Already recorded; preserve original approval.')
receipt=read(folder/'composition_receipt.json')
assert hashlib.sha256((root/receipt['output_path']).read_bytes()).hexdigest()==receipt['sha256']
assert receipt['sha256']=='d33dac1868d9e78faf63556fb7df6bf647252e255b8ff940920c63af0cb82b24'
approval=dict(date='2026-10-08',user_quote='可以。這個是之前研究其他帳號所得到的短走方式嗎?',
 context='Direct response to displayed exact M02 nine-second v2 film and request to confirm short walk, transition and background.',
 file=receipt['output_path'],sha256=receipt['sha256'],
 scope='Accept this exact film picture for use; not other stills, proof/Carousel assets, other films, a mandatory weekly format or audience-performance claims.',
 user_full_duration_playback_self_report=None,assistant_continuous_playback_review=False,status='user_picture_accepted',
 prior_v1='Comparison preserved; no retrospective approval.')
save(target,approval)
approval_rel=target.relative_to(root).as_posix()
receipt.update(user_approval=approval_rel,status='user_picture_accepted');save(folder/'composition_receipt.json',receipt)
p=folder/'visual_review_2026-10-08.json'; review=read(p)
review.update(user_approval=approval_rel,status='sampled_review_complete_user_picture_accepted');save(p,review)
p=base/'reels/production_manifest.json'; manifest=read(p)
entry=next(x for x in manifest['reels'] if x['model_profile_id']=='M02')
assert entry['output_path']==receipt['output_path']
entry['status']='film_picture_accepted_proof_and_carousel_incomplete'
entry['qa'].update(user_approval=approval_rel,status='sampled_review_complete_user_picture_accepted')
save(p,manifest)
p=root/'10_automation/production_requests/2026-10-08_next_five_reels.json'; req=read(p)
slot=next(x for x in req['slots'] if x['model']=='M02')
slot.update(status=entry['status'],accepted_picture_file=receipt['output_path'],user_approval=approval_rel,final_file=None);save(p,req)
p=base/'reels/batch_storyboard.json'; boards=read(p)
film=next(x for x in boards['films'] if x['reel_id']=='2026-W41-M02-reel')
film.update(output_status=entry['status'],actual_duration=9,output_path=receipt['output_path'],user_video_approval=approval_rel)
film['research_lineage']={
 'source':'03_research/ig_saved_ootd_study_2026-10-06/independent_review.md',
 'observed_references':['jenaby.u DJnnv5OPD6k','gaya_yaa DY6W8peI7LC'],
 'borrowed_principle':'Subject distance/scale changes can structure clothing viewing, with a readable settle.',
 'editorial_adaptation':'Fixed full-person camera and brief forward approach, rather than the references full near/far/side/back sequence. Actual output includes catch-up and stance adjustments.',
 'transition_origin':'User decision:0.75s soft cross dissolve; not attributed to the reference accounts.',
 'performance':'No causal reach or retention conclusion; references were screenshot samples and page like counts.'}
save(p,boards)
p=base/'publishing_structure.md'; txt=p.read_text(encoding='utf-8')
txt=txt.replace('仍待使用者完整播放核准；proof與Carousel未完成。','使用者回覆「可以」核准九秒v2畫面，完整播放自述尚無紀錄；proof與Carousel未完成。',1)
p.write_text(txt,encoding='utf-8')
p=root/'CURRENT_STATUS.md'; txt=p.read_text(encoding='utf-8')
heading='# Current Status - Mira AI Fashion Creator\n\n'
new='## W41 M02 v2 picture accepted; short-walk research lineage clarified — 2026-10-08\n\nUser directly replies `可以。這個是之前研究其他帳號所得到的短走方式嗎?` to the displayed exact9s M02 v2. Hash verified; bounded picture approval saved at `10_automation/runs/2026-W41/reels/M02/review_v2/user_picture_approval_2026-10-08.json`. No full-duration playback self-report or assistant continuous watch inferred. The fixed-camera short approach is an editorial simplification of subject near/far viewing observed in jenaby.u and gaya_yaa saved-OTT D research; reference motion is not copied shot-for-shot and0.75s dissolve comes from user feedback. Research lineage saved in the M02 batch storyboard. Actual output contains short approach, catch-up and stance adjustments. This acceptance does not set a universal weekly format or establish reach performance. M01 and M02 pictures now accepted; their proof/Carousel incomplete. M05 picture/proofs pending; M03/M04 new stills pending. Previously authorized checkpoint0c1f93b remains synced; subsequent production saved locally. No W41 Drive upload/IG publication or W37 overwrite.\n\n'
assert txt.startswith(heading)
p.write_text(heading+new+txt[len(heading):],encoding='utf-8')
print('M02 exact film acceptance and research lineage saved; outstanding batch assets preserved.')
