"""Inspect one exact cadence trial and create a native-rate diagnostic pair.

Run only after root provides the downloaded source's exact SHA-256. New files are
confined to this QA directory. This is not an Instagram film or dynamic pass.
"""
from pathlib import Path
import argparse,hashlib,json,math,re,subprocess,sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'CURRENT_STATUS.md').exists())
RESET=HERE.parent.parent.parent
SOURCE=HERE.parent/'cadence_source.mp4'
BASELINE=RESET/'F04_motion_01/F04_source.mp4'
BASELINE_SHA='e32ee2f282b80dec8b8666d6755c9d2e77e5def6850bc53c89b5333927cd2208'
FPS=24
SIZE=(720,1280)
PAIR_SIZE=(720,640)
COUNT=144
sys.path.insert(0,str(ROOT/'10_automation/.video_dependencies'))
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageDraw

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def decode(path):
    reader=imageio_ffmpeg.read_frames(str(path),pix_fmt='rgb24',output_params=['-vsync','0'])
    meta=next(reader)
    width,height=meta['size']
    frames=[Image.frombytes('RGB',(width,height),b) for b in reader]
    return meta,frames

def sheet(frames,fps,indices,name,crop=None):
    width,height=frames[0].size
    cw,ch=(crop[2]-crop[0],crop[3]-crop[1]) if crop else (width,height)
    tw=230;th=round(ch*tw/cw);rowh=th+28
    canvas=Image.new('RGB',(5*tw,math.ceil(len(indices)/5)*rowh),'#efefef')
    draw=ImageDraw.Draw(canvas)
    for k,i in enumerate(indices):
        frame=frames[i].crop(crop) if crop else frames[i]
        x=k%5*tw;y=k//5*rowh
        canvas.paste(frame.resize((tw,th),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+4,y+th+5),f'f{i:03d} / {i/fps:.3f}s',fill='black')
    path=HERE/name
    if path.exists():raise FileExistsError(path)
    canvas.save(path,quality=97)
    return {'path':str(path),'indices':indices,'crop_xyxy':list(crop) if crop else None,
            'diagnostic_still_only':True,'video_cropped':False}

def composed(a,b):
    # Both equal 0.5 scales: no crop, distortion, temporal change, labels or bars.
    out=Image.new('RGB',PAIR_SIZE)
    out.paste(a.resize((360,640),Image.Resampling.LANCZOS),(0,0))
    out.paste(b.resize((360,640),Image.Resampling.LANCZOS),(360,0))
    return out

def stream_info(ff,path):
    result=subprocess.run([ff,'-hide_banner','-i',str(path)],capture_output=True)
    return result.stderr.decode('utf-8',errors='replace')

