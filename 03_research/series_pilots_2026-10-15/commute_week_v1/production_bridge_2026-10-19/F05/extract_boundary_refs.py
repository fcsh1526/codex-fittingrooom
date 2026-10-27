from pathlib import Path
import hashlib, json, sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / '10_automation' / '.video_dependencies').is_dir())
sys.path.insert(0, str(ROOT / '10_automation' / '.video_dependencies'))
import imageio_ffmpeg
from PIL import Image

HERE = Path(__file__).resolve().parent
source = HERE.parent / 'F04/close_tracking_proposal_2026-10-20/F04_close_motion_01/F04_close_source.mp4'
expected = '502951d7b908e24c7d5c21f60f9a2e0d369e9fc05f012cb9a1bb0fee16b73145'
actual = hashlib.sha256(source.read_bytes()).hexdigest()
assert actual == expected, 'Original F04 close source changed'
reader = imageio_ffmpeg.read_frames(str(source), pix_fmt='rgb24')
meta = next(reader)
receipt = {'date_client':'2026-10-21','source':str(source),'source_sha256':actual,'fps':meta['fps'],'dimensions':meta['size'],'outputs':[]}
for i, frame in enumerate(reader):
    if i in (127,144):
        out = HERE / f'F04_actual_f{i:03}.png'
        assert not out.exists(), 'Refusing reference overwrite'
        Image.frombytes('RGB',meta['size'],frame).save(out)
        receipt['outputs'].append({'frame':i,'seconds':i/meta['fps'],'path':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
receipt['decoded_frames'] = i + 1
receipt['role'] = 'frame127 is F05-first edit target for18frame overlap;144 is overlap-end reference only'
(HERE / 'boundary_reference_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=True))
