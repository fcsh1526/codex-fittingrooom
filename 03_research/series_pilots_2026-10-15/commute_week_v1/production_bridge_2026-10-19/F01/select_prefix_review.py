from pathlib import Path
import importlib.util, json, hashlib, subprocess
ROOT=Path.cwd()
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mira_prefix_qa',ROOT/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
source=HERE/'F01_source.mp4'
preview=HERE/'F01_prefix_3p25s_silent_review_v2.mp4'
subprocess.run([h.imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-n','-i',str(source),'-map','0:v:0','-frames:v','78','-c:v','libx264','-crf','18','-preset','medium','-an','-movflags','+faststart',str(preview)],check=True)
scan=h.full_decode(preview)
if scan['decoded_frames']!=78: raise ValueError(scan)
receipt={'source':'F01_source.mp4','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'preview':preview.name,'preview_sha256':hashlib.sha256(preview.read_bytes()).hexdigest(),'selected_source_frames_half_open':[0,78],'seconds':3.25,'decoded_frames':78,'fps':24,'pixels':[720,1280],'stream_copy':False,'reencoded_for_exact_frame_boundary':True,'retime':False,'crop':False,'freeze':False,'added_text':False,'audio':'removed in preview only','cuts_inside_selected_interval':0,'preserved_failed_v1':'Packet-copy v1 duration metadata3.25 but decoded80frames; not the review deliverable.','selection_reason':'Later newly revealed deep arched corridor is incompatible with approved short rectangular colonnade. This prefix is only a walk/camera-direction candidate; no end-to-end spatial or dynamic pass.','assistant_continuous_playback':False,'user_exact_prefix_motion_feedback':None,'whole_route_or_five_look_film_approved':False,'technical_scan':scan}
(HERE/'F01_prefix_selection_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
