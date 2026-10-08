import argparse, hashlib, importlib.util, json
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('config')
args=parser.parse_args()
cfg=json.loads((root/args.config).read_text(encoding='utf-8'))
assert cfg['week']=='2026-W41' and cfg['model'] in ['M01','M02','M03','M04','M05']
work=root/f"10_automation/runs/2026-W41/reels/{cfg['model']}"
output=work/cfg['version']
if output.exists():
    raise FileExistsError('Preserve existing outputs; choose a new version.')
spec=importlib.util.spec_from_file_location('native_pair',root/'03_research/reel_planning_2026-10-07/front_opening_gesture/local_trial_2026-10-08/native_pair_tools.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[root/p for p in cfg['source_paths']] if 'source_paths' in cfg else [work/f'{s}_attempt_01/source.mp4' for s in ['A','B']]
for p in paths:
    if not p.resolve().is_relative_to(work.resolve()):
        raise ValueError('Composition sources must remain in this model weekly folder.')
intervals=[cfg['A_frames'],cfg['B_frames']]
before=[sha(p) for p in paths]
for p,(start,end) in zip(paths,intervals):
    scan=mod.full_decode(p)
    mod.require_interval(start,end,scan['decoded_frames'],19)
output.mkdir(parents=True)
video=output/cfg.get('output_filename',f"2026-W41_{cfg['model']}_two_looks_soft_v1.mp4")
streams=[mod.selected_frames(p,*interval) for p,interval in zip(paths,intervals)]
countA=intervals[0][1]-intervals[0][0]
countB=intervals[1][1]-intervals[1][0]
join=18; begin=countA-join;total=countA+countB-join
mapping=[]
def frames():
    for i in range(begin):
        mapping.append(dict(output_frame=len(mapping),A_frame=intervals[0][0]+i,B_frame=None,B_alpha=0))
        yield next(streams[0])
    for i in range(join):
        alpha=(i+1)/join
        mapping.append(dict(output_frame=len(mapping),A_frame=intervals[0][0]+begin+i,B_frame=intervals[1][0]+i,B_alpha=alpha))
        yield Image.blend(next(streams[0]),next(streams[1]),alpha)
    for i in range(join,countB):
        mapping.append(dict(output_frame=len(mapping),A_frame=None,B_frame=intervals[1][0]+i,B_alpha=1))
        yield next(streams[1])
stream=frames()
try:
    mod.encode_new(video,stream)
finally:
    stream.close()
    for s in streams:s.close()
decoded=mod.full_decode(video)
assert decoded['decoded_frames']==len(mapping)==total
assert before==[sha(p) for p in paths]
qa=output/'QA';qa.mkdir()
samples=mod.extract_boards(video,qa,0,total,range(begin-8,begin+join+8))
(qa/'frame_mapping.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8')
receipt=dict(week=cfg['week'],model=cfg['model'],look_ids=cfg['look_ids'],output_path=video.relative_to(root).as_posix(),sha256=sha(video),native_pixels=[720,1280],fps=24,frames=total,duration_seconds=total/24,sources=[dict(path=p.relative_to(root).as_posix(),sha256=h,selected_frames_half_open=interval) for p,h,interval in zip(paths,before,intervals)],transition=dict(type='linear_cross_dissolve',frames=join,seconds=.75,output_frames_half_open=[begin,countA]),source_speed='unchanged',framing_transform='none',freeze_reverse_replay=False,text='none',audio='none',interval_reason=cfg['interval_reason'],technical_decode=decoded,samples=samples,source_sampled_visual_review=cfg['source_sampled_visual_review'],combined_visual_QA='pending',continuous_playback_review=False,user_approval=None,status='candidate_pending_combined_visual_review',prior_batch_write=False)
(output/'composition_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path=root/'10_automation/runs/2026-W41/reels/production_manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
record=next(r for r in manifest['reels'] if r['model_profile_id']==cfg['model'])
record.update(output_path=receipt['output_path'],status='video_candidate_combined_QA_and_user_review_pending')
record['identity']['saved_reference_name']=cfg['saved_reference_name']
record['generation'].update(settings=dict(mode='video',resolution='720p',duration=6,aspect='9:16',audio=False,saved_reference=cfg['saved_reference_name']),prompt_version=cfg.get('prompt_version','motion_prompt_v1'),trials=[dict(look_id=lid,attempt=attempt,source=s['path'],browser_receipt=str(Path(s['path']).with_name('browser_receipt.json'))) for lid,attempt,s in zip(cfg['look_ids'],cfg.get('attempts',[1,1]),receipt['sources'])])
record['qa'].update(status='source_sampling_checked_combined_pending',continuous_watch_done=False,user_approval=None)
record['music']['clean_master']=receipt['output_path']
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(output=receipt['output_path'],seconds=total/24,frames=total,status=receipt['status'])))
