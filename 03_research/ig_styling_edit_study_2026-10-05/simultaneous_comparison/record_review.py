"""Record sampled evidence and protected original hashes without changing media."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

v2 = read(OUT / 'M02_parallel_compare_review_v2.json')
expected = '1425a09a0476e821617253aa7881feee5bcbce06de0cc377e774482f5cedd812'
assert sha(ROOT / v2['output_path']) == expected == v2['output_sha256']
v2['status'] = 'research_candidate_pending_user_full_film_review'
v2['assistant_sampled_visual_review'] = 'Root reviewed5 full-source checkpoints per source and5 combined output checkpoints; independent A/B25 checkpoints with original-size boundary checks. No obvious sampled face/outfit/background jump in selected intervals; wider fixed window retains outfit boundaries at inspected points. More vertical margin and small panels remain a user comfort/readability question.'
v2['independent_source_reviews'] = [f'qa/{letter}_independent/visual_review.json' for letter in ('A','B')]
for i, source in enumerate(v2['sources']):
    source['sampled_qa'] = 'Root5 plus independent25 checkpoints reviewed; actual short steps, weight/size change and bag motion recorded; no continuous pass inferred.'
    source['continuous_qa'] = 'not_claimed'
write(OUT / 'M02_parallel_compare_review_v2.json', v2)
v1 = read(OUT / 'M02_parallel_compare_review_v1.json')
v1['status'] = 'rejected_boundary_safety_diagnostic'
v1['rejection_reason'] = 'B tote outer corner touches/slightly exceeds common445px-window right edge around1.75s; retained for history. v2 expands common window to470px.'
v1['publishable'] = False
write(OUT / 'M02_parallel_compare_review_v1.json',v1)
old = read(ROOT / '10_automation/runs/2026-W37/reels/google_drive_update_2026-10-02.json')
protected = []
for item in old['files']:
    path = ROOT / item['source_video_path']
    actual = sha(path)
    assert actual == item['local_sha256']
    protected.append(dict(model=item['model'],path=item['source_video_path'],sha256=actual,drive_id=item['video']['id'],matched=True))
paired = read(ROOT / '10_automation/runs/2026-W37/reels/M02_paired_D_v1/storyboard.json')
assets = []
for role, rel in paired['current_asset_candidates'].items():
    path = ROOT / rel
    assert path.is_file()
    assets.append(dict(role=role,path=rel,sha256=sha(path),approval_basis='Previously individually approved paired-scene stills; see M02_paired_D_v1 records. No new still generation or approval inferred.'))
write(OUT / 'research_manifest.json',dict(date='2026-10-05',updated_at_local=datetime.now().astimezone().isoformat(),model='M02',look_ids=['2026-W37-001-L01','2026-W37-001-L02'],audience_problem='Compare two thin-shirt/dress layering palettes and whole-outfit proportions in the same reading situation.',reference_url='https://www.instagram.com/__iamkubo__/reel/DdyQ56qRXGA/',reference_evidence='reference_live.json',source_assets=assets,output=v2['output_path'],output_sha256=expected,review='REVIEW.md',generation_attempts=2,retries=0,active_minutes=None,observed_wait_seconds_including_other_work=[166.22,75.5],status=v2['status'],user_approval=None,publication_url=None,audience_metrics=None,cloud_writes=False,protected_first_wave=protected,previous_accepted_paired_cut_unchanged=(sha(ROOT/'10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4')=='3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989')))
print(json.dumps({'research_status':v2['status'],'five_original_hashes_match':True,'output_hash':expected,'no_video_write':True},ensure_ascii=False))
