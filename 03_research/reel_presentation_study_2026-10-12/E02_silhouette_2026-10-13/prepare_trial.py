from pathlib import Path
import json,hashlib
from PIL import Image

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
approval=json.loads((ROOT/'10_automation/runs/2026-W41/reels/M05_full_pair_user_approval_2026-10-08.json').read_text(encoding='utf-8'))
assets=[]
for item in approval['assets']:
    p=ROOT/item['file'];assert sha(p)==item['sha256']
    proof=p.with_name(p.name.replace('_reel_candidate_A','_reel_proof_candidate_v1'))
    assets.append({**item,'actual_pixels':list(Image.open(p).size),'reuse_review':{'head_and_shoes_visible':True,'frontal_identity_information':True,'waist_and_short_hem_readable':True,'background_and_scale_matched':True,'motion_space':'Suitable for small weight shift and shallow turn; no walking or full spin. Figure roughly85% height, larger than planning target but complete shoe/ground margins retained.'},'proof_candidate':proof.relative_to(ROOT).as_posix(),'proof_candidate_sha256':sha(proof),'proof_review':'Vertical, face/collar/short hem/belt/trouser waist clear; candidate still awaits user approval, not sent to Grok or treated as completed delivery.'})
refs=[]
for role in ['face','full']:
    p=ROOT/f'02_brand/reference_models/M05_start_v1_{role}.png';assert p.exists()
    refs.append({'role':role,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'registry_status':'approved'})
protected=json.loads((ROOT/'10_automation/runs/2026-W41/reels/delivery/google_drive_delivery_2026-10-08.json').read_text(encoding='utf-8-sig'))
unchanged=[]
for reel in protected['reels']:
    p=ROOT/reel['source_path'];assert sha(p)==reel['sha256']
    unchanged.append({'model':reel['model'],'source_path':reel['source_path'],'sha256':sha(p)})
prompts={
'A': 'Use the selected Mira M05 v1 face character reference for identity and the uploaded approved cream-jacket image as the exact first frame and wardrobe. One continuous full-person daily-fashion editorial shot, fixed chest-height level camera and natural 50mm perspective. The cream short stand-collar jacket stays open over the white crew-neck tee, black belt, cocoa straight trousers, black loafers and black shoulder bag. Show the relationship between short jacket hem, visible waist and full trouser line. She makes one small, believable shift of body weight from one leg to the other, then settles into a relaxed frontal stance. Start naturally without a prolonged opening hold. Arms stay relaxed away from the waist; hands do not touch the clothes or bag. Ordinary real-time human movement, subtle breathing, no staged slow motion. Keep her entirely visible including head and both shoes. Keep exact garment cuts/colors, face/hair, bag shape and realistic foot-floor contact. The left window frames, gray wall, bench and floor remain completely stationary with the same daylight. No camera move, zoom, wardrobe change, extra gesture, text or audio.',
'B': 'Use the selected Mira M05 v1 face character reference for identity and the uploaded approved charcoal-jacket image as the exact first frame and wardrobe. One continuous full-person daily-fashion editorial shot, fixed chest-height level camera and natural 50mm perspective. The charcoal short stand-collar jacket stays open over the cream crew-neck tee, black belt, light-gray straight trousers, black loafers and black shoulder bag. Show jacket side length and the uninterrupted trouser silhouette. From the frontal stance she makes one shallow body turn approximately25 to35 degrees toward frame-right, briefly lets the side silhouette read, then returns naturally to the original front stance. Her face remains recognizable, turned gently toward the camera rather than showing her back. Feet pivot and bear weight believably without sliding; this is a small turn, not a spin or a walk. Start naturally without a prolonged opening hold. Arms stay loose, no touching clothes or bag. Ordinary real-time human motion, no staged slow motion. Preserve complete head and shoes, exact identity, cuts/colors and bag. Keep the left window, gray wall, bench, floor and daylight stationary. No camera move, zoom, wardrobe change, extra gesture, text or audio.'}
for k,v in prompts.items():(OUT/f'{k}_prompt_v1.txt').write_text(v+'\n',encoding='utf-8')
record={'date':'2026-10-13','user_instruction':'恢復試作，繼續實驗，注意原始目標','status':'resumed_prepared_not_yet_submitted','format_id':'E02','model':'M05','look_ids':[x['look_id'] for x in assets],'original_goal':'Approachable daily-fashion magazine; movements reveal clothing information, comfortable readable edit, repeatable weekly production, later evaluate account growth with publication insights.','viewer_takeaway':'Short jacket hem plus high waist and straight trouser line, seen frontally and at a shallow side angle.','assets':assets,'identity_references':refs,'selected_grok_character_target':'Mira M05 v1 face','planned_settings':{'seconds_per_source':6,'resolution':'720p','aspect':'9:16','audio':False},'planned_join':{'type':'cross_dissolve','seconds':0.75,'nominal_total_seconds':11.25,'frontal_A_end_to_frontal_B_start':True,'actual_interval_selection_pending':True},'max_retry_per_main_shot':1,'source_speed':'unchanged','text':'none','not_new_editing_technology':True,'protected_w41_originals_before':unchanged,'final_user_approval':None,'instagram_performance':None,'active_minutes':None,'generation_wait_minutes':None,'formal_full_proof_carousel_delivery_complete':False}
(OUT/'trial.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Trial prepared; approved sources and protected files hash verified.')