def bitstream_sha(ff,path):
    result=subprocess.run([ff,'-hide_banner','-loglevel','error','-i',str(path),'-map','0:v:0',
        '-c:v','copy','-bsf:v','h264_mp4toannexb','-f','h264','pipe:1'],capture_output=True)
    if result.returncode:raise RuntimeError(result.stderr.decode('utf-8',errors='replace'))
    return hashlib.sha256(result.stdout).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-sha',required=True)
    args=parser.parse_args()
    expected=args.source_sha.lower()
    if not re.fullmatch('[0-9a-f]{64}',expected):raise ValueError('Exact SHA-256 required')
    if not SOURCE.exists():raise FileNotFoundError(SOURCE)
    if sha(SOURCE)!=expected:raise ValueError('Downloaded source hash is not root-approved exact source')
    if sha(BASELINE)!=BASELINE_SHA:raise ValueError('Original F04 hash mismatch')
    receipt_path=HERE/'inspection_and_comparison_receipt.json'
    pair_path=HERE/'original_left_trial_right_native_6s.mp4'
    silent_path=HERE/'cadence_silent_streamcopy.mp4'
    planned=[receipt_path,pair_path,silent_path,HERE/'new_feet_every3.jpg',HERE/'new_whole_every6.jpg',
        HERE/'new_checkpoints25.jpg',HERE/'original_feet_every3.jpg',HERE/'original_whole_every6.jpg',
        HERE/'original_checkpoints25.jpg',HERE/'comparison_checkpoints25.jpg',
        HERE/'source_ffmpeg_info.txt',HERE/'comparison_ffmpeg_info.txt',HERE/'silent_remux_log.txt']
    if any(p.exists() for p in planned):raise FileExistsError('QA already exists; preserve and version explicitly')
    protected={str(SOURCE):expected,str(BASELINE):BASELINE_SHA}
    source_meta,source_frames=decode(SOURCE)
    base_meta,base_frames=decode(BASELINE)
    for label,meta,frames in [('trial',source_meta,source_frames),('original',base_meta,base_frames)]:
        if tuple(meta['size'])!=SIZE or abs(meta['fps']-FPS)>1e-8 or len(frames)<COUNT:
            raise ValueError(f'{label} must be native 720x1280,24fps,at least144 frames')
    outputs={}
    for label,meta,frames in [('new',source_meta,source_frames),('original',base_meta,base_frames)]:
        feet=list(range(0,len(frames),3));whole=list(range(0,len(frames),6))
        if whole[-1]!=len(frames)-1:whole.append(len(frames)-1)
        points=[round(k*(len(frames)-1)/24) for k in range(25)]
        outputs[label]={'feet':sheet(frames,FPS,feet,f'{label}_feet_every3.jpg',(0,740,720,1280)),
            'whole':sheet(frames,FPS,whole,f'{label}_whole_every6.jpg'),
            'checkpoints25':sheet(frames,FPS,points,f'{label}_checkpoints25.jpg')}
    writer=imageio_ffmpeg.write_frames(str(pair_path),PAIR_SIZE,pix_fmt_in='rgb24',pix_fmt_out='yuv420p',
        fps=FPS,codec='libx264',quality=None,macro_block_size=1,
        output_params=['-crf','18','-preset','medium','-an','-movflags','+faststart'])
    writer.send(None)
    try:
        for i in range(COUNT):writer.send(np.asarray(composed(base_frames[i],source_frames[i])))
    finally:writer.close()
    pair_meta,pair_frames=decode(pair_path)
    if tuple(pair_meta['size'])!=PAIR_SIZE or abs(pair_meta['fps']-FPS)>1e-8 or len(pair_frames)!=COUNT:
        raise ValueError('Diagnostic pair frame count, fps or raster mismatch')
    if pair_meta.get('audio_codec'):raise ValueError('Diagnostic pair must be silent')
    errors=[];psnrs=[]
    for i,frame in enumerate(pair_frames):
        expected_frame=np.asarray(composed(base_frames[i],source_frames[i]),dtype=np.int16)
        difference=expected_frame-np.asarray(frame,dtype=np.int16)
        errors.append(float(np.abs(difference).mean()))
        mse=float(np.square(difference.astype(np.float32)).mean())
        psnrs.append(100.0 if mse==0 else 10*math.log10(255*255/mse))
    tolerance=max(errors)<=3.5 and min(psnrs)>=32
    if not tolerance:raise ValueError('Pair encoding exceeds established diagnostic fidelity tolerance')
    pair_points=[round(k*(COUNT-1)/24) for k in range(25)]
    outputs['comparison_checkpoints25']=sheet(pair_frames,FPS,pair_points,'comparison_checkpoints25.jpg')
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    remux=subprocess.run([ff,'-hide_banner','-n','-i',str(SOURCE),'-map','0:v:0','-an','-c:v','copy',
        '-movflags','+faststart',str(silent_path)],capture_output=True)
    (HERE/'silent_remux_log.txt').write_text(remux.stderr.decode('utf-8',errors='replace'),encoding='utf-8')
    if remux.returncode:raise RuntimeError('Stream-copy silent source failed')
    original_bit=bitstream_sha(ff,SOURCE);silent_bit=bitstream_sha(ff,silent_path)
    if original_bit!=silent_bit:raise ValueError('Silent remux video bitstream changed')
    (HERE/'source_ffmpeg_info.txt').write_text(stream_info(ff,SOURCE),encoding='utf-8')
    (HERE/'comparison_ffmpeg_info.txt').write_text(stream_info(ff,pair_path),encoding='utf-8')
    if protected!={str(SOURCE):sha(SOURCE),str(BASELINE):sha(BASELINE)}:raise ValueError('Protected input changed')
    record={'purpose':'Research-only native-rate diagnostic comparison, not Instagram delivery or a gait pass',
        'source':{'path':str(SOURCE),'sha256':expected,'bytes':SOURCE.stat().st_size,
            'metadata':source_meta,'fully_decoded':True,'decoded_frames':len(source_frames),
            'frame_derived_duration_seconds':len(source_frames)/FPS,'full_source_preserved':True},
        'baseline':{'path':str(BASELINE),'sha256':BASELINE_SHA,'fully_decoded':True,
            'decoded_frames':len(base_frames),'metadata':base_meta},'diagnostic_images':outputs,
        'comparison':{'path':str(pair_path),'sha256':sha(pair_path),'bytes':pair_path.stat().st_size,
            'left':'Original F04 native[0,144)','right':'New trial native[0,144)',
            'per_panel_dimensions':[360,640],'uniform_scale':0.5,'output_dimensions':list(PAIR_SIZE),
            'metadata':pair_meta,'decoded_frames':len(pair_frames),'frame_derived_duration_seconds':COUNT/FPS,
            'every_frame_compared_to_expected_pair':COUNT,'mean_frame_MAE':sum(errors)/COUNT,
            'worst_frame_MAE':max(errors),'minimum_frame_PSNR_dB':min(psnrs),
            'codec_tolerance':{'worst_frame_MAE_max':3.5,'minimum_PSNR_dB_min':32},
            'within_codec_tolerance':tolerance,'silent':True,'text_or_labels_burned_in':False,
            'crop':False,'freeze':False,'duplicate_or_looped_frames':False,'retime':False,
            'transitions':False,'native_temporal_mapping':'outputi maps originali and triali at24fps'},
        'silent_source_copy':{'path':str(silent_path),'sha256':sha(silent_path),
            'source_video_h264_annexb_sha256':original_bit,'silent_video_h264_annexb_sha256':silent_bit,
            'identical_video_bitstream':True,'stream_copy_only':True,'full_video_stream_preserved':True},
        'protected_sources_unchanged':True,'continuous_visual_playback_performed':False,
        'gait_target_met':None,'dynamic_visual_QA_pass':None,'user_approval':None,
        'IG_publish_or_external_write':False}
    receipt_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_sha256':expected,'decoded_source_frames':len(source_frames),
        'comparison':record['comparison'],'protected_sources_unchanged':True},ensure_ascii=False))

if __name__=='__main__':main()
