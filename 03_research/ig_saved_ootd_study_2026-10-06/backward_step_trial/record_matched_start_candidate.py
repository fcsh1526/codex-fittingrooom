"""Record the failed native join and selected new still; do not grant approval."""
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

BASE=Path(__file__).resolve().parent
ROOT=next(p for p in BASE.parents if (p/'10_automation').is_dir())
JOB=ROOT/'10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/body_distance_matched_start_v2'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p,data):
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

base_still=JOB/'2026-W37-001-L02_M02_body_distance_matched_start_candidate_v1.png'
selected=JOB/'2026-W37-001-L02_M02_body_distance_matched_start_candidate_v2.png'
target=BASE/'qa/near_A1/full/frame_000096.png'
outfit=ROOT/'10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/paired_scene_v1/2026-W37-001-L02_M02_reel_full_master_candidate_v1.png'
face=ROOT/'02_brand/reference_models/M02_start_v3_face.png'
body=ROOT/'02_brand/reference_models/M02_start_v3_full.png'
for p in (base_still,selected,target,outfit,face,body):
    if not p.is_file():
        raise FileNotFoundError(str(p))
    with Image.open(p) as im:
        im.load()

receipt={'date':'2026-10-06','model':'M02','look_id':'2026-W37-001-L02','method':'built_in_image_gen','use_case':'identity-preserve','status':'pending_user_visual_approval',
         'selected_asset':selected.relative_to(ROOT).as_posix(),'selected_sha256':sha(selected),'actual_size':list(Image.open(selected).size),'surface':'reel_native_portrait_9x16',
         'generation_count':2,'base_generation_count':1,'targeted_edit_count':1,'targeted_edit':'person_distance_only','prompt_files':['matched_B_start_v2_prompt.txt','matched_B_start_v2_distance_edit_prompt.txt'],
         'base_preserved':{'path':base_still.relative_to(ROOT).as_posix(),'sha256':sha(base_still),'status':'retained_superseded_before_user_approval'},
         'inputs':[{'role':'composition_edit_target_A_actual_f96','path':target.relative_to(ROOT).as_posix(),'sha256':sha(target),'approval_limit':'Sampled dynamic-QA composition guide, not separately user-approved still.'},
                   {'role':'approved_L02_exact_outfit','path':outfit.relative_to(ROOT).as_posix(),'sha256':sha(outfit)},
                   {'role':'approved_v3_face_identity','path':face.relative_to(ROOT).as_posix(),'sha256':sha(face)},
                   {'role':'approved_v3_full_body_proportions_only','path':body.relative_to(ROOT).as_posix(),'sha256':sha(body)}],
         'root_static_review':{'method':'visible_generated_image_and_composition_comparison','head_position':'v2 closer to A guide; approximate 720-space head top~185 vsA~178','shoe_bottom':'v2~1020 vsA~1060; residual stance/proportion difference remains','same_exact_background_or_pixel_registration':False,'subject_outfit':'same M02; open mist-blue shirt, navy square-neck dress, cream no-lace slip-on shoes, grey shoulder tote visible','future_dynamic_success':None},
         'independent_review':'03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/qa/matched_B_start_v2/independent_review.md','independent_review_status':'pending_at_recording','user_approval':None,'uploaded_to_Grok':False,'video_generated_from_selected_still':False,'text':'none','publishable':False,'cloud_write':False,'original_assets_overwritten':False}
save(JOB/'generation_receipt_v2.json',receipt)
prompts='\n\n'.join(['# Matched second-look starting image\n\nMethod: built-in image_gen. Selected v2 is a candidate pending individual visual approval. One base plus one targeted person-distance correction; originals preserved.',
                    '## Base\n\n'+(BASE/'matched_B_start_v2_prompt.txt').read_text(encoding='utf-8'),
                    '## Single distance correction\n\n'+(BASE/'matched_B_start_v2_distance_edit_prompt.txt').read_text(encoding='utf-8')])
