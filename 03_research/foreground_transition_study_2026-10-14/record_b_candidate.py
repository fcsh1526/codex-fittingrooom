from pathlib import Path
import csv, hashlib, json
from PIL import Image

root = Path(__file__).resolve().parents[2]
base = Path(__file__).resolve().parent
reel = root / '10_automation/runs/2026-W41/generated_images/2026-W41-003/looks/2026-W41-003-L02/reel'
asset = reel / 'foreground_transition_2026-10-14/2026-W41-003-L02_M02_reveal_candidate_v2.jpg'
receipt = {
    'date': '2026-10-14', 'model': 'M02', 'look_id': '2026-W41-003-L02',
    'tool': 'Grok canvas left agent composer',
    'file': asset.relative_to(root).as_posix(),
    'sha256': hashlib.sha256(asset.read_bytes()).hexdigest(),
    'native_pixels': list(Image.open(asset).size),
    'native_format': Image.open(asset).format,
    'agent_submissions': 2, 'scope': 'one initial still plus one wall-material-only correction',
    'status': 'candidate_pending_user_visual_approval', 'user_visual_approval': None,
    'video_submissions_for_B': 0,
    'source_roles': {
        'M02_start_v3_face.png': 'identity; selected existing uploaded asset',
        '2026-W41-003-L02_M02_reel_candidate_A_v3.png': 'own look wardrobe and full-person proportions; selected existing uploaded asset',
        'approved A canvas video': 'cafe daylight and wall material; selected canvas node',
        'M02_start_v3_full.png': 'approved local anchor inspected; not successfully newly attached to Grok in this turn'
    },
    'visual_review': {
        'full_native_candidate_viewed': True,
        'findings': ['M02 face and low brown bun remain recognizable against inspected approved references.',
                     'White pointed-collar short-sleeve shirt, cocoa denim, narrow black belt, small shoulder bag and both loafers readable.',
                     'Complete head and both shoes retained; no image text or extra person visible.',
                     'Left foreground wall remains about 30 percent rather than originally requested 15 percent; it does not occlude the outfit.',
                     'Correction removes coarse mottled stone and makes wall fine grey-beige plaster; blur and tone are not a proven pixel match to A ending.',
                     'This is a clear reveal-side keyframe, not an all-wall first frame or verified continuation of cafe architecture.'],
        'image_to_video_reference_execution_verified': False,
        'complete_join_verified': False
    },
    'agent_reported_video_input_support': {
        'first': 'first_frame_asset_id', 'last': 'last_frame_asset_id',
        'identity': 'asset_ids plus @asset_id in prompt',
        'evidence': 'agent reply only; not independently executed or confirmed in actual video input UI'
    },
    'canvas_url': 'https://grok.com/imagine/agent/f040d332-48df-47c4-86d4-28e85c97d5b5?conversation=3f0241af-1184-4a74-9ced-b0b4715a1a95',
    'download_name': 'grok-24a1b901-8206-4e0b-9706-e380ba23a93a.jpg',
    'history_deleted': False, 'publishing_files_replaced': False
}
(base / 'B_start_still_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
sheet = reel / 'review_sheet.csv'
with sheet.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f); rows = list(reader); fields = reader.fieldnames
identifier = '2026-W41-003-L02_foreground_reveal_v2'
if not any(row.get('prompt_id') == identifier for row in rows):
    row = dict(carousel_id='2026-W41-003', look_id='2026-W41-003-L02', prompt_id=identifier,
               model_profile_id='M02', candidate_file=asset.relative_to(reel).as_posix(),
               tool='Grok canvas agent', publishable='not_assessed',
               status='candidate_pending_user_visual_approval',
               notes='Clear reveal-side keyframe; one wall material correction completed. Full native still reviewed. New image gate pending; no B video or join executed.')
    rows.append({field: row.get(field,'') for field in fields})
    with sheet.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
print(json.dumps({'pixels':receipt['native_pixels'],'sha256':receipt['sha256'],'status':receipt['status']}))
