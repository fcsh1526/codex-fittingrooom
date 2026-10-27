"""Extra sampled checks around the reported, potentially snapped F03 keyframe."""
import runpy
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
q = runpy.run_path(str(HERE / 'inspect_source.py'), run_name='qa_helpers_only')
source = HERE.parent / 'F03_pace_source.mp4'
expected = '6bdf5237c8e8b40772b91ddd76a3d99cf81c0f44f0aea6381a69a7eb21fc61c3'
assert q['sha'](source) == expected
indices = list(range(80, 109))
metadata, frames, count = q['decode'](source, set(indices))
anchor = q['Image'].open(q['RESET'] / 'source_audit/F03_f091.png').convert('RGB')
artifacts = []
for i in [88, 91, 96]:
    artifacts.append(q['save_new'](HERE / 'frames' / f'anchor_window_new_F03_f{i:06d}.png', frames[i]))
artifacts.append(q['board']([
    ('exact OLD F03 f091\nrequested guide image', anchor),
    ('new F03 f088\n3.666667s', frames[88]),
    ('new F03 f091\nrequested 3.791667s', frames[91]),
    ('new F03 f096\n4.000000s', frames[96]),
], 'anchor_window_88_91_96.jpg', 'Keyframe snapping unreported: samples do NOT prove an exact timestamp or hit', cols=4, width=300))
artifacts.append(q['board'](q['frame_items'](frames, indices, 'new F03'), 'anchor_window_f080_f108_every1_foot.jpg', 'Native f80..108 every-frame feet; QA crop only; no retiming', cols=5, width=230, crop=q['FOOT']))
assert q['sha'](source) == expected
q['save_new'](HERE / 'anchor_window_receipt.json', json.dumps({
    'source_sha256': expected,
    'source_frames': count,
    'requested_keyframe_seconds': 91 / 24,
    'actual_keyframe_timestamp': None,
    'ui_reported_potential_snapping': '1/3 second; no actual chosen timestamp reported',
    'precise_hit_claim': False,
    'dense_sample_half_open': [80, 109],
    'normal_speed_continuous_visual_review': False,
    'artifacts': artifacts,
}, ensure_ascii=False, indent=2))
print('ANCHOR_WINDOW_QA_CREATED')
