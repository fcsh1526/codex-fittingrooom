"""Record research completed and motion-source retrieval failures without inventing a cut."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

# Historical failure recorder must never overwrite a recovered/current state.
current_manifest = HERE / 'research_manifest.json'
if current_manifest.exists():
    current = json.loads(current_manifest.read_text(encoding='utf-8-sig'))
    if current.get('recovery_attempts') or current.get('output'):
        raise RuntimeError('Recovery/candidate already recorded; preserve current manifest. This recorder is historical.')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

prior = read(HERE.parent / 'simultaneous_comparison' / 'research_manifest.json')
assert all(sha(ROOT / item['path']) == item['sha256'] for item in prior['protected_first_wave'])
assert sha(ROOT / prior['output']) == prior['output_sha256'] == 'a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'
assert sha(ROOT / '10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4') == '3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989'
attempts = []
for name in ('grok_A_attempt_01', 'grok_B_attempt_01', 'grok_A_attempt_02'):
    folder = HERE / name
    issue = read(folder / 'retrieval_issue.json')
    settings = read(folder / 'settings.json')
    settings['status'] = issue['status']
    if (folder / 'submission.json').exists():
        settings['post_url'] = read(folder / 'submission.json')['post_url']
    write(folder / 'settings.json', settings)
    attempts.append(dict(folder=name, settings='settings.json', issue=issue,
                         source_downloaded=False, source_quality=None))
manifest = {
    'date': '2026-10-05',
    'recorded_at_local': datetime.now(timezone(timedelta(hours=8))).isoformat(),
    'model': 'M02', 'look_ids': prior['look_ids'],
    'status': 'reference_study_and_storyboard_complete_motion_sources_unavailable',
    'audience_problem': 'Compare open-shirt side drape, sleeve outline and dress silhouette in the same shallow viewing direction.',
    'source_assets': [a for a in prior['source_assets'] if a['role'].endswith('_full')],
    'identity_reference': {'ui_name':'Mira M02 v3', 'canonical_csv_status':'approved',
                           'face_file_exists':True, 'full_file_exists':True,
                           'actual_selection_screenshots':True},
    'new_stills_generated': 0,
    'reference_observation': {'url':'https://www.instagram.com/reel/Dd60yYTMtJ1/',
                              'evidence':'evidence/lydia_jackets/', 'samples':52,
                              'boards_inspected':4, 'muted':True,
                              'source_duration_seconds':37.707754,
                              'exact_cuts_or_audio_analysis':False,
                              'continuous_full_watch_claimed':False,
                              'independent_review':'evidence/lydia_jackets/source_visual_review.md'},
    'storyboard':'README.md', 'prompts':['prompt_A.txt','prompt_B.txt'],
    'send_clicks_observed':3, 'generation_progress_observed_attempts':2,
    'attempts':attempts, 'new_video_sources_retrieved':0,
    'output':None, 'output_sha256':None, 'usable_seconds':None,
    'dynamic_qa':None, 'user_video_approval':None,
    'active_minutes':None,
    'failure_cause':'unknown; initial post URLs redirected after navigation during generation, A retry stayed on the same page but did not produce a new result. No raw Bad Request or console error was observed.',
    'next_operational_gate':'Verify a submitted source progresses to an accessible generated result before further image/action variants; do not resend automatically past the source retry bound.',
    'B_retry_not_started_reason':'No retrieved A source after the single A retry; avoid another unusable paired source.',
    'protected_first_wave':prior['protected_first_wave'],
    'accepted_parallel_v4_unchanged':True, 'accepted_paired_11_25s_unchanged':True,
    'cloud_writes':False, 'publication':False, 'audience_metrics':None,
}
write(HERE / 'research_manifest.json', manifest)
print(json.dumps({'status':manifest['status'], 'retrieved_new_sources':0,
                  'protected_media_unchanged':True, 'cloud_writes':False}, ensure_ascii=False))
