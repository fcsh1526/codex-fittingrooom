import importlib.util,json,hashlib,subprocess
from pathlib import Path
root=Path.cwd(); base=root/'03_research/series_pilots_2026-10-15/commute_week_v1/reference_reset_2026-10-16'
module=root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('mira_native_tools',module); helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
scan=json.loads((base/'R01_technical_scan.json').read_text(encoding='utf-8-sig'))
qa=base/'QA';qa.mkdir()
boards=helper.extract_boards(base/'R01_source.mp4',qa,0,scan['decoded_frames'])
helper.json_new(qa/'inspection_manifest.json',boards)
ffmpeg=root/'10_automation/.video_dependencies/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
out=base/'R01_walk_past_silent_review_v1.mp4'
subprocess.run([str(ffmpeg),'-v','error','-n','-i',str(base/'R01_source.mp4'),'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',str(out)],check=True)
res={'source_sha256':helper.digest(base/'R01_source.mp4'),'preview':str(out.relative_to(root)).replace(chr(92),'/'),'preview_sha256':helper.digest(out),'transformation':'audio removed; video stream copied without trim/retime/crop/scale','source_frames':scan['decoded_frames'],'size':scan['metadata']['size'],'fps':scan['metadata']['fps'],'duration_frames_over_fps':scan['decoded_frames']/scan['metadata']['fps'],'assistant_continuous_playback':False,'user_film_approval':None}
helper.json_new(base/'preview_receipt.json',res);print(json.dumps(res,ensure_ascii=False))

