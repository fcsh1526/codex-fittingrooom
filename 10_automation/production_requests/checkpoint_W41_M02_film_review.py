import json, hashlib
from pathlib import Path

root=Path(__file__).resolve().parents[2]
work=root/'10_automation/runs/2026-W41/reels/M02'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary_path=work/'review_v2/visual_review_2026-10-08.json'
if summary_path.exists(): raise FileExistsError('Preserve existing review.')
findings='25 whole-film and5 face checkpoints plus all34 transition-boundary full/head windows inspected. Both complete outfits are readable outside the dissolve. V2 enters B at1s, narrowing the vertical face separation versus B0 in v1; residual double-face/body and cafe-geometry overlap remains during the intended0.75s dissolve. No apparent gross face, hand, bag, shoe or background collapse in inspected source/checkpoint windows. This sampling does not establish full normal-speed comfort or a complete identity-stability pass; user playback review remains required.'
for version in ['review_v1','review_v2']:
    p=work/version/'composition_receipt.json'; r=read(p)
    assert r['sha256']==hashlib.sha256((root/r['output_path']).read_bytes()).hexdigest()
    r['combined_visual_QA']=findings if version=='review_v2' else '25 full/5 face and all34 boundary full/head windows inspected. Wider vertical face separation during dissolve; retained as comparison. V2 uses later B entry to reduce it. No user approval inferred.'
    r['status']='candidate_sampled_QA_complete_user_playback_pending' if version=='review_v2' else 'preserved_comparison_superseded_by_review_v2'
    save(p,r)
r=read(work/'review_v2/composition_receipt.json')
save(summary_path,dict(week='2026-W41',model='M02',film=r['output_path'],sha256=r['sha256'],frames=216,seconds=9,fps=24,native_pixels=[720,1280],transition_seconds=.75,source_speed='unchanged',text='none',audio='none',findings=findings,continuous_watch_done=False,user_approval=None,proof_and_carousel='incomplete',prior_batch_write=False))
p=root/'10_automation/runs/2026-W41/reels/production_manifest.json'; m=read(p)
record=next(x for x in m['reels'] if x['model_profile_id']=='M02')
record['status']='film_candidate_sampled_QA_complete_user_playback_pending_proof_carousel_incomplete'
record['qa'].update(status='source_and_combined_sampling_reviewed_user_playback_pending',continuous_watch_done=False,user_approval=None,visual_review=summary_path.relative_to(root).as_posix())
save(p,m)
p=root/'10_automation/production_requests/2026-10-08_next_five_reels.json'; req=read(p)
slot=next(x for x in req['slots'] if x['model']=='M02')
slot.update(status='film_candidate_pending_user_playback_proof_and_carousel_incomplete',candidate_file=r['output_path'],candidate_sha256=r['sha256'],final_file=None,previous_candidate='review_v1 preserved; larger face-position separation at dissolve')
save(p,req)
p=root/'10_automation/runs/2026-W41/publishing_structure.md'; txt=p.read_text(encoding='utf-8')
txt=txt.replace('逐鏡影片生成與驗收待完成；先前褲面異常版本保留且不送Grok。','兩段Grok來源已下載，各為720×1280／24fps／145格且無聲；全身與臉部抽查及全部腳部逐格檢視已完成。九秒v2採0.75秒疊化，第二套入點後移一秒減少臉部位置差，成片抽查及34格接點檢視已完成，仍待使用者完整播放核准；proof與Carousel未完成。先前褲面異常版本保留且不送Grok。')
p.write_text(txt,encoding='utf-8')
p=root/'CURRENT_STATUS.md'; txt=p.read_text(encoding='utf-8')
heading='# Current Status - Mira AI Fashion Creator\n\n'
assert txt.startswith(heading)
new='''## W41 M02 nine-second v2 candidate ready for playback; authorized Git checkpoint synced — 2026-10-08

The standalone user answer `同意公開上述 W41 檢查點` explicitly authorizes the previously described328-file78.7MB checkpoint to the public `fcsh1526/codex-fittingrooom` repository. Normal push succeeded, origin main `a1ee60c..0c1f93b`; receipt records full commit `0c1f93b12dafd7f16a2cecedac20f4ab50f9186b`. Earlier rejections are historical and resolved for this exact scope. No blanket authorization for unrelated or future sensitive records is inferred; subsequent M02 video work is saved locally.

Both approved M02 full-person sources were animated using saved `Mira M02 v3`, each own first frame, fixed full-person view,720p/6s/9:16/audio off. Actual files are720×1280,24fps,145frames/6.041667s and no audio. Source full/face checkpoints and every lower-body frame were inspected; approach, catch-up and several stance adjustments occur rather than an exact single foot placement. No gross foot/shoe/denim collapse was apparent in inspected windows. V1 is preserved; v2 retains A[0,114), enters B[24,144), and applies one18-frame0.75s dissolve. Moving B's entry one second later narrows vertical face separation; residual intentional dissolve overlap and small independent cafe-geometry differences remain. New film is9s/216frames with unchanged speed, no framing transform, text or audio. Whole-film25/face5 and all34 boundary full/head windows inspected; continuous normal-speed viewing remains false and user film approval pending. Exact candidate: `10_automation/runs/2026-W41/reels/M02/review_v2/2026-W41_M02_two_looks_soft_v2.mp4`.

M01 v2 picture remains accepted; M05 film/proofs pending; M03/M04 new stills pending. M02 proof/Carousel incomplete. No W41 Drive upload or Instagram publication and no W37 original replacement. Next: show exact M02 v2 for user playback/visual approval, then continue remaining batch assets.

'''
txt=heading+new+txt[len(heading):]
txt=txt.replace('The same direct response follows the explicit question authorizing public GitHub synchronization of the concrete328-file W41 checkpoint; bounded authorization is saved in its sync receipt and a normal push is pending.','That compound response was not accepted by automatic review as standalone public-sharing authorization. A subsequent separate explicit user answer resolved this for the concrete328-file checkpoint, and the normal push succeeded; see the latest entry above.')
p.write_text(txt,encoding='utf-8')
print(json.dumps(dict(film=r['output_path'],sha256=r['sha256'],seconds=9,status=record['status']),ensure_ascii=False))