(JOB/'PROMPTS.md').write_text(prompts+'\n',encoding='utf-8')
columns=['filename','model_consistency','body_proportion_consistency','reader_relatability','outfit_clarity','ai_realism','commerce_value','scene_lighting_integration','outfit_continuity','expression_liveliness','pose_variation','canva_frame_fit','publishable','status','notes']
with (JOB/'review_sheet.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=columns)
    writer.writeheader()
    writer.writerow({'filename':selected.name,'publishable':'no','status':'candidate_pending_user_visual_approval','notes':'Root static identity/outfit/framing review; closer head position to actual A f96, feet/body residual remains. Numerical scores not assigned; video and user approval untested. Independent review linked in receipt.'})

for folder,qa,sha_value,mechanism,notes in [
    ('near_start_A_attempt_01','near_A1','be49906fa1ec7397bb456acc1ce7947325e71b4ce5a0692d7235d878ad6017ea','whole_person_retreat_observed','Shoes fully visible around1.75s but near lower edge; multiple steps, not exactly two then hold.'),
    ('grok_B_attempt_01','B1','afa46cced85bf886029940f36b7bbbd0bf188b5ebe49d8ac5d7f5f278ea62e5b','whole_person_approach_observed','Shoes leave frame around3s as person approaches; later square neckline/waist readable, slight torso side angle and partial tote occlusion.')]:
    source=BASE/folder/'source.mp4'
    if sha(source)!=sha_value:
        raise ValueError('Source hash mismatch')
    save(BASE/folder/'sampled_review.json',{'date':'2026-10-06','source_sha256':sha_value,'qa':f'qa/{qa}/','root_reviewed':'25 full checkpoints, 5 head windows, all145 consecutive native lower-body windows; B f0/f144 full native also viewed','mechanism':mechanism,'sampled_identity_wardrobe_background':'no obvious major jump seen','notes':notes,'assistant_continuous_watch':False,'user_video_approval':None,'not_a_reliable_success_rate':True})

out_path=BASE/'M02_body_distance_review_v1.json'
out=json.loads(out_path.read_text(encoding='utf-8'))
out.update(status='retained_diagnostic_join_rejected_before_user_review',assistant_sampled_review='root viewed25 checkpoints and all27 consecutive transition/boundary frames; visible double-face residual',user_approval=None,publishable=False)
out['join_gate']='failed: head location/proportion mismatch produces obvious double faces during dissolve'
out['next_plan']='revised_storyboard_v3.md'
save(out_path,out)

mp=BASE/'trial_manifest.json'
m=json.loads(mp.read_text(encoding='utf-8'))
m.update(status='near_A1_retreat_passed_B1_approach_passed_native_join_failed_matched_B_v2_pending_user_approval',new_stills_generated=4,new_video_sources_retrieved=4,B_started=True,output='M02_body_distance_review_v1.mp4')
m['B_attempts']=[{'folder':'grok_B_attempt_01','send_clicks':1,'source_retrieved':True,'sha256':'afa46cced85bf886029940f36b7bbbd0bf188b5ebe49d8ac5d7f5f278ea62e5b','mechanism_pass':True,'quality_gate':'root_sampled_identity_wardrobe_background_and_all_lower_body_sequence','qa':'qa/B1/','root_review':'grok_B_attempt_01/sampled_review.json'}]
m['dynamic_qa'].update(stage='sources_sampled_pass_native_join_rejected',new_composite='8.25s diagnostic retained; visible double-face residual, not submitted for approval',near_start_source='retrieved_reviewed',assistant_continuous_full_watch=False)
m['revised_storyboard']='revised_storyboard_v3.md'
m['matched_second_start']={'path':selected.relative_to(ROOT).as_posix(),'sha256':sha(selected),'status':'pending_user_visual_approval','generation_receipt':(JOB/'generation_receipt_v2.json').relative_to(ROOT).as_posix(),'base_count':1,'single_targeted_edit':1,'uploaded_to_Grok':False,'new_B_source_generated':False}
m['protected_media_hashes_matched']=out['protected_media_hashes_matched']
m['browser_cleanup']='After runtime bindings were discarded, reacquiring the known temporary tab6 returned Tab not found in browser2; no unknown user tab closed.'
save(mp,m)

readme=(BASE/'README.md').read_text(encoding='utf-8')
latest='''## 最新結果：兩套動作可用，但接段不通過；新 B 起點待逐張核准

使用者核准近起點v2後，一次 near_A1 生成確實退遠；一次 B1 生成確實走近。各為720×1280、24fps、145幀／6.041667秒，根據25全圖、5頭部及完整145下肢序列的root抽查未見明顯換臉／換衣／大幅背景跳變。正常速度完整播放與使用者影片核准未宣稱。

原生試剪v1為8.25秒，A[0,72)與B[0,144)，0.75秒／18幀疊加；完整技術解碼通過，五支待發與三個舊研究成片SHA保持相同。root已看25輸出檢查點與全27過場前後連續幀；雙臉重影明顯，接點不通過，保留診斷檔但不送為可發布影片。

新分鏡在 `revised_storyboard_v3.md`：以實際 A f96／4秒為人物距離與房間基準，換成核准 L02 衣服。內建影像生成一張base，再只修人物距離一次；selected v2在L02週次素材的 `reel/body_distance_matched_start_v2/`。頭位更接近，但不是像素精準對齊；還需逐張使用者核准及真正新B來源驗收。沒有送入Grok、沒有新B2或新核准成片。第一波／Drive未改，沒有文字、音樂、改速或發布。以下較早近起點待核准紀錄為歷史。

'''
readme=readme.replace('## 最新結果：原全身起點兩次失敗，新近距離起點待核准',latest+'## 歷史結果：原全身起點兩次失敗，新近距離起點當時待核准',1)
(BASE/'README.md').write_text(readme,encoding='utf-8')

sp=ROOT/'CURRENT_STATUS.md'
s=sp.read_text(encoding='utf-8')
head='''## M02 distance sources pass sampled gate; native join failed; matched B v2 pending visual approval — 2026-10-06

New near_A1 retreat and B1 approach were each retrieved once (720×1280/24fps/145frames/6.041667s). B1 SHA `afa46cced85bf886029940f36b7bbbd0bf188b5ebe49d8ac5d7f5f278ea62e5b`; root25 full/5 head/all145 lower-body windows find useful movement and no obvious major sampled identity/wardrobe/background jump. Actual walking exceeds nominal two short steps; no continuous watch/user video pass inferred. Separate native8.25s diagnostic `M02_body_distance_review_v1.mp4`, SHA `170caa07b1f385562c93151ce1d03c3689504be8503dfb701d79d7c48c70acc6`, renders A[0,72)+B[0,144) with18-frame0.75s dissolve, no crop/retime/text/audio. Decode passes and protected first-wave five plus three accepted research hashes match. Root25 output samples/all27 transition boundary frames show obvious double faces; join rejected before user review. Revised v3 uses actualA f96/4s scene/person geometry to create L02 matched starting still, one base+one targeted distance edit; selected candidatev2 SHA `27298b46bcc0aeb18928dc540d6ee94e64be7287de2c39f2ba8a2f6e7ba32fa5` under L02 `reel/body_distance_matched_start_v2/`,941×1672. Still pending individual user approval, not uploaded toGrok or dynamically tested; head closer, residual feet/proportion/background alignment remains. Full receipts/prompts/reviews in `03_research/ig_saved_ootd_study_2026-10-06/backward_step_trial/`. No first-wave overwrite, cloud write, publication, global format or audience result. Prior notes below historical.

'''
s=s.replace('# Current Status - Mira AI Fashion Creator\n\n','# Current Status - Mira AI Fashion Creator\n\n'+head,1)
sp.write_text(s,encoding='utf-8')
print(json.dumps({'status':m['status'],'candidate':str(selected),'sha256':sha(selected),'native_join':'rejected_preserved','user_approval':None},ensure_ascii=False))
