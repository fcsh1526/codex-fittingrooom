from pathlib import Path
import hashlib,json
from PIL import Image
base=Path(__file__).resolve().parent;root=base.parents[1]
for label in ('A','B'):
    p=base/f'{label}_motion_attempt_01/technical_receipt.json'
    r=json.loads(p.read_text(encoding='utf-8'))
    r['visual_review']='25 whole/5 face/all241 thumbnail frames inspected; native endpoint crops checked. No gross identity/wardrobe/background jump seen in reviewed source frames. Whole normal-speed user viewing pending.'
    r['observed_motion']=('Full outfit clear for about first6seconds; actual woman walks toward lens, not isolated camera push-in. Selected0–7.5s.' if label=='A' else 'Pullback from tightly cropped face/torso to full skirt; initial head crop excluded by starting1.25s. Full head/shoes clear from about2.5s onward. Selected1.25–10.0417s.')
    r['source_audio']='AAC observed in source; silent stream-copy review created separately'
    r['all_frame_thumbnails_viewed']=241
    p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=base/'joined_review_v1/edit_receipt.json';r=json.loads(p.read_text(encoding='utf-8'))
r['visual_review']='25 whole-film samples and25 consecutive join frames159–183 viewed. Source faces/outfits/bag broadly retained. Join has visible vertical/scale offset and double outlines, not a seamless bag match. User comfort remains pending.'
r['actual_output']={'pixels':[720,1280],'fps':24,'decoded_frames':372,'seconds':15.5,'audio':False}
r['readable_full_outfit_seconds']={'A':'approximately0–6; no occlusion','B':'source approximately2.5–10.04, output approximately8–15.5','method':'visual sample estimate, not measured eye-tracking or retention'}
r['assistant_continuous_playback']=False
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=base/'M03_still_receipt.json';r=json.loads(p.read_text(encoding='utf-8'))
for label in ('A','B'):
    im=root/r[label]['candidate'];r[label]['pixels']=list(Image.open(im).size);r[label]['sha256']=hashlib.sha256(im.read_bytes()).hexdigest()
r['status']='editorial_pair_not_approved_wall_route_stopped';r['user_feedback_record']='M03_user_editorial_feedback.json'
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
submission={'canvas_url':'https://grok.com/imagine/agent/f040d332-48df-47c4-86d4-28e85c97d5b5?conversation=3f0241af-1184-4a74-9ced-b0b4715a1a95','model':'M04','input_still_approval_record':'10_automation/runs/2026-W41/reels/M04/parallel_first_frame_user_approval_2026-10-08.json','asset_roles_agent_reported':{'A_first_frame':'47b6bf83-510b-4ac3-ac63-51b9e5f6c32e','B_last_frame':'0c3f3221-77f3-4a56-a3f8-8c46e6cc017a','face':'a17c8ba2-3da1-46c4-a308-844387a0102a','full_proportion':'3e946490-8ff6-451f-897a-435e5ac9b675'},'raw_generation_parameters_independently_inspected':False,'first_agent_request':'Stopped because upload filenames unavailable; no generated result','followup':'Observed canvas assetUUIDs supplied; agent reported visual match and generated A/B once each','confirmed_video_results':2,'downloads':['grok-d3e8573e-1b56-410b-9cf3-040d7502bea2-720p.mp4','grok-b55242db-a784-47a8-b044-7864093a3721-720p.mp4'],'active_minutes':None,'wait_minutes':None,'output_user_approval':None,'published':False,'publishing_replacement':False}
(base/'M04_submission_receipt.json').write_text(json.dumps(submission,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(r['status']))
