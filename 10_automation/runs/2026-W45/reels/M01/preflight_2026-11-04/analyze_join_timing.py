"""Head-region appearance cue for choosing source timing, not semantic/physical QA."""
from pathlib import Path
import subprocess,json,sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
FF=ROOT/'openmontage/.local/bin/ffmpeg.exe'
def patches(path):
    r=subprocess.run([str(FF),'-v','error','-i',str(path),'-an','-vf','crop=180:210:260:100,format=gray','-f','rawvideo','-'],capture_output=True,check=True)
    return np.frombuffer(r.stdout,np.uint8).reshape(-1,210,180).astype(np.float32)
a=patches(HERE.parent/'L01_trial_01/source.mp4');b=patches(HERE.parent/'L02_trial_01/source.mp4')
weights=np.array([(i/18)*(1-i/18) for i in range(18)],np.float32)
scores=[]
for k in range(25):
    diff=np.mean(np.abs(a[126:144]-b[k:k+18]),axis=(1,2))
    scores.append({'B_start_frame':k,'B_start_seconds':k/24,'weighted_head_patch_MAD':float(np.sum(diff*weights)/sum(weights))})
scores.sort(key=lambda x:x['weighted_head_patch_MAD'])
out={'cue':'Unregistered head-region appearance differences over18frame overlap; lower can help source timing. Not face/identity/comfort or physical-motion certification.','A_outgoing_overlap_frames':[126,144],'original':next(x for x in scores if x['B_start_frame']==0),'best_five':scores[:5],'all_scores':scores}
(HERE/'join_timing_analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['original','best_five']},ensure_ascii=False))
