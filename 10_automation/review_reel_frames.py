"""Extract reproducible QA checkpoints. This never assigns a QA pass."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent / '.video_dependencies'))
import imageio_ffmpeg

def extract(source, output, times=None):
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    reader = imageio_ffmpeg.read_frames(str(source))
    meta = next(reader)
    reader.close()
    duration = meta['duration']
    if times is None:
        times = [0, duration*.25, duration*.5, duration*.75, max(0,duration-1/meta['fps'])]
    if any(seconds < 0 or seconds >= duration for seconds in times):
        raise ValueError(f'Checkpoint times must be within 0 <= t < {duration:.3f}s')
    sheet = Image.new('RGB', (len(times)*288, 544), 'white')
    draw = ImageDraw.Draw(sheet)
    for index, seconds in enumerate(times):
        frame=output/f'checkpoint_{index}_{seconds:.3f}s.png'
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-ss',str(seconds),'-i',str(source),'-frames:v','1',str(frame)],check=True)
        with Image.open(frame) as image:
            image.thumbnail((288,512))
            sheet.paste(image,(index*288,24))
        draw.text((index*288+8,5),f'{seconds:.3f}s',fill='black')
    sheet.save(output/'checkpoints.jpg',quality=95)
    (output/'metadata.json').write_text(json.dumps(dict(source=str(source), metadata=meta, checkpoint_seconds=times,continuous_review='pending'),indent=2),encoding='utf-8')
    return output/'checkpoints.jpg'

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--times',type=float,nargs='+',help='Specific checkpoint seconds for a denser review')
    args=parser.parse_args()
    print(extract(args.source,args.output,args.times))
