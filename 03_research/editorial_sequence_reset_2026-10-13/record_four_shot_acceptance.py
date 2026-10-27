from pathlib import Path
import csv,hashlib,json
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=BASE/'four_shot_edit_receipt.json';edit=read(p)
assert hashlib.sha256((ROOT/edit['file']).read_bytes()).hexdigest()==edit['sha256']
approval={'date':'2026-10-13','user_quote':'ok','question_context':'Direct reply after exact10.75s four-shot two-look trial was shown and assistant asked whether middle outfit switch and final return to full-person join felt comfortable.','file':edit['file'],'sha256':edit['sha256'],'seconds':10.75,'scope':'Exact research film visual/editorial acceptance, including current0.75s dissolve joins. Not replacing weekly publishing files, adopting a mandatory account-wide format, confirming production-time targets or proving audience results.','normal_speed_full_playback_user_self_report':None,'assistant_continuous_playback':False,'drive_upload_authorized_by_this_reply':False}
save(BASE/'four_shot_user_approval_2026-10-13.json',approval)
save(BASE/'four_shot_review_v1/user_picture_approval_2026-10-13.json',approval)
edit.update(status='exact_research_picture_user_accepted',user_film_approval=approval)
edit['visual_review'].update(status='sampled_review_complete_exact_picture_user_accepted',user_film_approval=approval,limits='User accepts this exact full film. Does not infer uninterrupted playback self-report, assistant continuous playback, geometric match, production-time targets, mandatory weekly template or IG success.')
save(p,edit)
p=BASE/'four_shot_review_v1/technical_receipt.json';qa=read(p);qa['user_film_approval']=approval;qa['visual_review']=edit['visual_review'];save(p,qa)
p=BASE/'storyboard_candidate.json';story=read(p);story.update(status='exact_four_shot_picture_accepted_repeatability_plan_ready',user_film_approval=approval,repeatability_recipe='REPEATABILITY_RECIPE.md',next_action='M02 W41-003 transfer pilot: first visually inspect existing approved native full-person images/motion for actual reuse, then plan only missing seated styling-proof sources. Maintain original purpose, still gates, dynamic review and protected weekly files.');save(p,story)
with (ROOT/'10_automation/runs/2026-W41/weekly_look_plan.csv').open(encoding='utf-8-sig',newline='') as f:looks=[r for r in csv.DictReader(f) if r['model_profile_id']=='M02']
with (ROOT/'02_brand/mira_reference_images.csv').open(encoding='utf-8-sig',newline='') as f:identity=next(r for r in csv.DictReader(f) if r['model_profile_id']=='M02')
assert identity['status']=='approved'
refs=[]
for field in ['reference_face_path','reference_full_path']:
 r=ROOT/identity[field];assert r.is_file();refs.append({'path':identity[field],'sha256':hashlib.sha256(r.read_bytes()).hexdigest()})
packet={'date':'2026-10-13','status':'planning_only_existing_sources_reuse_review_pending','week':'2026-W41','model':'M02','theme_id':'2026-W41-003','working_title':'咖啡店外的短暫停留','purpose':'Transfer the accepted daily-magazine viewing structure while assessing reduced material retries and measured production effort. Not a new style claim or scheduled publishing batch.','look_plan_rows':looks,'identity_refs':refs,'prompt_age_language':identity['visual_age_prompt'],'first_action':'Review actual approved M02 L01/L02 native full-person images and original clips for scene/clothing/framing/motion reuse. Do not generate duplicate full frames before this review.','candidate_screen_order':['L01 full short-step/proportion','L01 seated waist/outer-layer view','L02 seated collar/waist view','L02 full proportion/short step'],'scene_purpose':'A coherent brief pause outside the existing street-corner cafe setting. Sitting shows tee/outer layer or shirt collar with waist; full shots show straight denim and shoes. Match scene to observed existing sources before choosing exact bench/window geometry.','reusable_source_files':None,'missing_images':None,'new_stills_generated':0,'new_motion_submitted':0,'new_user_still_approval':None,'controls':{'one_model_two_looks':True,'no_baked_text':True,'source_speed_unchanged':True,'dissolve_seconds':0.75,'initial_still_target_if_all_new':4,'reserved_corrections_target':2,'motion_retry_limit_per_candidate':1,'duration':'Derive from reviewed footage;10.75s is accepted reference, not forced timing.'},'timing':{'active_minutes':None,'pure_generation_wait_minutes':None,'user_approval_wait_minutes':None},'limits':'Planning packet only. Approved identity existence and look data verified; source suitability not yet visually reviewed. This packet does not establish new stills, clips, production efficiency or final acceptance.'}
save(BASE/'next_M02_repeatability_plan.json',packet)
report=BASE/'FOUR_SHOT_REVIEW.md';old=report.read_text(encoding='utf-8-sig');report.write_text('> 更新2026-10-13：使用者回覆「ok」，接受這支精確10.75秒研究片與銜接。下方待看片為製作當時歷史；完整播放自述／效率／成效仍未推定。精確核准見`four_shot_user_approval_2026-10-13.json`。\n\n'+old,encoding='utf-8')
update='''## M03日常四鏡已核准；下一輪先驗證製作效率 — 2026-10-13

使用者看過精確10.75秒四鏡片後回覆「ok」，記錄為整支研究片視覺／銜接接受。核准檔：`03_research/editorial_sequence_reset_2026-10-13/four_shot_review_v1/M03_lunch_outing_two_looks_trial_v1.mp4`；SHA與範圍在`four_shot_user_approval_2026-10-13.json`，不推定完整播放自述、五位固定模板、時間效率或IG成效。現已整理`REPEATABILITY_RECIPE.md`及`next_M02_repeatability_plan.json`：下一輪以W41 M02棕丹寧兩套做同形式轉用，先實際查看舊全身素材是否可共用，再補缺的坐姿層次；這次14張靜態生成成本列為未驗證量產效率的問題。下一輪規劃從單一失敗原因與乾淨參照控制補圖，記錄主動／生成等待／核准等待及增量／共用成本。M02人物雙參照存在且核准、兩套週次服裝已核對；素材適用性還未視覺查看，不標可共用。此步只有本機核准與製作規格，無新圖／Grok／Drive／IG／GitHub寫入，既有發布影片保留。下方為歷史進度。

'''
p=ROOT/'CURRENT_STATUS.md';head,rest=p.read_text(encoding='utf-8-sig').split('\n',1);p.write_text(head+'\n\n'+update+rest.lstrip('\n'),encoding='utf-8')
p=BASE/'README.md';p.write_text(update+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
print('Exact film acceptance saved; reusable recipe and M02 transfer planning packet ready. No new media or external writes.')
