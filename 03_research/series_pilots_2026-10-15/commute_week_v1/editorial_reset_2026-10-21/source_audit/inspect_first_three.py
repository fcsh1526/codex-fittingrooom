from pathlib import Path
import importlib.util
import json

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
HELPER = ROOT / '03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec = importlib.util.spec_from_file_location('mira_native_source_audit', HELPER)
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
BRIDGE = ROOT / '03_research/series_pilots_2026-10-15/commute_week_v1/production_bridge_2026-10-19'
SOURCES = {
    'F01': (BRIDGE / 'F01/F01_source.mp4', '6a9bf3204aadad28dc710aa914592e26851a03e47209c5bd9b682286b184fa50', [0, 59, 60, 77]),
    'F02': (BRIDGE / 'F02/motion_retry_01/F02_source.mp4', 'cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0', [0, 17, 37, 90, 107, 127, 144]),
    'F03': (BRIDGE / 'F03/F03_source.mp4', '26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5', [1, 18, 90, 91, 107, 108, 127, 144]),
}
report = {'purpose': 'Read-only source trim feasibility; source frames copied without edits. No rendering or generation.', 'sources': {}, 'assistant_continuous_playback': False}
all_items = []
for name, (source, expected, keep) in SOURCES.items():
    native.verified_source(str(source), expected)
    frames = {}
    for index, image in enumerate(native.selected_frames(source, 0, 145)):
        if index in keep:
            target = OUT / f'{name}_f{index:03d}.png'
            native.image_new(target, image)
            frames[index] = image
    native.sheet(list(frames.items()), OUT / f'{name}_checkpoints.jpg', f'{name} native-source trim checkpoints (24fps)')
    report['sources'][name] = {
        'path': str(source), 'sha256': expected, 'verified_unchanged_after': native.digest(source) == expected,
        'frames_inspected': keep,
        'frame_hashes': {str(i): native.digest(OUT / f'{name}_f{i:03d}.png') for i in frames},
    }
native.json_new(OUT / 'source_audit_evidence.json', report)
print(json.dumps(report, ensure_ascii=False, indent=2))
