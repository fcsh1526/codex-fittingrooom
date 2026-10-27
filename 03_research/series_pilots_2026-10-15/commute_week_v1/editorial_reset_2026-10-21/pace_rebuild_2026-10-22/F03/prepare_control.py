from pathlib import Path
import hashlib, json, sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'10_automation/CANONICAL_WORKFLOW.md').is_file())
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from PIL import Image
BASE=ROOT/'03_research/series_pilots_2026-10-15/commute_week_v1'
SOURCE=BASE/'production_bridge_2026-10-19/F03/F03_source.mp4'
EXPECTED='26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5'
def sha(p):
    with p.open('rb') as s:return hashlib.file_digest(s,'sha256').hexdigest()
assert sha(SOURCE)==EXPECTED
out=HERE/'controls/F03_original_actual_frame_000091.png'
assert not out.exists()
out.parent.mkdir(parents=True,exist_ok=True)
r=imageio_ffmpeg.read_frames(str(SOURCE),pix_fmt='rgb24',output_params=['-vsync','0'])
m=next(r)
assert m['fps']==24 and tuple(m['size'])==(720,1280)
try:
    for i,raw in enumerate(r):
        if i==91:
            Image.frombytes('RGB',(720,1280),raw).save(out)
            break
finally:r.close()
assert out.is_file() and sha(SOURCE)==EXPECTED
receipt={
 'date':'2026-10-22',
 'type':'unmodified native video frame extraction; not AI image generation',
 'source':str(SOURCE),'source_sha256':EXPECTED,
 'native_frame_index_zero_based':91,'source_time_seconds':91/24,
 'output':str(out),'output_sha256':sha(out),'pixels':[720,1280],
 'crop_resize_retouch':False,
 'approval_lineage':'Original F03[1,109) occurs in previously accepted three/four-look research intervals; user latest explicitly retains camera design and authorizes F03 gait repair. No new photographic content or separately fabricated exact-still approval.',
 'role':'F03 interior framing anchor at91/24 seconds, corresponding to existing F04 first-frame derivation; not gait conditioning or guarantee of frame accuracy',
 'planned_selection':[1,109],
 'planned_generation':{'duration':'6','first':'existing approved F03 first a7a33bb7-39ff-472d-b27d-53e50fe48c58','keyframe':{'asset':'pending actual upload','timestamp_s':91/24},'last':None,'identity':['6236309c-2343-41e6-985c-994239ff744a','ac9ede4e-1715-4518-95b4-bda341a62061']},
 'risk':'Only keyframe composition is anchored. Newf91..108 motion and newf1..18 entry must be checked against both neighboring sources. No guarantee of exact conditioning, constant cadence, route reconstruction or zero slip.',
 'not_new_source_approval':True
}
(HERE/'controls/extraction_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
