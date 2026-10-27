import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[5]
run = root / '10_automation/runs/2026-W37'
image_path = run / 'generated_images/2026-W37-004/looks/2026-W37-004-L01/reel/2026-W37-004-L01_M01_S01_full_start_candidate_v1.png'
relative = str(image_path.relative_to(root)).replace('\\','/')
with Image.open(image_path) as im:
    pixels = list(im.size)
record = dict(look_id='2026-W37-004-L01', model_profile_id='M01', date='2026-10-01',
              status='candidate_pending_user_visual_approval', source_path=relative, pixels=pixels,
              sha256=hashlib.sha256(image_path.read_bytes()).hexdigest(), provider='built_in_imagegen',
              references=['02_brand/reference_models/M01_start_v4_face.png','02_brand/reference_models/M01_start_v4_full.png'],
              prompt_path='10_automation/runs/2026-W37/reels/prompts/M01_A_L01_start_v1.md',
              storyboard_path='10_automation/runs/2026-W37/reels/M01_storyboard_v1.md',
              assistant_review=dict(identity='Face/hair consistent with v4 anchors on visual comparison; user confirmation pending.',
                                    framing='Native vertical9:16 composition; full hair and both shoes visible, forward floor space.',
                                    wardrobe='White short-sleeved collar shirt, high-waisted dark-gray ankle-clear straight trousers, black belt and shoulder bag; burgundy closed-toe low broad heels with one vertical instep strap joining ankle-front strap.',
                                    realism='Light and contact shadows coherent; near-frontal face, front foot planted, back foot position needs normal-speed dynamic validation.',
                                    proof='T intersection visible in full native source; larger lower-body proof still required clarity review.',
                                    text='none'), user_visual_approval=None, grok_submitted=False)
image_path.with_name('S01_full_start_generation_v1.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path = run / 'reels/production_manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
item = next(r for r in manifest['reels'] if r['model_profile_id']=='M01')
view = next(v for v in item['views'] if v['look_id'].endswith('L01') and v['role']=='full')
view.update(source_path=relative,source_type='native_vertical_still_candidate',approval='pending_user_visual_approval',framing_review=record['assistant_review']['framing'],clarity_review=record['assistant_review']['wardrobe'])
item['status']='L01_full_still_candidate_pending_user_visual_approval'
item['storyboard'][0]['source_still_status']='generated_2026-10-01_pending_user_approval'
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(source=relative,pixels=pixels,sha256=record['sha256'])))
