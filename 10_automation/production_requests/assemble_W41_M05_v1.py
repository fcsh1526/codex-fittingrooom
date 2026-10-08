"""Compose a new exact eight-second candidate; preserve source motion and earlier batches."""
import hashlib
import importlib.util
import json
from pathlib import Path

root=Path(__file__).resolve().parents[2]
run=root/'10_automation/runs/2026-W41'
work=run/'reels/M05'
output=work/'review_v1'
if output.exists():
    raise FileExistsError('Preserve existing candidate; choose a new version before rendering again.')
helper=root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py'
spec=importlib.util.spec_from_file_location('w41_native_pair',helper)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
from PIL import Image

sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[work/'A_attempt_01/source.mp4',work/'B_attempt_01/source.mp4']
counts=[114,96]
before=[sha(p) for p in paths]
for p,end in zip(paths,counts):
    scan=module.full_decode(p)
    module.require_interval(0,end,scan['decoded_frames'],19)
output.mkdir(parents=True)
video=output/'2026-W41_M05_two_looks_soft_v1.mp4'
a=module.selected_frames(paths[0],0,counts[0])
b=module.selected_frames(paths[1],0,counts[1])
mapping=[]
def frames():
    for f in range(96):
        mapping.append(dict(output_frame=len(mapping),A_frame=f,B_frame=None,B_alpha=0))
        yield next(a)
    for f in range(18):
        alpha=(f+1)/18
        mapping.append(dict(output_frame=len(mapping),A_frame=96+f,B_frame=f,B_alpha=alpha))
        yield Image.blend(next(a),next(b),alpha)
    for f in range(18,96):
        mapping.append(dict(output_frame=len(mapping),A_frame=None,B_frame=f,B_alpha=1))
        yield next(b)
stream=frames()
try:
    module.encode_new(video,stream)
finally:
    stream.close();a.close();b.close()
decoded=module.full_decode(video)
assert decoded['decoded_frames']==192 and len(mapping)==192
assert before==[sha(p) for p in paths]
qa=output/'QA';qa.mkdir()
samples=module.extract_boards(video,qa,0,192,range(88,122))
(qa/'frame_mapping.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8')
receipt=dict(week='2026-W41',model='M05',look_ids=['2026-W41-001-L01','2026-W41-001-L02'],
    output_path=video.relative_to(root).as_posix(),sha256=sha(video),
    native_pixels=[720,1280],fps=24,frames=192,duration_seconds=8,
    sources=[dict(path=p.relative_to(root).as_posix(),sha256=s,selected_frames_half_open=[0,n]) for p,s,n in zip(paths,before,counts)],
    transition=dict(type='linear_cross_dissolve',frames=18,seconds=.75,output_frames_half_open=[96,114],start_seconds=4,end_seconds=4.75),
    source_speed='unchanged',framing_transform='none',freeze_reverse_replay=False,text='none',audio='none',
    interval_reason='A finishes its gesture before the overlap; B finishes its gesture with a short clean settle. Later idle time and additional foot rotation excluded.',
    technical_decode=decoded,samples=samples,
    source_sampled_visual_review='25 full-frame and 5 face samples for each source: no apparent identity/clothing/background instability; actual hand begins higher than specified waist.',
    combined_visual_QA='pending',continuous_playback_review=False,user_approval=None,
    status='candidate_pending_combined_visual_review',prior_batch_write=False)
(output/'composition_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path=run/'reels/production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
record=next(r for r in manifest['reels'] if r['model_profile_id']=='M05')
record.update(output_path=receipt['output_path'],status='video_candidate_combined_QA_and_user_review_pending')
record['generation'].update(settings=dict(mode='video',resolution='720p',duration=6,aspect='9:16',audio=False,saved_reference='Mira M05 v1 face'),
    prompt_version='motion_prompt_v1',trials=[dict(look_id=lid,attempt=1,source=s['path'],browser_receipt=str(Path(s['path']).with_name('browser_receipt.json'))) for lid,s in zip(receipt['look_ids'],receipt['sources'])])
record['qa'].update(status='source_sampling_checked_combined_pending',continuous_watch_done=False,user_approval=None)
record['music']['clean_master']=receipt['output_path']
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':receipt['output_path'],'duration':8,'frames':192,'transition':.75,'status':receipt['status']}))
