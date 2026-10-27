"""Inspect one preserved source and make a stream-copy silent review only."""
from pathlib import Path
import importlib.util
import hashlib
import json
import subprocess

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
source = HERE / 'F01_source.mp4'
module = ROOT / '03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec = importlib.util.spec_from_file_location('mira_f01_qa', module)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
scan = h.full_decode(source)
scan['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
scan['source_bytes'] = source.stat().st_size
(HERE / 'F01_technical_scan.json').write_text(json.dumps(scan, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
qa = HERE / 'QA_source'
qa.mkdir()
boards = h.extract_boards(source, qa, 0, scan['decoded_frames'])
h.json_new(qa / 'inspection_manifest.json', boards)
preview = HERE / 'F01_silent_review_v1.mp4'
subprocess.run([h.imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error', '-n', '-i', str(source), '-map', '0:v:0', '-c:v', 'copy', '-an', '-movflags', '+faststart', str(preview)], check=True)
preview_scan = h.full_decode(preview)
receipt = {'source_sha256':scan['source_sha256'], 'preview_sha256':hashlib.sha256(preview.read_bytes()).hexdigest(), 'source_frames':scan['decoded_frames'], 'preview_frames':preview_scan['decoded_frames'], 'preview_seconds':preview_scan['frame_count_over_fps_seconds'], 'preview_metadata':preview_scan['metadata'], 'picture_stream_copy':True, 'audio_removed_in_preview_only':True, 'text_added':False, 'cuts':0, 'crop':False, 'retime':False, 'dynamic_visual_qa':'pending_review', 'continuous_playback_review':False, 'user_motion_approval':None}
(HERE / 'F01_silent_preview_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'source_scan':scan,'preview_receipt':receipt},ensure_ascii=False,indent=2))
