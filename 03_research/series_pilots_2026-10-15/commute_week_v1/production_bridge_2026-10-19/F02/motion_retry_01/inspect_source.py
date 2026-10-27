from pathlib import Path
import importlib.util, hashlib, json
ROOT=Path.cwd();HERE=Path(__file__).resolve().parent
source=HERE/'F02_source.mp4'
spec=importlib.util.spec_from_file_location('mira_f02_gait_source_qa',ROOT/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
scan=h.full_decode(source)
scan['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
scan['source_bytes']=source.stat().st_size
h.json_new(HERE/'technical_scan.json',scan)
qa=HERE/'QA_source';qa.mkdir()
boards=h.extract_boards(source,qa,0,scan['decoded_frames'])
h.json_new(qa/'inspection_manifest.json',boards)
print(json.dumps(scan,ensure_ascii=False,indent=2))
