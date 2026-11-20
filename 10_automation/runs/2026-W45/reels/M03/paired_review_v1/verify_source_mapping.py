"""Check native frame mapping outside the dissolve after encoding, not physical QA."""
from pathlib import Path
import subprocess,json,sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
def frames(path):
    r=subprocess.run([str(FF),'-v','error','-i',str(path),'-an','-vf','scale=180:320:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True,check=True)
    return np.frombuffer(r.stdout,np.uint8).reshape(-1,320,180,3).astype(np.float32)
a=frames(HERE.parent/'L01_trial_02/source.mp4');b=frames(HERE.parent/'L02_trial_01/source.mp4');v=frames(HERE/'M03_W45_two_looks_review_v1.mp4')
assert len(v)==252
da=np.mean(np.abs(v[:78]-a[0:78]),axis=(1,2,3))
db=np.mean(np.abs(v[96:]-b[18:174]),axis=(1,2,3))
assert max(da.max(),db.max())<2.5,'Output source mapping unexpectedly differs'
out={'unblended_output_frames_checked':234,'scale_for_comparison':[180,320],'A_source_frame_mapping':'output[0,78)=A[0,78)','B_source_frame_mapping':'output[96,252)=B[18,174)','A_mean_MAD':float(da.mean()),'A_max_MAD':float(da.max()),'B_mean_MAD':float(db.mean()),'B_max_MAD':float(db.max()),'outside_join_mapping_check':'passed within encoder-loss tolerance','does_not_certify':'Full-resolution identity, hand/foot physics, continuous visual QA or viewing comfort.'}
(HERE/'source_mapping_check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
