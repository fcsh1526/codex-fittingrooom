"""Four-shot two-look clean review using three 0.75s dissolves."""
import hashlib,json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(root/'10_automation'))
sys.path.insert(0,str(root/'10_automation/.video_dependencies'))
import imageio_ffmpeg
from scan_reel_video import scan
reels=root/'10_automation/runs/2026-W37/reels'
work=reels/'qa/M03_two_looks_soft_review_v1_01';work.mkdir(exist_ok=True)
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(a):subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y',*a],check=True)
base=root/'10_automation/runs/2026-W37/generated_images/2026-W37-005/looks/2026-W37-005-L02/reel'
specs=[
 ('B1','full_start_candidate_v2','B1_full_start_generation_v2.json','https://grok.com/imagine/post/b051813d-738d-4595-ab64-71ffe52aab8a?conversation=4ac374b2-aa1a-4eb9-a459-b946e109762e','Nine checkpoints inspected: near-frontal face and long hair retained; blue shirt dress, waist belt, calf hem, chocolate-brown bag and complete black flats visible. No obvious sampled cafe morph. Continuous playback remains pending.'),
 ('B2','detail_start_candidate_v1','B2_detail_generation_v1.json','https://grok.com/imagine/post/57c71868-a4bd-4f8f-9f92-234222bcd1b9?conversation=a54c2efd-8a25-43b5-a05e-dea8c41e669d','Nine checkpoints inspected: face remains excluded; blue short sleeves, belt knot and dark-brown bag persist. Small rotation later changes bag presentation. No obvious sampled wall/window/bench morph. Continuous playback remains pending.')]
