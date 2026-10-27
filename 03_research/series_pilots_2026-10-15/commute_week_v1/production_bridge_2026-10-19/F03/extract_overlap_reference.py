from pathlib import Path
import importlib.util, hashlib, json
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent
source=HERE.parent/'F02/motion_retry_01/F02_source.mp4'
expected='cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0'
if hashlib.sha256(source.read_bytes()).hexdigest()!=expected: raise ValueError('F02 source differs')
spec=importlib.util.spec_from_file_location('mira_f03_overlap',ROOT/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
outputs=[]
for index in [127,144]:
    out=HERE/f'F02_actual_frame_{index:06d}.png'
    h.image_new(out,next(h.selected_frames(source,index,index+1)))
    outputs.append({'file':out.name,'source_frame':index,'source_seconds':index/24,'pixels':[720,1280],'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
h.json_new(HERE/'overlap_reference_receipt.json',{'recorded_date':'2026-10-19','source':str(source),'source_sha256':expected,'overlap_source_frames_half_open':[127,145],'overlap_seconds':0.75,'outputs':outputs,'frame127_role':'exact outgoing overlap-start edit target','frame144_role':'outgoing overlap-end direction reference, not F03 first frame','new_generative_images':False})
print(json.dumps(outputs,indent=2))
