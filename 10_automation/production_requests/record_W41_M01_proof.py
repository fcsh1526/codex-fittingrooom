import hashlib,json,shutil
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[2]
run=root/'10_automation/runs/2026-W41'
srcroot=Path('C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61')
items=[('2026-W41-002-L01','exec-1df09617-0256-497c-821e-cd43cf78c69f.png','v1',45.4,'candidate_pending_user_visual_approval'),('2026-W41-002-L02','exec-5f326110-9a0b-4d36-993e-31c8eda18e42.png','v1',41.9,'needs_visual_revision_trouser_surface_pattern'),('2026-W41-002-L02','exec-43d5faac-ed4d-4b17-a263-73a3a2e3499f.png','v2',40.4,'needs_visual_revision_residual_trouser_surface_pattern')]
receipts=[]
for lid,srcname,version,wait,status in items:
    job=run/f'generated_images/2026-W41-002/looks/{lid}/reel'
    path=job/f'{lid}_M01_reel_proof_candidate_{version}.png'
    with path.open('xb') as dst,(srcroot/srcname).open('rb') as src:shutil.copyfileobj(src,dst)
    with Image.open(path) as im:size=list(im.size)
    r=dict(look_id=lid,model='M01',role='proof',path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),actual_pixels=size,generator='built_in_image_gen',tool_wall_seconds=wait,status=status,user_approval=None,notes='Head-to-thigh portrait shows cuffs, shirt tuck and waist; same face/scene. L02 decorative-looking trouser surface persists after one targeted edit; no second edit, no dynamic submission, not marked usable.' if lid.endswith('L02') else 'Own approved full-person Hero as wardrobe lock with v4 face/full; cuffs and tuck visible; user visual review pending.')
    (job/f'proof_generation_receipt_{version}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    receipts.append(r)
manifest_path=run/'reels/production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
r=next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
for v in r['views']:
    if v['role']=='proof':
        found=next(i for i in reversed(receipts) if i['look_id']==v['look_id'])
        v.update(source_path=found['path'],source_type='native_vertical_proof_candidate',approval=None,framing_review='assistant_static_pass',clarity_review='candidate_user_pending' if found['look_id'].endswith('L01') else 'needs_visual_revision_surface_pattern')
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([dict(look=i['look_id'],status=i['status']) for i in receipts]))
