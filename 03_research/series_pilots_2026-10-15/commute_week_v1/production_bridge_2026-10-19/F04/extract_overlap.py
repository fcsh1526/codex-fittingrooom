from pathlib import Path
import hashlib, importlib.util, json

root=Path.cwd()
folder=Path(__file__).resolve().parent
source=folder.parent/'F03/F03_source.mp4'
expected='26087d5c7f4fd7dd8153b9c0c5a70fcdeea0429c0e8def12dc672632a9b499d5'
if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
    raise ValueError('Require original F03, never failed pillar retry')
helper=root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('mira_f04_overlap',helper)
native=importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)
assets=[]
for i,im in enumerate(native.selected_frames(source,0,145)):
    if i not in (127,144):
        continue
    p=folder/f'F03_actual_frame_{i:06d}.png'
    native.image_new(p,im)
    assets.append({'path':str(p),'frame':i,'seconds':i/24,'size':list(im.size),'sha256':native.digest(p),'role':'overlap_start_edit_target' if i==127 else 'overlap_end_direction_reference_only'})
native.json_new(folder/'overlap_reference_receipt.json',{
    'record_date_local':'2026-10-20','source':str(source),'source_sha256':expected,
    'accepted_three_shot_sha256':'f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33',
    'outgoing_source_frames_half_open':[127,145],
    'accepted_composite_outgoing_frames_half_open':[313,331],
    'dissolve_frames':18,'fps':24,'seconds':0.75,
    'assets':assets,'generated_stills':False,'failed_retry_used':False
})
print(json.dumps(assets,ensure_ascii=False))
