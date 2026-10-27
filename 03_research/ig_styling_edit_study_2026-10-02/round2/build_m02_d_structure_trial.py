"""Review and render M02's four existing shots in detail/full/full/detail order."""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mira_trial_helpers',BASE/'build_m03_order_trial.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
OUT=BASE/'M02_D_structure_trial';ROOT=h.ROOT
VIDEO=ROOT/'10_automation/runs/2026-W37/reels/pilot_M02/videos'
SHOTS={
 'A2':('S02_comparison_v2_02.mp4',6,66,'2026-W37-001-L01','S02_comparison_v2_motion_02.json'),
 'A1':('S01_comparison_v2_01.mp4',6,84,'2026-W37-001-L01','S01_comparison_v2_motion_01.json'),
 'B1':('S04_comparison_v2_01.mp4',6,84,'2026-W37-001-L02','S04_comparison_v2_motion_01.json'),
 'B2':('S03_comparison_v2_02.mp4',6,54,'2026-W37-001-L02','S03_comparison_v2_motion_02.json'),
}

def prepare():
    records=[];OUT.mkdir(parents=True,exist_ok=True)
    for shot,(filename,start,end,look,generation) in SHOTS.items():
        source=VIDEO/filename;full=h.scan(source);h.save(OUT/f'{shot}_full_scan.json',full)
        if full['metadata']['fps']!=24 or full['decoded_frames']<=end:
            raise ValueError(f'{shot}: incompatible timing')
        selected=OUT/f'{shot}_selected.mp4'
        h.run(['-i',str(source),'-vf',h.selected_graph(start,end)+',format=yuv420p',
               '-an','-c:v','libx264','-crf','18','-preset','medium','-r','24',
               '-movflags','+faststart',str(selected)])
        decoded=h.scan(selected);h.save(OUT/f'{shot}_selected_scan.json',decoded)
        if decoded['decoded_frames']!=end-start or decoded['black_candidate_frames']:
            raise ValueError(f'{shot}: selected decode invalid')
        times=sorted(set([0,(end-start-1)/24]+[i*.25 for i in range(1,int((end-start)/6))]))
        board=h.checkpoints(selected,OUT/'qa'/shot,times,'selected_checkpoints.jpg')
        records.append(dict(shot_id=shot,look_id=look,path=h.rel(source),
            sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            generation_record=h.rel(VIDEO.parent/generation),start_frame=start,end_frame_exclusive=end,
            selected_frames=end-start,selected_seconds=(end-start)/24,
            technical_scan=decoded,checkpoint_board=board,checkpoint_count=len(times),
            framing='uniform cover scale, centered crop, no animated framing',
            assistant_sampled_visual_review='pending',assistant_continuous_review=False))
    h.save(OUT/'source_selection.json',dict(date='2026-10-02',sources=records,
         known_failure='B2/S03 late shoulder slip; only source0.25-2.25s used, early interval separately checked.'))
    print(json.dumps({'sources':[dict(shot=x['shot_id'],frames=x['selected_frames'],checkpoints=x['checkpoint_count'],near_identical_pairs=len(x['technical_scan']['near_identical_frame_pairs'])) for x in records]}))

def assemble():
    inputs=[];graphs=[]
    for i,(shot,(filename,start,end,look,generation)) in enumerate(SHOTS.items()):
        inputs+=['-i',str(VIDEO/filename)]
        graphs.append(f'[{i}:v]{h.selected_graph(start,end)}[s{i}]')
    starts=[1.75,4.25,6.75]
    graphs+=['[s0][s1]xfade=transition=fade:duration=0.75:offset=1.75[x1]',
             '[x1][s2]xfade=transition=fade:duration=0.75:offset=4.25[x2]',
             '[x2][s3]xfade=transition=fade:duration=0.75:offset=6.75,format=yuv420p[v]']
    output=OUT/'M02_detail_full_full_detail_review_v1.mp4'
    h.run([*inputs,'-filter_complex',';'.join(graphs),'-map','[v]','-an','-c:v','libx264',
           '-crf','18','-preset','medium','-r','24','-frames:v','210','-movflags','+faststart',str(output)])
    decoded=h.scan(output);h.save(OUT/'output_scan.json',decoded)
    if decoded['decoded_frames']!=210 or decoded['black_candidate_frames']:
        raise ValueError('Output duration/decode invalid')
    times=sorted(set([0,.875,3.375,5.875,8,209/24]+[x+d for x in starts for d in [-1/24,0,.375,.75,.75+1/24]]))
    board=h.checkpoints(output,OUT/'qa'/'output',times,'output_checkpoints.jpg')
    selection=json.loads((OUT/'source_selection.json').read_text(encoding='utf-8'))
    h.save(OUT/'M02_detail_full_full_detail_review_v1.json',dict(date='2026-10-02',
       status='candidate_pending_user_visual_review',output_path=h.rel(output),
       sha256=hashlib.sha256(output.read_bytes()).hexdigest(),sources=selection['sources'],shot_order=list(SHOTS),
       actual_seconds=decoded['decoded_seconds'],resolution=[720,1280],fps=24,text='none',audio='none',
       source_speed='unchanged',transitions=[dict(start=x,end=x+.75,duration=.75,type='cross dissolve') for x in starts],
       technical_scan=decoded,checkpoint_board=board,assistant_sampled_visual_review='pending',
       assistant_continuous_review=False,user_approval=None,publication_url=None,
       time=dict(active_minutes=None,new_generation_wait_minutes=0)))
    print(json.dumps(dict(output=str(output),frames=decoded['decoded_frames'],seconds=decoded['decoded_seconds'])))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('stage',choices=['prepare','assemble'])
    args=parser.parse_args();before=time.monotonic()
    (prepare if args.stage=='prepare' else assemble)()
    print(f'Processing wall seconds: {time.monotonic()-before:.2f}')
