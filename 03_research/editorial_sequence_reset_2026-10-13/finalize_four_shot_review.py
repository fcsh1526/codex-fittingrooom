from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
method='All258 output thumbnails,25 larger whole-frame samples,5 face samples and all23 boundary/overlap samples at each of3 joins (all18 dissolve frames per join) viewed. Native source spot checks recorded separately. No assistant continuous normal-speed playback.'
review={'status':'sampled_frame_review_complete_user_whole_film_review_pending','method':method,'single_source_findings':'Recognizable face and readable locked wardrobe in sampled intervals; no gross instantaneous face/clothing/hand/bag/background morph observed.0black candidates;258 frames decoded. Does not certify native contact or exact architecture every frame.','join_findings':{'A1_A2':'Standing/seated body scale and position differ; visible double heads and bench outlines. Retains previously direction-accepted first-look cut.','A2_B1':'Seated head/waist focus closer than full→medium, but size, x-position and bench/window viewpoint differ; visible face/body overlap. Not an invisible change.','B1_B2':'Seated/standing scale differs and viewing direction changes; visible larger/smaller double head/body during0.75s overlap. Comfort requires whole-film viewing.'},'assistant_continuous_playback':False,'user_film_approval':None,'limits':'Still approvals and first-look direction acceptance do not approve this full film, adopt a weekly template, prove production-time targets or establish IG performance.'}
p=BASE/'four_shot_edit_receipt.json';edit=read(p);edit['status']=review['status'];edit['visual_review']=review
edit['unoverlapped_reading_seconds']={'A1':1.5,'A2':2.5,'B1':2.25,'B2':2.25}
edit['research_cost']={'still_generation_calls':14,'by_shot':{'A1':2,'A2':4,'B1':4,'B2':4},'confirmed_motion_results':4,'total_server_generations':None,'unconfirmed_UI_send_actions':1,'active_minutes':None,'pure_generation_wait_minutes':None,'note':'B2 had one unconfirmed locator send before UI recovery. Rebuilds and material failures retained; not a demonstrated30–60min production recipe.'}
edit['source_behavior_limits']={'A1':'Initial one-step/settle, not sustained crossing.','A2':'Already seated torso adjustment; no sit-down action.','B1':'Looks toward image-left rather than prompted right.','B2':'Mainly forward step then posture change; not sustained departure.'}
save(p,edit)
p=BASE/'four_shot_review_v1/technical_receipt.json';d=read(p);d['visual_review']=review;save(p,d)
for source in edit['sources']:
 p=ROOT/source['technical_receipt'];d=read(p);d['retained_interval_seconds']=source['seconds'];d['retained_frames_end_exclusive']=source['frames'];d['final_trial_edit_receipt']='03_research/editorial_sequence_reset_2026-10-13/four_shot_edit_receipt.json';d['user_film_approval']=None;save(p,d)
