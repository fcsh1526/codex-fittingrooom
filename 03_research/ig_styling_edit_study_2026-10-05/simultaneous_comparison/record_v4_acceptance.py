"""Record the user's acceptance of one exact research cut; no media/cloud mutation."""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPECTED = 'a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

receipt_path = HERE / 'M02_parallel_compare_review_v4_size_matched.json'
manifest_path = HERE / 'research_manifest.json'
receipt = read(receipt_path)
manifest = read(manifest_path)
assert sha(ROOT / receipt['output_path']) == receipt['output_sha256'] == EXPECTED
assert all(sha(ROOT / item['path']) == item['sha256'] for item in manifest['protected_first_wave'])
assert sha(ROOT / '10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4') == '3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989'

approval = {
    'decision': 'accepted_clean_picture_track',
    'user_reply': 'ok',
    'recorded_at_local': datetime.now(timezone(timedelta(hours=8))).isoformat(),
    'context': 'Direct reply to the complete six-second v4 size-corrected video preview, followed by continue.',
    'output_path': receipt['output_path'],
    'output_sha256': EXPECTED,
    'scope': 'This exact research picture cut, including the displayed size correction; no detailed rationale or full-watch self-report inferred.',
    'assistant_continuous_review_claimed': False,
    'account_wide_style_adoption': False,
    'first_wave_replacement_authorized': False,
    'cloud_upload_performed': False,
    'publication_performed': False,
    'audience_performance': None,
}
existing = HERE / 'user_approval_v4.json'
if existing.exists():
    approval = read(existing)
    assert approval['output_sha256'] == EXPECTED
else:
    write(existing, approval)
receipt.update(status='accepted_research_clean_picture_track', user_video_approval=approval,
               publishable=False, publication=False, cloud_upload=False)
manifest.update(status=receipt['status'], user_approval=approval,
                latest_user_feedback='ok', cloud_writes=False)
manifest['previous_size_feedback'] = '左右人物大小有點不一致'
manifest['updated_at_local'] = approval['recorded_at_local']
write(receipt_path, receipt)
write(manifest_path, manifest)
print(json.dumps({'status': receipt['status'], 'output_sha256': EXPECTED,
                  'protected_media_unchanged': True, 'cloud_writes': False}, ensure_ascii=False))
