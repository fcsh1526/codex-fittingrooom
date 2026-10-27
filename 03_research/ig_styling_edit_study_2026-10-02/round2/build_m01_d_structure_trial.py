"""Render one review cut from existing full shots and two new shoe details."""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('mira_trial_helpers', BASE/'build_m03_order_trial.py')
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
OUT = BASE/'M01_D_structure_trial'
h.OUT = OUT
ROOT = h.ROOT
VIDEO = ROOT/'10_automation/runs/2026-W37/reels/videos'
SHOTS = {
    'A2': (OUT/'M01_A2_shoe_motion_v1.mp4',0,42,'2026-W37-004-L01'),
    'A1': (VIDEO/'M01_A_L01_fixed_full_v1_01.mp4',18,96,'2026-W37-004-L01'),
    'B1': (VIDEO/'M01_B_L02_fixed_full_v1_01.mp4',18,96,'2026-W37-004-L02'),
    'B2': (OUT/'M01_B2_shoe_motion_v2.mp4',6,84,'2026-W37-004-L02'),
}

def graph_for(shot,start,end):
    graph=h.selected_graph(start,end)
    if shot=='B1':
        graph=graph.replace('scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280',
                            'crop=642:1140:39:20,scale=720:1280')
    return graph

def prepare():
    records=[]
    for shot,(source,start,end,look) in SHOTS.items():
        decoded=h.scan(source)
        h.save(OUT/f'{shot}_full_scan.json',decoded)
        if decoded['metadata']['fps'] !=24 or decoded['decoded_frames'] <=end:
            raise ValueError(f'{shot}: fps or selected endpoint unsuitable')
        selected=OUT/f'{shot}_selected.mp4'
        h.run(['-i',str(source),'-vf',graph_for(shot,start,end)+',format=yuv420p',
               '-an','-c:v','libx264','-crf','18','-preset','medium','-r','24',
               '-movflags','+faststart',str(selected)])
        result=h.scan(selected)
        h.save(OUT/f'{shot}_selected_scan.json',result)
        if result['decoded_frames'] !=end-start or result['black_candidate_frames']:
            raise ValueError(f'{shot}: invalid selected decode')
        # Near-identical signals on a locked detail are inspected, not auto-passed.
        times=([i/8 for i in range(14)]+[41/24]) if shot=='A2' else [0,.65,1.3,1.95,2.6,77/24]
        board=h.checkpoints(selected,OUT/'qa'/shot,times,'selected_checkpoints.jpg')
        records.append(dict(shot_id=shot,look_id=look,path=h.rel(source),
            sha256=hashlib.sha256(source.read_bytes()).hexdigest(),start_frame=start,
            end_frame_exclusive=end,selected_frames=end-start,seconds=(end-start)/24,
            selected_preview=h.rel(selected),technical_scan=result,checkpoint_board=board,
            framing='crop=642:1140:39:20,scale=720:1280' if shot=='B1' else 'uniform cover scale and narrow center crop',
            sampled_visual_review='pending',assistant_continuous_review=False))
    h.save(OUT/'source_selection.json',dict(date='2026-10-02',sources=records,
           selection_note='A2 short clean head only; late lift/cross-foot artifacts excluded.'))
    print(json.dumps({'prepared':len(records),'scans':[dict(shot=x['shot_id'],frames=x['selected_frames'],near_identical_pairs=len(x['technical_scan']['near_identical_frame_pairs'])) for x in records]}))

def assemble():
    graphs=[];inputs=[]
    for i,(shot,(source,start,end,look)) in enumerate(SHOTS.items()):
        inputs+=['-i',str(source)]
        graphs.append(f'[{i}:v]{graph_for(shot,start,end)}[s{i}]')
    starts=[1,3.5,6]
    graphs+=['[s0][s1]xfade=transition=fade:duration=0.75:offset=1[x1]',
             '[x1][s2]xfade=transition=fade:duration=0.75:offset=3.5[x2]',
             '[x2][s3]xfade=transition=fade:duration=0.75:offset=6,format=yuv420p[v]']
    output=OUT/'M01_detail_full_full_detail_review_v1.mp4'
    h.run([*inputs,'-filter_complex',';'.join(graphs),'-map','[v]','-an','-c:v','libx264',
           '-crf','18','-preset','medium','-r','24','-frames:v','222','-movflags','+faststart',str(output)])
    decoded=h.scan(output)
    h.save(OUT/'output_scan.json',decoded)
    if decoded['decoded_frames'] !=222 or decoded['black_candidate_frames']:
        raise ValueError('Output length/decode unsuitable')
    times=sorted(set([0,.5,2.5,5,8,221/24]+[x+d for x in starts for d in [-1/24,0,.375,.75,.75+1/24]]))
    board=h.checkpoints(output,OUT/'qa'/'output',times,'output_checkpoints.jpg')
    sources=json.loads((OUT/'source_selection.json').read_text(encoding='utf-8'))
    h.save(OUT/'M01_detail_full_full_detail_review_v1.json',dict(date='2026-10-02',
        status='candidate_pending_user_visual_review',output_path=h.rel(output),
        sha256=hashlib.sha256(output.read_bytes()).hexdigest(),shot_order=list(SHOTS),
        sources=sources['sources'],actual_seconds=decoded['decoded_seconds'],
        resolution=[720,1280],fps=24,text='none',audio='none',source_speed='unchanged',
        transitions=[dict(start=x,end=x+.75,duration=.75,type='cross dissolve') for x in starts],
        technical_scan=decoded,checkpoint_board=board,assistant_sampled_review='pending',
        assistant_continuous_review=False,user_approval=None,publication_url=None,
        time=dict(active_minutes=None,generation_wait_minutes=None)))
    print(json.dumps(dict(output=str(output),frames=decoded['decoded_frames'],seconds=decoded['decoded_seconds'])))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['prepare','assemble'])
    args=parser.parse_args();before=time.monotonic()
    (prepare if args.stage=='prepare' else assemble)()
    print(f'Processing wall seconds: {time.monotonic()-before:.2f}')
