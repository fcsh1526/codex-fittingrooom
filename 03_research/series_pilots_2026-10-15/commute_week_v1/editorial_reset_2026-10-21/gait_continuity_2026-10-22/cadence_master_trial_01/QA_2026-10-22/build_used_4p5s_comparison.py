"""Primary diagnostic: compare only original F04's actual film-used108 frames."""
from pathlib import Path
import hashlib,importlib.util,json,math,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cadence_qa',HERE/'inspect_and_compare.py')
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
EXPECTED='9707b42d230466ef2c2088a926ec45745d546d717c0fa9756d1b8e52ac0ab21d'
assert qa.sha(qa.SOURCE)==EXPECTED and qa.sha(qa.BASELINE)==qa.BASELINE_SHA
path=HERE/'original_used_left_trial_right_native_4p5s.mp4'
receipt_path=HERE/'used_4p5s_comparison_receipt.json'
assert not path.exists() and not receipt_path.exists()
source_meta,source=qa.decode(qa.SOURCE);old_meta,old=qa.decode(qa.BASELINE)
assert source_meta['fps']==24 and old_meta['fps']==24
assert tuple(source_meta['size'])==qa.SIZE and tuple(old_meta['size'])==qa.SIZE
assert len(source)>=108 and len(old)>=108
writer=qa.imageio_ffmpeg.write_frames(str(path),qa.PAIR_SIZE,pix_fmt_in='rgb24',pix_fmt_out='yuv420p',
    fps=24,codec='libx264',quality=None,macro_block_size=1,
    output_params=['-crf','18','-preset','medium','-an','-movflags','+faststart'])
writer.send(None)
try:
    for i in range(108):writer.send(qa.np.asarray(qa.composed(old[i],source[i])))
finally:writer.close()
meta,decoded=qa.decode(path)
assert len(decoded)==108 and meta['fps']==24 and tuple(meta['size'])==qa.PAIR_SIZE and not meta.get('audio_codec')
errors=[];psnrs=[]
for i,frame in enumerate(decoded):
    delta=qa.np.asarray(qa.composed(old[i],source[i]),dtype=qa.np.int16)-qa.np.asarray(frame,dtype=qa.np.int16)
    errors.append(float(qa.np.abs(delta).mean()));mse=float(qa.np.square(delta.astype(qa.np.float32)).mean())
    psnrs.append(100.0 if mse==0 else 10*math.log10(255*255/mse))
assert max(errors)<=3.5 and min(psnrs)>=32
assert qa.sha(qa.SOURCE)==EXPECTED and qa.sha(qa.BASELINE)==qa.BASELINE_SHA
record={'purpose':'Primary current-film-used range diagnostic; not IG delivery or gait pass',
    'path':str(path),'sha256':qa.sha(path),'bytes':path.stat().st_size,'metadata':meta,
    'decoded_frames':len(decoded),'frame_derived_duration_seconds':4.5,
    'source_sha256':EXPECTED,'baseline_sha256':qa.BASELINE_SHA,
    'left':'Original F04 native[0,108), exact range used in21.29sfilm',
    'right':'New trial native[0,108)','native_temporal_mapping':'outputi maps originali/triali at24fps',
    'each_panel':[360,640],'uniform_scale':0.5,'output_dimensions':[720,640],
    'every_frame_compared':108,'mean_frame_MAE':sum(errors)/108,'worst_frame_MAE':max(errors),
    'minimum_frame_PSNR_dB':min(psnrs),'codec_tolerance':{'worst_frame_MAE_max':3.5,'minimum_PSNR_dB_min':32},
    'within_codec_tolerance':True,'silent':True,'text':False,'crop':False,'retime':False,
    'freeze':False,'duplicate_or_looped_frames':False,'transitions':False,
    'new_full_source_frames_preserved':len(source),'baseline_full_source_frames_preserved':len(old),
    'protected_sources_unchanged':True,'previous_6s_diagnostic_preserved':True,
    'previous_6s_diagnostic_internal_only_reason':'Original f108..143 not used in current film; not attribution evidence',
    'continuous_visual_playback_performed':False,'gait_target_met':None,'dynamic_visual_QA_pass':None}
receipt_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
