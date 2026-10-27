from pathlib import Path
import importlib.util, json, sys
from datetime import datetime, timezone

folder = Path(__file__).resolve().parent
root = Path.cwd()
helper = root / '03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec = importlib.util.spec_from_file_location('mira_native_source_tools', helper)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
pair_spec = importlib.util.spec_from_file_location('mira_pair_tools', folder.parent / 'F02/build_first_pair_review.py')
pair = importlib.util.module_from_spec(pair_spec)
pair_spec.loader.exec_module(pair)
source = folder / 'F03_source.mp4'
source_hash = native.digest(source)
scan = native.full_decode(source)
inventory = pair.stream_inventory(source)
out = folder / 'QA_source'
out.mkdir()
samples = native.extract_boards(source, out, 0, scan['decoded_frames'])
gait_indices = sorted(set(range(0,25,3)) | set(range(60,85,3)) | set(range(120,145,3)))
items = []
for index, frame in enumerate(native.selected_frames(source, 0, scan['decoded_frames'])):
    if index in gait_indices:
        target = out / 'frames' / f'frame_{index:06d}.png'
        if not target.exists():
            native.image_new(target, frame)
        # Inspection-only foot/ground window, never used in the video.
        items.append((index, frame.crop((80, 820, 650, 1230))))
native.sheet(items, out / 'gait_early_mid_late_windows.jpg', 'QA-only foot/ground windows: 0.125s intervals in early/mid/late seconds')
if native.digest(source) != source_hash:
    raise ValueError('Source changed during inspection')
receipt = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'source': str(source), 'source_sha256': source_hash, 'bytes': source.stat().st_size,
    'full_decode': scan, 'stream_inventory': inventory,
    'sample_extraction': samples,
    'gait_window_native_xyxy': [80,820,650,1230], 'gait_indices': gait_indices,
    'gait_windows_inspection_only': True,
    'visual_qa_pass': None, 'assistant_continuous_visual_playback': False,
    'user_video_approval': None, 'publishable': False,
    'requested_settings_are_not_actual_settings': True
}
native.json_new(folder / 'technical_scan.json', receipt)
print(json.dumps({'sha256':source_hash, 'bytes':source.stat().st_size,'frames':scan['decoded_frames'],'seconds':scan['frame_count_over_fps_seconds'],'metadata':scan['metadata'],'streams':inventory},ensure_ascii=False))
