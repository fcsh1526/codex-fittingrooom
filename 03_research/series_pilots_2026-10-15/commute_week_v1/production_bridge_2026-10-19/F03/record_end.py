from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
from PIL import Image

root = Path.cwd()
folder = Path(__file__).resolve().parent

def asset(path):
    path = Path(path)
    data = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
    if path.suffix.lower() == '.png':
        with Image.open(path) as im:
            data['width'], data['height'] = im.size
    return data

candidate = asset(folder / 'F03_M03_L03_end_candidate_A.png')
data = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'record_date_local': '2026-10-19',
    'method': 'built_in_image_gen',
    'original_output': 'C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-9d8f00bc-a914-47af-8202-2af81b542402.png',
    'candidate': candidate,
    'prompt': asset(folder / 'F03_end_candidate_A_prompt.txt'),
    'inputs': [
        {'role': 'user_approved_start_same_identity_exact_outfit_person_scale', **asset(folder / 'F03_M03_L03_start_candidate_A.png')},
        {'role': 'approved_site_topology_materials_only_not_elevated_camera', **asset(folder.parent / 'environment/E00_shared_scene_candidate_A.png')},
        {'role': 'M03_v3_face_identity_only', **asset(root / '02_brand/reference_models/M03_start_v3_face.png')},
        {'role': 'M03_v3_body_proportions_only', **asset(root / '02_brand/reference_models/M03_start_v3_full.png')}
    ],
    'requested_aspect_ratio': '9:16',
    'post_generation_crop_resize_stretch': False,
    'visual_review': {
        'scope': 'assistant inspection of endpoint still only',
        'observed': ['full head and both shoes', 'side-profile rightward mid-stride', 'ivory short jacket, white crew T, charcoal straight trousers, black shoes and shoulder bag retained', 'no pillar or long corridor ahead', 'curb and zebra-crossing beginning at frame right; both feet still on near-side paving', 'green-gray glass facade and trees, coherent dappled daylight'],
        'deviations_or_limits': ['large stepped planter is more prominent than in starting view', 'new curb, crossing and facade visibility are generated geometry, not measured continuity', 'minor shoe, hand and fabric contours regenerated', 'normal-speed gait and travel distance remain untested'],
        'dynamic_qa_pass': None,
        'publishable': False
    },
    'status': 'candidate_pending_exact_user_visual_approval',
    'grok_submission_count_F03': 0,
    'next': 'exact endpoint approval before one bounded F03 motion generation'
}
with (folder / 'F03_end_generation_receipt.json').open('x', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps({'candidate': candidate, 'status': data['status']}, ensure_ascii=False))
