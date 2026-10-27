"""Compose two actual videos with fixed proportional panels; no generated synchronization."""
import argparse, importlib.util, json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('native', ROOT/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
p=argparse.ArgumentParser();p.add_argument('config');args=p.parse_args()
cfg=json.loads((ROOT/args.config).read_text(encoding='utf-8'))
out=(ROOT/cfg['output_directory']).resolve()
week=(ROOT/'10_automation/runs/2026-W41').resolve()
if not out.is_relative_to(week) or out.exists(): raise ValueError('Require new W41 output directory')
sources=[n.verified_source(ROOT/x['path'],x['sha256']) for x in cfg['sources']]
scans=[n.full_decode(x) for x in sources]
for x,scan in zip(cfg['sources'],scans):
    n.require_interval(*x['frames_half_open'],scan['decoded_frames'])
    if x['sampled_visual_review']!='completed': raise ValueError('Actual sampled source review required')
counts=[x['frames_half_open'][1]-x['frames_half_open'][0] for x in cfg['sources']]
if counts[0]!=counts[1]:raise ValueError('Use equal actual source intervals; no freeze or retiming')
out.mkdir(parents=True)
streams=[n.selected_frames(path,*x['frames_half_open']) for path,x in zip(sources,cfg['sources'])]
mapping=[]
def composite():
    for i,frames in enumerate(zip(*streams)):
        canvas=Image.new('RGB',(720,1280),cfg['background'])
        for frame,x in zip(frames,cfg['sources']):
            roi=x['crop_xyxy']; size=x['panel_size']; pos=x['panel_position']
            if abs(size[0]/(roi[2]-roi[0])-size[1]/(roi[3]-roi[1]))>0.001:raise ValueError('No stretching')
            canvas.paste(frame.crop(roi).resize(tuple(size),Image.Resampling.LANCZOS),tuple(pos))
        mapping.append({'output_frame':i,'A_native_frame':cfg['sources'][0]['frames_half_open'][0]+i,'B_native_frame':cfg['sources'][1]['frames_half_open'][0]+i})
        yield canvas
video=out/'2026-W41_M04_two_looks_parallel_v1.mp4'
try:n.encode_new(video,composite())
finally:
    for stream in streams:stream.close()
scan=n.full_decode(video)
if scan['decoded_frames']!=counts[0]:raise ValueError('Frame count mismatch')
qa=out/'QA';qa.mkdir()
n.extract_boards(video,qa,0,counts[0])
face_indices=n.uniform(0,counts[0],5)
faces=Image.new('RGB',(5*300,2*270),'#f5f3ef');draw=ImageDraw.Draw(faces)
for i,frame in enumerate(n.selected_frames(video,0,counts[0])):
    if i==0:
        n.image_new(out/'first_frame.png',frame)
        n.image_new(out/'mobile_first_frame.png',frame.resize((360,640),Image.Resampling.LANCZOS))
    if i in face_indices:
        col=face_indices.index(i)
        for row,roi in enumerate([(50,180,315,440),(410,180,675,440)]):
            face=frame.crop(roi);face.thumbnail((290,240),Image.Resampling.LANCZOS)
            faces.paste(face,(col*300+(300-face.width)//2,row*270+25))
            draw.text((col*300+4,row*270+4),f'{"A" if row==0 else "B"} f{i}',fill='black')
n.image_new(qa/'both_faces_5_checkpoints.jpg',faces)
for path,x in zip(sources,cfg['sources']):n.verified_source(path,x['sha256'])
receipt=dict(model='M04',format='parallel_two_looks',output_path=video.relative_to(ROOT).as_posix(),sha256=n.digest(video),native_size=[720,1280],fps=24,frames=counts[0],duration_seconds=counts[0]/24,audio='none',text='none',sources=cfg['sources'],background=cfg['background'],native_speed=True,forced_synchronization=False,transition='none; simultaneous panels without shot changes',source_scans=scans,combined_sampled_visual_review='pending',continuous_playback_review=False,user_video_approval=None,status='candidate_pending_combined_QA_and_user_approval')
n.json_new(out/'composition_receipt.json',receipt);n.json_new(qa/'frame_mapping.json',mapping)
print(json.dumps(receipt,ensure_ascii=False))