trials=[]
for shot,suffix,gen_name,url,note in specs:
    src=reels/f'videos/M03_{shot}_L02_motion_v1_01.mp4'
    scan_result=scan(src);qa=reels/f'qa/M03_{shot}_L02_motion_v1_01';save(qa/'decode_scan.json',scan_result)
    still=base/f'2026-W37-005-L02_M03_{shot}_{suffix}.png'
    trial=dict(reel_id='2026-W37-M03-reel',look_id='2026-W37-005-L02',trial_id=f'M03_{shot}_L02_motion_v1_01',date='2026-10-01',status='decoded_sampled_review_complete_continuous_qa_pending',source_post_url=url,input_still=rel(still),input_role='single First frame; exact filename checkbox1 verified; Add last frame visible, no Last frame',identity_reference='No separate saved character attached. Approved B1 face is full-shot identity input; approved B2 is faceless detail.',prompt_path=rel(reels/f'prompts/M03_{shot}_L02_motion_v1.md'),ui_settings=dict(resolution='720p',duration='6s',audio='off; checkbox0 confirmed',model='unnamed in visible UI'),video=dict(output_path=rel(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest(),resolution=[720,1264],fps=24,duration_seconds=scan_result['decoded_seconds']),qa=dict(decode_scan=scan_result,sampled_review=note,continuous_watch_done=False,user_visual_approval=None,usable_seconds=None),time=dict(active_minutes=None,generation_wait_minutes=None),upload=dict(status='assistant_upload_success',method='filechooser registered, actual Upload media AX click, setFiles, selected exact filename observed'))
    save(reels/f'M03_{shot}_L02_motion_v1_01.json',trial)
    trials.append(dict(trial_id=trial['trial_id'],output_path=rel(src),source_url=url,qa='sampled_only_continuous_pending',record_path=rel(reels/f'M03_{shot}_L02_motion_v1_01.json')))
    p=base/gen_name;d=json.loads(p.read_text(encoding='utf-8-sig'));d.update(grok_submitted=True,motion_record_path=rel(reels/f'M03_{shot}_L02_motion_v1_01.json'));save(p,d)
    p=reels/f'prompts/M03_{shot}_L02_motion_v1.md';s=p.read_text(encoding='utf-8-sig');s=s.replace(s.splitlines()[0],'# Submitted 2026-10-01; approved single First frame, 720p / 6s / audio off');p.write_text(s,encoding='utf-8')

selection=[('A1','L01',18,72),('A2','L01',6,72),('B2','L02',6,78),('B1','L02',18,91)]
common='scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=24,settb=1/24'
inputs=[];filters=[];sources=[]
for i,(shot,look,start,end) in enumerate(selection):
    src=reels/f'videos/M03_{shot}_{look}_motion_v1_01.mp4';inputs+=['-i',str(src)]
    filters.append(f'[{i}:v]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,{common}[s{i}]')
    sources.append(dict(shot_id=shot,look_id=f'2026-W37-005-{look}',path=rel(src),start_frame=start,end_frame_exclusive=end))
filters+=['[s0][s1]xfade=transition=fade:duration=0.75:offset=1.5[x1]','[x1][s2]xfade=transition=fade:duration=0.75:offset=3.5[x2]','[x2][s3]xfade=transition=fade:duration=0.75:offset=5.75,format=yuv420p[v]']
out=reels/'videos/M03_two_looks_soft_review_v1_01.mp4'
run([*inputs,'-filter_complex',';'.join(filters),'-map','[v]','-an','-c:v','libx264','-crf','18','-r','24','-frames:v','210','-movflags','+faststart',str(out)])
decoded=scan(out);save(work/'decode_scan.json',decoded)
times=[0,.75,1.458333,1.875,2.25,2.75,3.458333,3.875,4.25,4.75,5.708333,6.125,6.5,7.25,8,209/24]
sheet=Image.new('RGB',(288*4,544*4),'white');draw=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    p=work/f'frame_{round(t*24):03d}.png';run(['-ss',str(t),'-i',str(out),'-frames:v','1',str(p)])
    x=i%4*288;y=i//4*544
    with Image.open(p) as im:
        im.thumbnail((288,512));sheet.paste(im,(x,y+24))
    draw.text((x+8,y+5),f'{t:.3f}s',fill='black')
sheet.save(work/'checkpoints.jpg',quality=95)
record=dict(reel_id='2026-W37-M03-reel',date='2026-10-01',status='two_look_candidate_pending_continuous_user_approval',output_path=rel(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),duration_seconds=decoded['decoded_seconds'],resolution=[720,1280],fps=24,text='none',audio='none',speed='source timing unchanged',sources=sources,transitions=[dict(start=s,end=s+.75,type='cross dissolve',duration_seconds=.75) for s in [1.5,3.5,5.75]],first_transition_basis='User accepted L01 0.75s junction as 更舒服; same first full-shot source interval retained. Additional two junctions are unapproved candidates.',aspect_handling='Uniform cover-scale and narrow center side crop to720x1280, no stretching or animated framing.',technical_scan=decoded,qa=dict(continuous_watch_done=False,user_approval=None,sampled_visual_review=None,open_issues=['Normal-speed comfort across all three dissolves.','Ghosting, bag position/scale and clothing readability during overlap.','Full two-look theme and sufficient viewing time.']))
save(reels/'M03_two_looks_soft_review_v1_01.json',record)
p=reels/'production_manifest.json';manifest=json.loads(p.read_text(encoding='utf-8-sig'));m=next(x for x in manifest['reels'] if x['model_profile_id']=='M03')
m['generation']['trials'].extend(x for x in trials if x['trial_id'] not in {y['trial_id'] for y in m['generation']['trials']})
m['status']='two_look_soft_candidate_pending_continuous_user_approval'
m['output_path']=rel(out);m['qa'].update(status='technical_sampled_complete_full_user_review_pending',continuous_watch_done=False,user_approval=None)
m['storyboard']=[dict(shot_id=shot,look_id=f'2026-W37-005-{look}',start=s,end=e,source_video=source['path'],framing='full_person' if shot.endswith('1') else 'faceless_bag_and_cloth_detail',status='motion_sampled_pending_full_review') for (shot,look,_,_),source,(s,e) in zip(selection,sources,[(0,2.25),(1.5,4.25),(3.5,6.5),(5.75,8.75)])]
m['delivered_video_text']='none';m['instagram_editor_text_note']=None
save(p,manifest);print(json.dumps(dict(output=rel(out),scan=decoded),ensure_ascii=False))
