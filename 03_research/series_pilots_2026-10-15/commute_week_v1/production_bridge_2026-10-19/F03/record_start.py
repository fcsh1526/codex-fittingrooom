from pathlib import Path
import hashlib, json
from datetime import datetime, timezone
from PIL import Image

root = Path.cwd()
folder = Path(__file__).resolve().parent
base = root / '03_research/series_pilots_2026-10-15/commute_week_v1'

def asset(path):
    path = Path(path)
    result = {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
    if path.suffix.lower() == '.png':
        with Image.open(path) as im:
            result['width'], result['height'] = im.size
    return result

def write_new(name, data):
    with (folder / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

candidate = asset(folder / 'F03_M03_L03_start_candidate_A.png')
data = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'record_date_local': '2026-10-19',
    'use_case': 'identity-preserve',
    'method': 'built_in_image_gen',
    'original_output': 'C:/Users/Brandon_ChangChien/.codex/generated_images/01a0a39c-4727-7593-ac24-1a8727f9ff61/exec-907ade50-7544-40b4-b8d7-8130386aa6e8.png',
    'project_copy': candidate,
    'prompt': asset(folder / 'F03_start_candidate_A_prompt.txt'),
    'requested_aspect_ratio': '9:16',
    'post_generation_crop_resize_stretch': False,
    'generation_wait_seconds': 49.024,
    'inputs': [
        {'role': 'edit_target_actual_corrected_F02_frame127', **asset(folder / 'F02_actual_frame_000127.png')},
        {'role': 'approved_L03_wardrobe_only', **asset(base / 'starting_images/S03_M03_L03_candidate_A_refined_v2.png')},
        {'role': 'approved_M03_v3_face_identity_only', **asset(root / '02_brand/reference_models/M03_start_v3_face.png')},
        {'role': 'approved_M03_v3_body_proportions_only', **asset(root / '02_brand/reference_models/M03_start_v3_full.png')}
    ],
    'visual_review': {
        'scope': 'assistant inspection of generated still only; not motion or measured pixel geometry',
        'observed': ['full head and both shoes visible', 'similar large person scale and rightward stride as frame127', 'ivory short stand-collar open jacket, white crew T and charcoal trousers visible', 'black shoulder bag and low heels visible', 'same dominant square-column, tree, planter, glass-grid and paving arrangement retained'],
        'remaining_limits': ['fabric and shoe contours regenerated', 'small pose/edge differences possible', 'native aspect-ratio raster rounding recorded without normalization', 'motion, scene progression and neighboring dissolve not yet tested'],
        'dynamic_qa_pass': None,
        'publishable': False
    },
    'generation_status': 'candidate_pending_exact_user_visual_approval_at_generation_time'
}
write_new('F03_start_generation_receipt.json', data)
approval = {
    'record_date_local': '2026-10-19',
    'asset': candidate,
    'question': '剛顯示的 M03 第三套起始圖：臉、米白短立領外套／白T／炭灰褲、黑鞋包，以及承接前鏡的跨步與柱廊構圖，是否可以沿用？依你在 AGENTS.md 設定的「新圖先視覺核准」流程，確認後才會製作同廣場路緣前的末幀；影片仍待兩張都核准。',
    'user_answer': '可以，沿用這張',
    'status': 'exact_F03_start_still_user_approved',
    'scope': 'exact still appearance and authority to prepare compatible endpoint candidate; does not approve endpoint, motion, neighboring join or full five-look film',
    'next': 'endpoint still candidate and exact visual approval before Grok'
}
write_new('F03_start_user_still_approval_2026-10-19.json', approval)
print(json.dumps({'candidate': candidate, 'approval_status': approval['status']}, ensure_ascii=False))
