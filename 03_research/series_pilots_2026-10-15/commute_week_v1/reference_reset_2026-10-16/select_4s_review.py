import importlib.util,json
from pathlib import Path
root=Path.cwd();base=root/'03_research/series_pilots_2026-10-15/commute_week_v1/reference_reset_2026-10-16'
module=root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('mira_native',module); h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
source=base/'R01_source.mp4'
assert h.digest(source)=='4bf0bdb9f4d547827fd36001da3c359eadcd2b7a2c053761b454effdc0ee4981'
out=base/'R01_walk_past_4s_review_v2.mp4'
h.encode_new(out,h.selected_frames(source,48,144))
decoded=h.full_decode(out)
assert decoded['decoded_frames']==96
qa=base/'QA_selected_4s';qa.mkdir()
boards=h.extract_boards(out,qa,0,96)
receipt={'recorded_date':'2026-10-16','status':'sampled_QA_pending_user_review','source':str(source.relative_to(root)).replace(chr(92),'/'),'source_sha256':h.digest(source),'source_interval_frames_half_open':[48,144],'source_interval_seconds':[2,6],'preview':str(out.relative_to(root)).replace(chr(92),'/'),'preview_sha256':h.digest(out),'output_frames':96,'seconds':4.0,'pixels':[720,1280],'fps':24,'text':False,'audio':False,'internal_cuts':0,'dissolves':0,'retime':False,'crop':False,'scale':False,'trim_reason':'Remove repeated early centred walking; retain actual full-to-near rightward pass. Natural walking speed unchanged.','full_decode':decoded,'boards':boards,'assistant_continuous_playback':False,'user_approval':None,'generation_calls':1}
h.json_new(base/'selected_4s_edit_receipt.json',receipt)
print(json.dumps({'preview':receipt['preview'],'sha256':receipt['preview_sha256'],'frames':96,'seconds':4.0},ensure_ascii=False))

