"""Compose one separate native-frame body-distance trial with an 18-frame dissolve."""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'10_automation').is_dir())
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
sys.path.insert(0,str(ROOT/'10_automation'))
import imageio_ffmpeg
from scan_reel_video import scan

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def selected_frames(path,count,expected):
    if sha(path)!=expected:
        raise ValueError('Source changed from the reviewed version')
    gen=imageio_ffmpeg.read_frames(str(path),pix_fmt='rgb24')
    meta=next(gen)
    if meta['fps']!=24 or tuple(meta['size'])!=(720,1280):
        raise ValueError('Source clock/dimensions need a new design decision')
    try:
        for index in range(count):
            yield Image.frombytes('RGB',(720,1280),next(gen))
    finally:
        gen.close()

def main():
    output=HERE/'M02_body_distance_review_v1.mp4'
    receipt=output.with_suffix('.json')
    if output.exists() or receipt.exists():
        raise FileExistsError('Keep all prior candidates')
    old_manifest=json.loads((ROOT/'03_research/ig_styling_edit_study_2026-10-05/orientation_study/research_manifest.json').read_text(encoding='utf-8-sig'))
    protected=[(ROOT/r['path'],r['sha256']) for r in old_manifest['protected_first_wave']]
    protected.extend([
        (ROOT/'03_research/ig_styling_edit_study_2026-10-05/orientation_study/M02_parallel_angle_review_v2.mp4','9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569'),
        (ROOT/'03_research/ig_styling_edit_study_2026-10-05/simultaneous_comparison/M02_parallel_compare_review_v4_size_matched.mp4','a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'),
        (ROOT/'10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4','3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989')])
    for path,expected in protected:
        if sha(path)!=expected:
            raise ValueError('Protected media already differs: '+str(path))
    A=HERE/'near_start_A_attempt_01/source.mp4'
    B=HERE/'grok_B_attempt_01/source.mp4'
    a_sha='be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea'
    b_sha='afa46cced85bf886029940f36b7bbbd0bf188b5ebe49d8ac5d7f5f278ea62e5b'
    a_count,b_count,overlap=72,144,18
    a=selected_frames(A,a_count,a_sha)
    b=selected_frames(B,b_count,b_sha)
    writer=imageio_ffmpeg.write_frames(str(output),(720,1280),fps=24,codec='libx264',pix_fmt_in='rgb24',pix_fmt_out='yuv420p',quality=None,macro_block_size=1,ffmpeg_log_level='error',output_params=['-crf','18','-preset','medium','-movflags','+faststart'])
    writer.send(None)
    mapping=[]
    try:
        for index in range(a_count-overlap):
            writer.send(next(a).tobytes())
            mapping.append({'output_frame':len(mapping),'A_native_frame':index,'B_native_frame':None,'B_alpha':0})
        for index in range(overlap):
            # Each input advances one native frame at the same original clock.
            alpha=(index+1)/overlap
            writer.send(Image.blend(next(a),next(b),alpha).tobytes())
            mapping.append({'output_frame':len(mapping),'A_native_frame':a_count-overlap+index,'B_native_frame':index,'B_alpha':alpha})
        for index in range(overlap,b_count):
            writer.send(next(b).tobytes())
            mapping.append({'output_frame':len(mapping),'A_native_frame':None,'B_native_frame':index,'B_alpha':1})
    finally:
        writer.close()
        a.close()
        b.close()
    expected_count=a_count+b_count-overlap
    decoded=scan(output)
    if decoded['decoded_frames']!=expected_count or decoded['metadata']['fps']!=24 or tuple(decoded['metadata']['size'])!=(720,1280):
        raise ValueError('Rendered clock/size/count mismatch')
    qa=HERE/'qa/output_v1'
    qa.mkdir()
    full_dir=qa/'full'
    full_dir.mkdir()
    keep=set(round(n*(expected_count-1)/24) for n in range(25))
    keep.update(range(50,77))
    reader=imageio_ffmpeg.read_frames(str(output),pix_fmt='rgb24')
    next(reader)
    samples=[]
    transition=[]
    for index,raw in enumerate(reader):
        if index not in keep:
            continue
        im=Image.frombytes('RGB',(720,1280),raw)
        im.save(full_dir/f'frame_{index:06d}.png')
        if index in set(round(n*(expected_count-1)/24) for n in range(25)):
            samples.append((index,im))
        if 50<=index<=76:
            transition.append((index,im))
    def board(items,name,title,cols):
        tw,th=208,368
        canvas=Image.new('RGB',(cols*tw,30+((len(items)+cols-1)//cols)*(th+25)),'#f5f3ef')
        draw=ImageDraw.Draw(canvas)
        draw.text((5,7),title,fill='black')
        for slot,(index,im) in enumerate(items):
            im=im.copy()
            im.thumbnail((tw-8,th-6),Image.Resampling.LANCZOS)
            x,y=(slot%cols)*tw,30+(slot//cols)*(th+25)
            draw.text((x+4,y+4),f'f{index} / {index/24:.3f}s',fill='black')
            canvas.paste(im,(x+(tw-im.width)//2,y+25+(th-im.height)//2))
        canvas.save(qa/name,quality=95)
    board(samples,'full_25_checkpoints.jpg','Distance-v1 sampled output; not continuous visual review',5)
    board(transition,'transition_all_27_frames.jpg','Distance-v1 transition boundary; all consecutive native output frames',5)
    for path,expected in protected:
        if sha(path)!=expected:
            raise ValueError('Protected media changed during composition')
    save(qa/'decode_scan.json',decoded)
    save(qa/'frame_mapping.json',mapping)
    info={'status':'research_candidate_pending_visual_review','date':'2026-10-06','model':'M02','look_ids':['2026-W37-001-L01','2026-W37-001-L02'],
          'output':output.relative_to(ROOT).as_posix(),'output_sha256':sha(output),'native_size':[720,1280],'fps':24,'frames':expected_count,'seconds':expected_count/24,
          'sources':[{'role':'A_near_to_full','path':A.relative_to(ROOT).as_posix(),'sha256':a_sha,'selected_native_frames_half_open':[0,a_count]},
                     {'role':'B_full_to_near','path':B.relative_to(ROOT).as_posix(),'sha256':b_sha,'selected_native_frames_half_open':[0,b_count]}],
          'transition':{'type':'linear_cross_dissolve','seconds':0.75,'frames':18,'output_frames_half_open':[54,72],'B_weight':'(overlap_index+1)/18'},
          'frame_mapping':'qa/output_v1/frame_mapping.json','framing_transform':'none; native full raster both inputs','retime_freeze_reverse_replay':False,'forced_action_synchronization':False,
          'text':'none','audio':'none; frame-only encode','technical_scan':'qa/output_v1/decode_scan.json','assistant_sampled_review':'pending','assistant_continuous_review':False,'user_approval':None,'publishable':False,
          'limitations':['A pure full-shoe read before dissolve is short (~0.5s, from about1.75 to2.25); overlap visibility must be judged.',
                         'Native head/waist/proportion differ at transition; no exact subject registration or natural-speed comfort claim.',
                         'Both clips perform more walking steps than nominal two-step prompt; source speed unchanged.'],
          'protected_media_hashes_matched':True,'protected_media':[{'path':p.relative_to(ROOT).as_posix(),'sha256':v} for p,v in protected],'cloud_write':False,'publication':False,'global_template_adopted':False,'audience_performance':None}
    save(receipt,info)
    print(json.dumps({'output':str(output),'sha256':info['output_sha256'],'seconds':info['seconds'],'frames':expected_count,'protected_media_hashes_matched':True},ensure_ascii=False))

if __name__=='__main__':
    main()
