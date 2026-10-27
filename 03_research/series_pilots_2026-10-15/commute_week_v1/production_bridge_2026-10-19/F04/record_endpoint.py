from pathlib import Path
import hashlib,json
from PIL import Image

root=Path.cwd()
folder=Path(__file__).resolve().parent
def asset(path):
    path=Path(path)
    a={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size}
    if path.suffix.lower()=='.png':
        with Image.open(path) as im:
            a['width'],a['height']=im.size
    return a

base=asset(folder/'F04_M03_L02_end_candidate_A.png')
corrected=asset(folder/'F04_M03_L02_end_candidate_A_footfix_v2.png')
record={
    'record_date_local':'2026-10-20',
    'method':'built_in_image_gen',
    'base':{
        'asset':base,
        'original_output':'C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-655156e4-ed6d-40c3-8180-cd57964169f6.png',
        'prompt':asset(folder/'F04_end_candidate_A_prompt.txt'),
        'inputs':[
            {'role':'approved_start_identity_exact_outfit_scale',**asset(folder/'F04_M03_L02_start_candidate_A.png')},
            {'role':'site_topology_materials_not_camera',**asset(folder.parent/'environment/E00_shared_scene_candidate_A.png')},
            {'role':'crossing_direction_only_not_figure_bag_side_labels',**asset(folder.parent.parent/'static_key_views_2026-10-16/K3_view.png')},
            {'role':'M03v3_face_identity_only',**asset(root/'02_brand/reference_models/M03_start_v3_face.png')},
            {'role':'M03v3_body_proportions_only',**asset(root/'02_brand/reference_models/M03_start_v3_full.png')}
        ],
        'review':'Crossing behindlowerleft, glassfacade ahead, nosecondroad/doorway. Trailing shoe still touches road/curbedge, so one targeted correction used.',
        'status':'base_preserved_superseded_by_single_foot_correction'
    },
    'single_correction':{
        'asset':corrected,
        'original_output':'C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-5146235c-5091-4e10-8f0c-544092264dbc.png',
        'prompt':asset(folder/'F04_end_foot_correction_prompt.txt'),
        'inputs':[
            {'role':'edit_target_base_endpoint',**base},
            {'role':'approved_start_wardrobe_identity',**asset(folder/'F04_M03_L02_start_candidate_A.png')},
            {'role':'M03v3_face_identity_only',**asset(root/'02_brand/reference_models/M03_start_v3_face.png')},
            {'role':'M03v3_body_proportions_only',**asset(root/'02_brand/reference_models/M03_start_v3_full.png')}
        ],
        'changed_factor':'Trailing knee/lowerleg/shoe clears curb into swing over companyside pavement; supportfoot/hip/torso/camera/background held.',
        'observed':'Trailing shoe now raised above companyside paving instead of touching roadside edge; forwardshoe remains planted, scene/crosswalk/glass/bag arrangement visually similar.',
        'intended_correction_observed_in_still':True
    },
    'requested_aspect_ratio':'9:16',
    'post_generation_crop_resize_stretch':False,
    'base_calls':1,
    'targeted_edit_calls':1,
    'status':'corrected_endpoint_candidate_pending_exact_user_visual_approval',
    'limitations':[
        'rearquarter new angle is inferred from site references; exact geometry not reconstructed or measured',
        'black bag changes screen side duringrearwardcamera arc, but visually stays on same physicalshoulder; not flipped to matchdiagram',
        'minor generated fabric/face/shoe/scenecontours may differ',
        'no motion, turn, foot-ground tracking or crossing continuity pass from still approval'
    ],
    'dynamic_qa_pass':None,'publishable':False,
    'F04_Grok_submissions':0,
    'next':'Exact correctedendpoint approval before one F04 motion between approvedstart and this endpoint'
}
with (folder/'F04_endpoint_generation_and_correction_receipt.json').open('x',encoding='utf-8') as f:
    json.dump(record,f,ensure_ascii=False,indent=2)
    f.write('\n')
print(json.dumps({'base':base,'corrected':corrected,'status':record['status']},ensure_ascii=False))
