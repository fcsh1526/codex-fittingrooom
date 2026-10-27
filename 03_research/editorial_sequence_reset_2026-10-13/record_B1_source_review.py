from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parent
JOB=ROOT/'10_automation/runs/2026-W41/generated_images/2026-W41-004/looks/2026-W41-004-L02/reel/lunch_outing_v1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=BASE/'B1_motion_attempt_01/technical_receipt.json';d=read(p)
d.update(visual_review='sampled_source_candidate_whole_film_review_pending',review_method='All145 thumbnails,25 larger whole-frame samples,5 face samples and native frames36/72 viewed. No continuous normal-speed assistant playback.',actual_motion='Small head/gaze change toward image-left then return later; direction differs from requested image-right. Torso, crossed leg and resting hands mostly stationary. No sit-to-stand action.',identity_wardrobe_background='Recognizable M03, plain gray cotton tee, navy lapels/cuffs, cream trousers and black shoulder bag retained in reviewed frames. Resting hands remain simply supported. Window/bench/wall broadly stationary; no gross instant morph observed. Exact geometry/native contact every frame not certified.',motion_prompt_compliance='partial: opposite gaze direction',retained_interval_seconds=[0,3.75],retained_frames_end_exclusive=[0,90],interval_note='Contains small attention shift and readable seated layers; tails after3.75s excluded. Match comfort depends on full assembled film.',assistant_continuous_playback=False,user_film_approval=None)
save(p,d)
for p in [BASE/'B1_still_receipt.json',JOB/'B1_generation_receipt.json']:
 r=read(p);r.update(grok_uploaded=True,video_generated=True,confirmed_motion_result_count=1,motion_source=d['source'],motion_source_sha256=d['sha256'],motion_review='B1_motion_attempt_01/technical_receipt.json',user_film_approval=None);save(p,r)
print('B1 sampled review saved; retained0–3.75s. Opposite gaze direction explicit; whole-film acceptance pending.')
