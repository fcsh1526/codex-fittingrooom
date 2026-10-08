"""Save decode, audio metadata and sampled visual inspection assets; never approve a film."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'10_automation'))
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from scan_reel_video import scan

p=argparse.ArgumentParser()
p.add_argument('source',type=Path)
p.add_argument('output',type=Path)
a=p.parse_args()
source=a.source.resolve(); output=a.output.resolve()
if not output.is_relative_to((root/'10_automation/runs/2026-W41').resolve()) or output.exists():
    raise ValueError('Require a new QA directory inside W41.')
output.mkdir(parents=True)
helper=root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('w41_native_inspection',helper)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
technical=scan(source)
module.require_native(technical['metadata'])
samples=module.extract_boards(source,output,0,technical['decoded_frames'])
probe=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-i',str(source)],capture_output=True,text=True,encoding='utf-8',errors='replace')
streams=[x.strip() for x in probe.stderr.splitlines() if 'Stream #' in x]
record=dict(source=source.relative_to(root).as_posix(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    technical=technical,samples=samples,audio_stream_count=sum('Audio:' in x for x in streams),
    stream_declarations=streams,assistant_static_dynamic_review='pending',
    continuous_playback_review=False,user_video_approval=None)
(output/'inspection.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'frames':technical['decoded_frames'],'size':technical['metadata']['size'],
    'fps':technical['metadata']['fps'],'audio_streams':record['audio_stream_count'],
    'black_frames':technical['black_candidate_frames'],'output':str(output)}))
