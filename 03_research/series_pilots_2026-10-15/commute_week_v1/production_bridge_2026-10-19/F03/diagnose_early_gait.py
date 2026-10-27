from pathlib import Path
import importlib.util
import json

folder = Path(__file__).resolve().parent
root = Path.cwd()
helper = root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('mira_gait_tools',helper)
native=importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
out=folder/'gait_diagnostic_2026-10-20'
out.mkdir()
sources=[
    ('F03_first_1p5s',folder/'F03_source.mp4',range(0,37,2),'26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5'),
    ('F02_last_overlap',folder.parent/'F02/motion_retry_01/F02_source.mp4',range(126,145,2),'cc23a3e22b5d51b2db42cc87b33371f73189b25b101cc37fff3a070dd68800b0'),
    ('composite_J23_and_after',folder/'three_shot_review_v1/F01_F02_F03_native_soft_review_v1.mp4',range(186,224,2),'9bb9bf741f307df29c98be414ba3597606877a01236af7dc43acb43321a4c03e')
]
records=[]
for label,path,indices,sha in sources:
    native.verified_source(path,sha)
    keep=set(indices)
    items=[]
    frames=out/label
    frames.mkdir()
    for index,im in enumerate(native.selected_frames(path,0,max(keep)+1)):
        if index in keep:
            native.image_new(frames/f'frame_{index:06d}.png',im)
            items.append((index,im.crop((60,800,660,1240))))
    native.sheet(items,out/f'{label}_foot_windows.jpg',label+' native foot/ground inspection; no retiming')
    records.append({'role':label,'source':str(path),'sha256':sha,'native_indices':list(indices)})
mapping=json.loads((folder/'three_shot_review_v1/QA_three_shot/frame_mapping.json').read_text(encoding='utf-8'))
receipt={
    'record_date_local':'2026-10-20',
    'user_quote':'第二鏡切第三鏡時，比第一鏡切第三鏡更無痕跡更順暢。但約8-9秒之間，人物有腳步飄移現象',
    'interpretation':'New F02-to-F03 join is positively received; exact8-9s gait needs correction. First-to-third comparison wording retained verbatim, not silently rewritten.',
    'status':'revision_requested_gait_8_to_9s_preserve_join_direction',
    'film_sha256':'9bb9bf741f307df29c98be414ba3597606877a01236af7dc43acb43321a4c03e',
    'report_interval_seconds_approx':[8,9],
    'join_seconds_half_open':[187/24,205/24],
    'composite_frames_around_report':[m for m in mapping if 192<=m['output_frame']<=216],
    'inspection_only_crop_xyxy':[60,800,660,1240],
    'sources':records,
    'cause_not_yet_established':True,
    'normal_speed_full_playback_self_report':None,
    'next':'Inspect F03 source f5..29 versus composite and accepted F02 tail before a targeted correction; no F04 expansion'
}
native.json_new(out/'user_feedback_and_mapping.json',receipt)
print(json.dumps({'status':receipt['status'],'boards':len(records),'source_F03_report_frames_approx':[5,29],'dissolve_end_seconds':205/24},ensure_ascii=False))
