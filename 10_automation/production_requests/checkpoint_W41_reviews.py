import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
run=root/'10_automation/runs/2026-W41'
manifest_path=run/'reels/production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
for model in ['M05','M01']:
    folder=run/f'reels/{model}/review_v1'
    receipt_path=folder/'composition_receipt.json'
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    video=root/receipt['output_path']
    assert hashlib.sha256(video.read_bytes()).hexdigest()==receipt['sha256']
    review=dict(model=model,week='2026-W41',file=receipt['output_path'],sha256=receipt['sha256'],technical_decode='completed',source_review=dict(full_samples_each=25,face_samples_each=5,scope='sampled images only',findings='Recognizable identity, clothing and stationary background in inspected samples. Actual cuff look-down gesture for M01; higher jacket-edge touch for M05.'),combined_review=dict(full_samples=25,all_boundary_full_samples=34,all_boundary_head_samples=34,findings='Matched whole-person scale and broadly fixed background. Brief face/hand double contours during dissolve are visible; no apparent major scale jump in inspected frames. Normal-speed comfort remains for full playback.'),assistant_continuous_watch_done=False,user_visual_approval=None,status='sampled_QA_checked_user_playback_review_pending')
    (folder/'root_review_2026-10-08.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    receipt.update(combined_visual_QA=review['status'],continuous_playback_review=False,status='candidate_pending_user_playback_review')
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    record=next(r for r in manifest['reels'] if r['model_profile_id']==model)
    record['qa'].update(status=review['status'],continuous_watch_done=False,user_approval=None)
    record['status']='video_candidate_pending_user_playback_review_and_proof_completion'
    if model=='M05':
        for view in record['views']:
            if view['role']=='full' and view['approval']:
                view.update(framing_review='assistant_static_pass_user_approved',clarity_review='assistant_static_pass_user_approved')
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
request_path=root/'10_automation/production_requests/2026-10-08_next_five_reels.json'
request=json.loads(request_path.read_text(encoding='utf-8'))
for s in request['slots']:
    if s['model'] in ['M05','M01']:
        r=next(r for r in manifest['reels'] if r['model_profile_id']==s['model'])
        s.update(status=r['status'],candidate_file=r['output_path'])
request_path.write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('W41 M05/M01 review candidates checkpointed; no final approval inferred.')
