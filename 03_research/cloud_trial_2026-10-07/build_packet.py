"""Create a bounded M02 transfer packet without altering any production inputs."""
import csv
import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TRIAL = Path('03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial')
BASE = Path('10_automation/runs/2026-W37/generated_images/2026-W37-001/looks')
PAIRED = Path('10_automation/runs/2026-W37/reels/M02_paired_D_v1')
FILES = []


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def copy(source, target, role, expected=None):
    src, dst = ROOT / source, HERE / target
    actual = sha(src)
    if expected and actual != expected:
        raise ValueError(f'Approved input changed: {source}')
    if dst.exists():
        raise FileExistsError(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    if sha(dst) != actual:
        raise ValueError('Copy mismatch')
    FILES.append({'path': target, 'source_project_path': str(source).replace('\\', '/'),
                  'role': role, 'sha256': actual, 'size_bytes': dst.stat().st_size})


def save_json(target, value, role):
    dst = HERE / target
    if dst.exists():
        raise FileExistsError(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    FILES.append({'path': target, 'role': role, 'sha256': sha(dst), 'size_bytes': dst.stat().st_size})


def main():
    copy('02_brand/reference_models/M02_start_v3_face.png', 'inputs/M02_face.png', 'approved_identity_face',
         'b214676fb8b24b77654ac76d12be06a9b6f1101d1fca48083ba3bcbb740706f5')
    copy('02_brand/reference_models/M02_start_v3_full.png', 'inputs/M02_full.png', 'approved_identity_full',
         '2282c4fb3e35f8adb99b51aec4a55afa9402f1c60492503c555beecea6914ac4')
    a = BASE / '2026-W37-001-L01/reel/backward_step_v2'
    b = BASE / '2026-W37-001-L02/reel/body_distance_matched_start_v2'
    copy(a / '2026-W37-001-L01_M02_fixed_camera_near_start_candidate_v2.png', 'inputs/A_near_start_v2.png',
         'approved_first_frame_L01', 'e85778d9d38b7541cc5cf96fb73ea047c26da22c8179fe10b8c30f5c38356cb7')
    copy(b / '2026-W37-001-L02_M02_body_distance_matched_start_candidate_v3.png', 'inputs/B_matched_start_v3.png',
         'approved_first_frame_L02', 'f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6')
    copy(a / 'visual_approval_v2_2026-10-06.json', 'evidence/A_still_approval.json', 'exact_still_approval')
    copy(b / 'visual_approval_v3_2026-10-07.json', 'evidence/B_still_approval.json', 'exact_still_approval')
    copy(TRIAL / 'near_start_A_attempt_01/source.mp4', 'inputs/source_A.mp4', 'retained_reviewed_L01_source',
         'be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea')
    for look, suffix, role, expected in [
        ('L01', 'full_master', 'approved_full_person_L01', 'adf1d4fb2e55262b53d7763a65d5406edd92efe01f3b48ff2170f3d000fb071e'),
        ('L01', 'proof', 'approved_styling_proof_L01', '6c3c36d53e894f4be8aa1de1f7eef70749f15e0e906421d26bb838c74bed18bf'),
        ('L02', 'full_master', 'approved_full_person_L02', '48a85af156bfadf00afdc217a4e13fbb51750540a638290f2108bd1cc0b36b0a'),
        ('L02', 'proof', 'approved_styling_proof_L02', '1ea5251c0346edc52e38d414c5c52156a4c41e0a74d08d05c3140b196994dd77')]:
        look_id = f'2026-W37-001-{look}'
        source = BASE / look_id / 'reel/paired_scene_v1' / f'{look_id}_M02_reel_{suffix}_candidate_v1.png'
        copy(source, f'inputs/{look}_{suffix}.png', role, expected)
    for name in ['L01_full_visual_approval_2026-10-05.json',
                 'paired_still_visual_approvals_2026-10-05.json', 'L02_proof_visual_approval_2026-10-05.json']:
        copy(PAIRED / name, 'evidence/' + name, 'four_view_still_approval')
    for name in ['input_receipt.json', 'retrieval.json', 'sampled_review.json', 'submitted_prompt.txt']:
        copy(TRIAL / 'near_start_A_attempt_01' / name, 'evidence/A_' + name, 'historical_A_provenance')
    for name in ['actual_metadata.json', 'decode_scan.json', 'independent_review.md',
                 'full_25_checkpoints.jpg', 'face_5_checkpoints.jpg']:
        copy(TRIAL / 'qa/near_A1' / name, 'evidence/A_QA/' + name, 'historical_sampled_QA_not_full_watch')
    copy(TRIAL / 'matched_B_attempt_01/prompt.txt', 'prompts/B_approach.txt', 'approved_still_motion_plan')
    copy(TRIAL / 'revised_storyboard_v3.md', 'evidence/revised_storyboard_v3.md', 'historical_storyboard_current_approvals_override')
    copy(TRIAL / 'matched_B_source_plan_oct07.md', 'evidence/matched_B_source_plan_oct07.md', 'historical_plan_current_state_override')
    for source, target in [
        ('10_automation/CANONICAL_WORKFLOW.md', 'workflow/CANONICAL_WORKFLOW.md'),
        ('CURRENT_STATUS.md', 'workflow/CURRENT_STATUS_snapshot.md'),
        ('10_automation/runs/2026-W37/publishing_structure.md', 'workflow/publishing_structure_snapshot.md'),
        ('09_sops/mira_reel_production_sop.md', 'workflow/mira_reel_production_sop.md'),
        ('11_skills/mira-image-daily/SKILL.md', 'workflow/mira-image-daily/SKILL.md'),
        ('11_skills/mira-image-daily/references/image-standard.md', 'workflow/mira-image-daily/references/image-standard.md'),
        ('11_skills/mira-image-daily/references/reference-start-images.md', 'workflow/mira-image-daily/references/reference-start-images.md')]:
        copy(source, target, 'workflow_snapshot')
    with (ROOT / '10_automation/runs/2026-W37/weekly_look_plan.csv').open(encoding='utf-8-sig', newline='') as stream:
        looks = [row for row in csv.DictReader(stream) if row['model_profile_id'] == 'M02']
    if len(looks) != 2 or {r['look_id'] for r in looks} != {'2026-W37-001-L01', '2026-W37-001-L02'}:
        raise ValueError('Unexpected M02 look set')
    save_json('inputs/M02_looks.json', {'original_weekly_rows': looks,
        'current_trial_override': {'scene_both_looks': 'common library scene in approved trial stills',
        'L02_original_floral_scene': 'historical weekly source; do not use for this motion trial',
        'native_four_views': 'two full-person and two proof assets individually approved; four clips not required'}}, 'two_weekly_looks_and_current_scene')
    with (ROOT / '02_brand/mira_reference_images.csv').open(encoding='utf-8-sig', newline='') as stream:
        identity = next(row for row in csv.DictReader(stream) if row['model_profile_id'] == 'M02')
    if identity['status'] != 'approved' or identity['reference_version'] != 'v3':
        raise ValueError('M02 identity version changed')
    save_json('inputs/M02_identity.json', identity, 'approved_identity_registry_row')
    prior = json.loads((ROOT / TRIAL / 'M02_body_distance_review_v1.json').read_text(encoding='utf-8'))
    protected = prior['protected_media']
    for item in protected:
        if sha(ROOT / item['path']) != item['sha256']:
            raise ValueError('Protected original changed: ' + item['path'])
    save_json('evidence/protected_originals.json', {'verified_on_local_date': '2026-10-07',
        'policy': 'Originals stay outside packet. Do not overwrite, move, rename or replace their Drive IDs.',
        'records': protected}, 'local_protected_originals_verified_not_transferred')
    manifest = {'packet_version': 1, 'created_local_date': '2026-10-07', 'week': '2026-W37', 'model': 'M02',
        'scope': 'Cloud trial preparation. No new B source, final candidate, cloud execution or user-video pass yet.',
        'approval_precedence': 'Exact-hash approval receipts override historical pending-still notes. Static approval is not dynamic approval.',
        'files': FILES}
    (HERE / 'inputs_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'copied_files': len(FILES), 'input_bytes': sum(f['size_bytes'] for f in FILES),
        'protected_originals_hashes_verified': len(protected), 'new_B_source': False, 'cloud_executed': False}))


if __name__ == '__main__':
    main()
