import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '10_automation/runs/2026-W41'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

film = BASE / 'reels/M01/review_v2/composition_receipt.json'
receipt = read(film)
review = {
    'date': '2026-10-08',
    'film': receipt['output_path'],
    'film_sha256': receipt['sha256'],
    'B_source_sha256': receipt['sources'][1]['sha256'],
    'source_inspection': {
        'whole_frame_samples': 25,
        'face_samples': 5,
        'consecutive_hand_cloth_images': 145,
        'observed_contact': 'Fingers close at the visible forearm fold; local cloth gathers and moves with the hand, followed by release and return toward waist.',
        'deviation': 'Sustained small adjustment rather than one instantaneous tug; fold height moves modestly.'
    },
    'combined_inspection': {
        'whole_frame_samples': 25,
        'consecutive_join_full_images': 34,
        'consecutive_join_head_images': 34,
        'observations': 'Similar full-person scale and placement, broadly coherent bookstore geometry/exposure in inspected images; brief doubled outlines during the deliberate dissolve. No apparent major face pop or scene drift in inspected images.'
    },
    'scope': 'Image inspection and complete technical decode only; not continuous normal-speed playback or user acceptance.',
    'A_retained_unchanged': True,
    'continuous_playback_review': False,
    'user_approval': None,
    'status': 'sampled_review_complete_pending_user_playback',
    'prior_v1': 'Rejected by user for B hand-cloth interaction; preserved.'
}
review_path = BASE / 'reels/M01/review_v2/root_review_2026-10-08.json'
if review_path.exists():
    raise SystemExit('Review already recorded; do not overwrite.')
write(review_path, review)
receipt['combined_visual_QA'] = '25 whole-film and all34 boundary whole/head images inspected; no apparent major scale/face/scene discontinuity in inspected images. Intentional dissolve overlap retained. Separate normal-speed user review pending.'
receipt['status'] = 'candidate_pending_user_playback_review'
receipt['review_receipt'] = review_path.relative_to(ROOT).as_posix()
write(film, receipt)
contact_path = BASE / 'reels/M01/QA_B02_contact/contact_inspection.json'
contact = read(contact_path)
contact['contact_visual_result'] = review['source_inspection']
contact['user_approval'] = None
write(contact_path, contact)
manifest_path = BASE / 'reels/production_manifest.json'
manifest = read(manifest_path)
entry = next(x for x in manifest['reels'] if x['model_profile_id'] == 'M01')
assert entry['output_path'] == receipt['output_path']
entry['qa'].update(status='sampled_review_complete_pending_user_playback', continuous_watch_done=False, user_approval=None, review_receipt=review_path.relative_to(ROOT).as_posix())
entry['status'] = 'corrected_video_candidate_pending_user_playback_and_proof_completion'
write(manifest_path, manifest)
request_path = ROOT / '10_automation/production_requests/2026-10-08_next_five_reels.json'
request = read(request_path)
slot = next(x for x in request['slots'] if x['model'] == 'M01')
slot['candidate_file'] = receipt['output_path']
slot['status'] = entry['status']
slot['final_file'] = None
slot['prior_candidate_status'] = 'review_v1_rejected_by_user_B_hand_cloth_contact; preserved'
write(request_path, request)
status_path = ROOT / 'CURRENT_STATUS.md'
status = status_path.read_text(encoding='utf-8-sig')
old = 'B2 has been submitted; generation and contact QA are pending. Do not call the correction passed merely because the prompt was submitted.'
new = 'B2 is generated and saved separately. All145 consecutive hand/cloth-window images plus25 full and5 face samples show fold grasp/local cloth response followed by release; the adjustment is sustained with a modest fold-height change. New review_v2 is9.5s/228frames, retaining original A[0,114), B2[12,144) and one18-frame0.75s dissolve, native speed and no text/audio/transforms. Technical full decode,25 whole-film and all34 boundary whole/head images checked. The v2 root review records limited visual evidence; continuous normal-playback and user film approval remain pending. The old v1 review question is superseded by rejection; no acceptance of this repair is inferred.'
assert old in status
status_path.write_text(status.replace(old, new, 1), encoding='utf-8')
pub_path = BASE / 'publishing_structure.md'
pub = pub_path.read_text(encoding='utf-8-sig')
old_pub = 'M01兩張格紋全身起始圖已核准，兩段Grok來源與8.25秒合片也已保存，成片待完整播放與視覺核准；'
new_pub = 'M01兩張格紋全身起始圖已核准；8.25秒v1因第二鏡手與袖口無實際互動被使用者退回，原檔保留。第二鏡已針對折邊接觸重做一次，9.5秒v2保留第一鏡與0.75秒疊化，逐格接觸及成片抽查已完成，待完整播放與使用者視覺核准；'
assert old_pub in pub
pub_path.write_text(pub.replace(old_pub, new_pub, 1), encoding='utf-8')
print('M01 v2 checkpoint recorded; user playback/approval pending.')
