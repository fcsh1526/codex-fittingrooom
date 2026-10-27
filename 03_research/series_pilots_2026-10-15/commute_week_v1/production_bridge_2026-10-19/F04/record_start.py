from pathlib import Path
import json, hashlib
from PIL import Image

root=Path.cwd()
folder=Path(__file__).resolve().parent
base=folder.parent.parent

def asset(path):
    path=Path(path)
    a={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    if path.suffix.lower()=='.png':
        with Image.open(path) as im:
            a['width'],a['height']=im.size
    return a

candidate=asset(folder/'F04_M03_L02_start_candidate_A.png')
data={
    'record_date_local':'2026-10-20',
    'method':'built_in_image_gen',
    'use_case':'identity-preserve',
    'original_output':'C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-30b7cdaa-72c2-4281-9a5c-a73fb6bb9661.png',
    'candidate':candidate,
    'prompt':asset(folder/'F04_start_candidate_A_prompt.txt'),
    'inputs':[
        {'role':'edit_target_actual_originalF03_frame127',**asset(folder/'F03_actual_frame_000127.png')},
        {'role':'approvedL02_shirt_styling_only',**asset(base/'starting_images/S02_M03_L02_candidate_A.png')},
        {'role':'approvedM03v3_face_identity_only',**asset(root/'02_brand/reference_models/M03_start_v3_face.png')},
        {'role':'approvedM03v3_full_proportions_only',**asset(root/'02_brand/reference_models/M03_start_v3_full.png')}
    ],
    'requested_aspect_ratio':'9:16',
    'post_generation_crop_resize_stretch':False,
    'assistant_sample_review':{
        'observed':['full head and both shoes retained','same near-side profile and rightward passing step','cream/navy check pointed-collar shirt, rolled forearm sleeves and tucked waist visible','charcoal straight trousers, black shoes and shoulder bag retained','dominant stepped planter/tree/glass/paving arrangement remains similar'],
        'limitations':['small regenerated face/hand/foot contours and framing differences possible','not exact pixel geometry','next crossing angle and all motion untested'],
        'dynamic_qa_pass':None,
        'publishable':False
    },
    'status':'candidate_pending_exact_user_visual_approval',
    'Grok_F04_submissions':0,
    'next':'exact start visual approval before compatible crossing endpoint candidate; endpoint separately approved before Grok'
}
with (folder/'F04_start_generation_receipt.json').open('x',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps({'candidate':candidate,'status':data['status']},ensure_ascii=False))
