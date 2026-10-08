import csv, hashlib, json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[2]
run = root / '10_automation/runs/2026-W41'
manifest_path = run / 'reels/production_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
record = next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
approved = []
for order, wait in [(1,52.0),(2,40.1)]:
    lid = f'2026-W41-002-L{order:02d}'
    job = run / f'generated_images/2026-W41-002/looks/{lid}/reel'
    file = job / f'{lid}_M01_reel_candidate_A.png'
    with Image.open(file) as im:
        size = list(im.size)
    approval = dict(look_id=lid,file=file.relative_to(root).as_posix(),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),approved_on='2026-10-08',user_quote='兩張都可以，沿用',scope='this exact full-person still as video first frame; no video approval')
    approved.append(approval)
    receipt = dict(look_id=lid, model='M01', path=approval['file'], sha256=approval['sha256'], actual_pixels=size, generator='built_in_image_gen', prompt='production_prompt_v1.txt',reference_face='02_brand/reference_models/M01_start_v4_face.png',reference_full='02_brand/reference_models/M01_start_v4_full.png',tool_wall_seconds=wait,active_minutes=None,status='user_approved_full_person_first_frame',user_approval=approval, dynamic_QA=None,additional_reference_role=None if order==1 else 'L01 scene/camera/scale guide only; own wardrobe lock')
    receipt['assistant_static_review'] = dict(identity='Approved v4 tied-back hair and recognizable face; reference body proportions retained',wardrobe='Own specified plaid palette, tucked shirt, plain trousers and shoes/bag visible',framing='Complete hair and shoes; direct941x1672 portrait; matched paired background and subject placement',gesture_start='Both hands rest near front waist, differing from relaxed side-hands draft; animate from actual pose',limitations='No dynamic or final-film approval inferred')
    (job/'generation_receipt_v1.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sheet=job/'review_sheet.csv'
    with sheet.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
    for key in ['model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity','ai_realism','scene_lighting_integration','outfit_continuity','expression_liveliness','pose_variation','canva_frame_fit','commerce_value']:
        rows[0][key]='4'
    rows[0].update(publishable='yes',status='user_approved_reel_first_frame',notes='Static first-frame approval only; no video or Carousel approval. Actual hands near waist; animation prompt follows visible start pose.')
    with sheet.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    slot=next(v for v in record['views'] if v['look_id']==lid and v['role']=='full')
    slot.update(source_path=approval['file'],source_type='native_reel_approved_still',approval=approval,framing_review='assistant_static_pass_user_approved',clarity_review='assistant_static_pass_user_approved')
record['status']='two_full_first_frames_user_approved_video_generation_next'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt_path=run/'reels/M01_full_pair_user_approval_2026-10-08.json'
receipt_path.write_text(json.dumps(dict(model='M01',week='2026-W41',user_quote='兩張都可以，沿用',files=approved),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
request_path=root/'10_automation/production_requests/2026-10-08_next_five_reels.json'
request=json.loads(request_path.read_text(encoding='utf-8'))
next(s for s in request['slots'] if s['model']=='M01')['status']=record['status']
next(s for s in request['slots'] if s['model']=='M05')['status']='eight_second_video_and_proof_candidates_pending_separate_user_approval'
request_path.write_text(json.dumps(request,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([dict(look=a['look_id'],sha256=a['sha256'],approved=True) for a in approved]))
