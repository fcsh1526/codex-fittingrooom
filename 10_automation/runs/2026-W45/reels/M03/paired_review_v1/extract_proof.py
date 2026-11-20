"""Extract a source-native exact frame with provenance; no synthesized still."""
import hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5]
src=HERE.parent/'L02_trial_01/source.mp4'
out=HERE/'L02_styling_proof_source_f144.png'
ff=ROOT/'openmontage/.local/bin/ffmpeg.exe'
subprocess.run([str(ff),'-v','error','-y','-i',str(src),'-vf','select=eq(n\\,144)','-frames:v','1',str(out)],check=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'source_path':src.relative_to(ROOT).as_posix(),'source_sha256':sha(src),'source_video_asset_id':'76ee1ce6-4fdb-44b1-bdaa-9c14d480f070','zero_based_source_frame':144,'fps':24,'source_seconds':6.0,'whole_film_frame':222,'whole_film_seconds':9.25,'path':out.relative_to(ROOT).as_posix(),'sha256':sha(out),'size':[720,1280],'crop':False,'rescale':False,'new_image_generation':False,'scope':'Medium styling-proof candidate showing lapel/neckline/waist/bag; not full-person, not separate Carousel A/B/C. Film user acceptance pending.','user_separate_still_approval':None}
(HERE/'proof_frame_lineage.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
