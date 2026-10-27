"""Read actual input stream declarations without encoding or modifying media."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / '10_automation').is_dir())
sys.path.insert(0, str(ROOT / '10_automation/.video_dependencies'))
import imageio_ffmpeg
p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--out', required=True)
a = p.parse_args()
source = Path(a.source).resolve()
out = Path(a.out).resolve()
if not source.is_file() or not out.is_relative_to(HERE):
    raise ValueError('Require existing source and isolated local-trial output')
r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-i', str(source)], capture_output=True, text=True, encoding='utf-8', errors='replace')
streams = [s.strip() for s in r.stderr.splitlines() if 'Stream #' in s]
video = [s for s in streams if 'Video:' in s]
audio = [s for s in streams if 'Audio:' in s]
if not video:
    raise ValueError('No actual input video was detected')
info = {'source': str(source), 'audio_stream_count': len(audio), 'audio_stream_lines': audio, 'video_stream_lines': video, 'method': 'ffmpeg input metadata inspection; no output requested', 'source_modified': False}
with out.open('x', encoding='utf-8') as f:
    json.dump(info, f, ensure_ascii=False, indent=2)
print(json.dumps({'audio_stream_count':len(audio)}))
