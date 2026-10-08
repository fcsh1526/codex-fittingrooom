import csv
import hashlib
import json
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '10_automation/.video_dependencies'))
from PIL import Image

root = Path(__file__).resolve().parents[2]
run = root / '10_automation/runs/2026-W41'
folder = run / 'generated_images/2026-W41-001/looks'
second = folder / '2026-W41-001-L02/reel/2026-W41-001-L02_M05_reel_candidate_A.png'
source = Path('C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-232528ce-6bbf-4486-9973-f4346b3ff850.png')
if not second.exists():
    shutil.copyfile(source, second)
else:
    assert second.read_bytes() == source.read_bytes()
observations = []
for order, wait in [(1,45.6),(2,39.6)]:
    lid = f'2026-W41-001-L{order:02d}'
    job = folder / lid / 'reel'
    file = job / f'{lid}_M05_reel_candidate_A.png'
    with Image.open(file) as im:
        size = list(im.size)
    receipt = dict(look_id=lid, model='M05', role='reel_full_A', path=file.relative_to(root).as_posix(),
        sha256=hashlib.sha256(file.read_bytes()).hexdigest(), actual_pixels=size,
        composition='direct_native_portrait_9x16', generator='built_in_image_gen',
        prompt='production_prompt_v1.txt', reference_face='02_brand/reference_models/M05_start_v1_face.png',
        reference_full='02_brand/reference_models/M05_start_v1_full.png',
        additional_reference_role=None if order==1 else 'L01 candidate is scene/camera/scale guide only; no wardrobe approval transferred',
        tool_wall_seconds=wait, human_active_minutes=None,
        assistant_static_review=dict(identity='recognizable face/hair; no numeric age in prompt',
            outfit='planned jacket/collar/tee/trousers/black belt/shoes/bag visible',
            framing='complete hair and both shoes; overhead and floor margins; centered width',
            hands='relaxed separate hands without prominent apparent deformation',
            integration='shared left daylight and floor contact shadows',
            continuity='paired still positions and background appear closely matched; not a dynamic pass'),
        status='candidate_pending_user_visual_approval', user_approval=None,
        grok_submitted=False, dynamic_QA=None)
    (job/'generation_receipt_v1.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sheet = job/'review_sheet.csv'
    with sheet.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream); fields=reader.fieldnames; rows=list(reader)
    row=rows[0]
    for key in ['model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity',
        'ai_realism','scene_lighting_integration','outfit_continuity','expression_liveliness',
        'pose_variation','canva_frame_fit','commerce_value']:
        row[key]='4'
    row.update(publishable='pending',status='candidate_pending_user_visual_approval',
        notes='Assistant static check only. Native 941x1672 framing, full shoes/hair, near-frontal identity. Scene/scale pair matched. No Grok or video approval; user image question pending.')
    with sheet.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    observations.append(receipt)
manifest_path=run/'reels/production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
record=next(r for r in manifest['reels'] if r['model_profile_id']=='M05')
for slot in record['views']:
    if slot['role']=='full':
        observation=next(x for x in observations if x['look_id']==slot['look_id'])
        slot.update(source_path=observation['path'],source_type='native_reel_candidate',approval=None,
            framing_review='assistant_static_pass_user_pending', clarity_review='assistant_static_pass_user_pending')
record['status']='two_full_candidates_waiting_user_visual_approval'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'look':x['look_id'],'pixels':x['actual_pixels'],'status':x['status']} for x in observations]))