p=BASE/'storyboard_candidate.json';s=read(p)
s.update(status='four_shot_two_look_trial_exported_user_review_pending',b1_confirmed_motion_result_count=1,trial_file=edit['file'],trial_sha256=edit['sha256'],actual_trial_seconds=10.75,actual_source_frames=[54,96,90,72],actual_dissolves=edit['transitions'],visual_review=review,next_action='Show exact10.75s four-shot two-look research film for whole-film user comfort and daily-magazine review. If accepted, assess repeatability and plan next trial; do not overwrite accepted weekly publishing originals or infer audience success.')
save(p,s)
report='''# 午休的小出走：完整四鏡試片

2026-10-13。完整研究候選已輸出，待使用者看片。

成片：`four_shot_review_v1/M03_lunch_outing_two_looks_trial_v1.mp4`，10.75秒／720×1280／24fps／258幀。恰好同一位M03及W41-004兩套服裝。原速、無字、無音、無裁切縮放、無凍結或加速。

|鏡頭|來源保留|剪輯中的用途|無疊化的閱讀時間|
|---|---|---|---|
|A1 第一套全身|0–2.25秒|午休走過的一小步|1.5秒|
|A2 第一套坐姿|0–4秒|看西外、棉T與坐姿褲線|2.5秒|
|B1 第二套坐姿|0–3.75秒|延續窗邊片刻與第二套疊穿|2.25秒|
|B2 第二套全身|0–3秒|回到整套比例與短步／自然站姿|2.25秒|

三個0.75秒疊化區間：1.50–2.25、4.75–5.50、7.75–8.50秒。B2實際沒有持續離開畫面，B1實際向左看；不將提示詞寫成已達成動作。四張起始圖皆已獲精確核准，第一套片段方向已接受；完整成片審美核准尚未成立。

## 驗收

來源各145張縮圖、25張大圖及5張臉部；原尺寸抽查各鏡另記。成片看過全部258張縮圖、25張大圖、5張臉部，以及三處各23張接點圖（包含每處18張疊化幀）。單鏡取樣臉、服装、手包與背景大致稳定；無黑幀或解碼錯誤。不等於逐幀原尺寸接觸／背景幾何或完整正常播放通過。

站姿與坐姿的尺度和頭部位置不相同，中間兩坐姿亦有小幅差異；疊化會出現雙頭／身體／窗椅輪廓。保留使用者指定的柔和疊化，正常播放的舒服度與雜誌感由整段觀看評估。不宣稱無差別軟換、IG最佳秒數或流量效果。

## 成本與保護

本方向共14次靜態生成：A1兩次，A2／B1／B2各四次。四個確認的Grok結果；B2另有一次未確認建立任務的定位送出，伺服器是否計數／計費留空。主動製作與純等待時間未完整量測，不能宣稱已達30–60分鐘量產目標。

W41原五支交付影片在輸出時皆雜湊一致；研究獨立保存，沒有Drive／GitHub／IG發布。Carousel三張套組未由本試片完成。失敗材質與重建證據全保留。完整來源／提示詞版本／核准範圍／剪點／檢查與雜湊見`four_shot_edit_receipt.json`與各鏡紀錄。
'''
(BASE/'FOUR_SHOT_REVIEW.md').write_text(report,encoding='utf-8')
update='''## M03午休小出走：完整10.75秒四鏡試片待觀看 — 2026-10-13

B1v4坐姿已由使用者「可以，沿用最後這張」核准，Grok以Mira M03 v3＋單一First frame、720p／6秒／9:16／無音生成並下載一次。全片現已組成A1走過→A2第一套坐姿→B1第二套坐姿→B2全身短步，來源保留2.25／4／3.75／3秒，三處0.75秒疊化；10.75秒、258幀、原速、無字無音。全258縮圖、25張大圖、5臉部及三處各23接點圖已看；單鏡未見明顯瞬間跳變，但接點有人物尺度／位置與背景輪廓重影，尤其坐姿→全身，待使用者完整正常播放判斷舒服度與日常雜誌感。助手連續播放未成立，不標整片核准。B1實際向左看、B2偏前方短步＋站姿變化，非持續離開。成片：`03_research/editorial_sequence_reset_2026-10-13/four_shot_review_v1/M03_lunch_outing_two_looks_trial_v1.mp4`；`FOUR_SHOT_REVIEW.md`與`four_shot_edit_receipt.json`保存完整來源、提示詞、核准、剪點與檢查。共14次靜態生成、4個確認Grok結果；耗時未完整量測，量產效率未驗證。輸出時原W41五支交付雜湊一致，無Drive／GitHub／IG寫入；Carousel仍未完成。下方為歷史進度。

'''
p=ROOT/'CURRENT_STATUS.md';heading,rest=p.read_text(encoding='utf-8-sig').split('\n',1);p.write_text(heading+'\n\n'+update+rest.lstrip('\n'),encoding='utf-8')
p=BASE/'README.md';p.write_text(update+p.read_text(encoding='utf-8-sig'),encoding='utf-8')
print('Complete10.75s trial receipts finalized. User whole-film review pending; protected5 originals unchanged.')
