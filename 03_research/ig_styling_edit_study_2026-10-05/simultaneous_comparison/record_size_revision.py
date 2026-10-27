"""Update local review records for the user's size feedback; media remains immutable."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

new_path=OUT/'M02_parallel_compare_review_v4_size_matched.json'
new=read(new_path)
assert sha(ROOT/new['output_path'])==new['output_sha256']=='a383ea81ef1eb8e4b27993954aafe11376b80183bfc4634242370a7e0bdf9499'
new['assistant_sampled_visual_review']='Root and independent reviewer inspected5 combined checkpoints after constant scale/position correction, plus B critical tote position. Complete head/shoes/hem/hands/bags remain visible at inspected points. Most later head/sole positions close; opening residual recorded. No normal-speed continuous playback pass or exact per-frame size match claimed.'
new['scale_review_evidence']='qa/scale_review/manual_scale_estimates.json'
new['original_timing_verified']={'native_fps':24,'A_frame_range':[0,144],'B_frame_range':[0,144],'output_frames':144,'output_seconds':6,'source_hashes_unchanged':True,'no_freeze_reverse_repeat_retime':True}
write(new_path,new)
old_path=OUT/'M02_parallel_compare_review_v2.json'
old=read(old_path)
assert sha(ROOT/old['output_path'])==old['output_sha256']
old['status']='revision_requested_by_user_size_mismatch'
old['user_feedback']='左右人物大小有點不一致'
old['replacement_research_candidate']=new['output_path']
write(old_path,old)
manifest_path=OUT/'research_manifest.json'
manifest=read(manifest_path)
previous={'output':manifest['output'],'output_sha256':manifest['output_sha256'],'status':'revision_requested_by_user_size_mismatch','feedback':'左右人物大小有點不一致'}
manifest.setdefault('historical_candidates',[]).append(previous)
manifest.update(output=new['output_path'],output_sha256=new['output_sha256'],status=new['status'],user_approval=None,latest_user_feedback='左右人物大小有點不一致',size_revision=dict(new['correction']),cloud_writes=False)
assert all(sha(ROOT/item['path'])==item['sha256'] for item in manifest['protected_first_wave'])
assert sha(ROOT/'10_automation/runs/2026-W37/reels/M02_paired_D_v1/review/M02_paired_D_v1_review_v2_matched.mp4')=='3c077e1e05d31db0e92176ec49313ff051ddddfd8e3affb9b431ec88c6b27989'
write(manifest_path,manifest)
print(json.dumps({'status':new['status'],'output':new['output_path'],'five_originals_and_previous_paired_cut_unchanged':True,'new_video_user_approval':None},ensure_ascii=False))
