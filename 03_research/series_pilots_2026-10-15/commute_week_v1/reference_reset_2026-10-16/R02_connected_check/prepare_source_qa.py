import importlib.util,json,hashlib
from pathlib import Path
root=Path.cwd();base=root/'03_research/series_pilots_2026-10-15/commute_week_v1/reference_reset_2026-10-16/R02_connected_check'
source=base/'R02_source.mp4'
sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha=='a6ed7789501ea80753bd1819ffd37c2efa3576d3907fccc86c89f92e7a1482db'
module=root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('mira_source_qa',module);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
scan=json.loads((base/'R02_technical_scan.json').read_text(encoding='utf-8-sig'))
scan['source_sha256']=sha
(base/'R02_technical_scan.json').write_text(json.dumps(scan,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
qa=base/'QA_source';qa.mkdir()
boards=h.extract_boards(source,qa,0,scan['decoded_frames'])
h.json_new(qa/'inspection_manifest.json',boards)
print(json.dumps({'sha256':sha,'boards':'QA_source/full_25_checkpoints.jpg','frames':scan['decoded_frames']}))

