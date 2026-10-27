from pathlib import Path
import json,hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
observations={
 'A_attempt_01':('selected_after_editorial_replan','Shallow turn0.75-2.25s and front returnabout3s; originally rejected only for assigned frontal role. Reassigned as second silhouette shot after B02 remained frontal. Retain0-4.75s. All145 thumbnails,25 full samples,5 face samples and native frame36 viewed. Face/clothes/background broadly stable; bag briefly occluded by arm and returns. No verified back exposure.'),
 'A_attempt_02':('frontal_alternate_not_in_final','Small stance/weight adjustment, predominantly frontal. All145 thumbnails,25 whole and5 face samples plus native frame24 viewed. Clothing/background broadly stable. Does not add side information; retained as alternate, not final film.'),
 'B_attempt_01':('not_selected_motion_exposes_unverified_back','Actual turn exposes unverified back atabout2-3s; source excluded, not recycled in final film.'),
 'B_attempt_02':('selected_as_frontal_shot_after_editorial_replan','Planned shallow diagonal stance not clearly achieved. All145 thumbnails,25 whole and5 face samples plus native frame36 viewed. Small foot/weight shift and breathing, mostly front. Face/wardrobe/window/wall/bench/floor broadly stable. Retain0-4s as first frontal-proportion shot. Does not count as prompt-compliant shallow-turn success.')}
for name,(status,obs) in observations.items():
 p=OUT/name/'technical_receipt.json';d=read(p);d.update({'visual_review':status,'final_review_observations':obs,'assistant_continuous_playback':False,'user_film_approval':None});save(p,d)
review={'method':'All192 film thumbnails,25 larger whole frames,5 face samples, all21 join/boundary samples and native turn/stance source frame36 viewed. No assistant continuous normal-speed watch claimed.',
 'identity_clothing_background':'Recognizable M05 and respective short jackets, tee, high waist, straight trousers, belt, bag and loafers in retained views. Window/wall/bench/floor remain broadly fixed; no obvious architectural drift observed in sampled/thumbnail views.',
 'transition':'3.25-4.00s,18frames cross dissolve. Small head/foot position differences create transient double outlines and face ghosting; not an invisible outfit morph. No black-frame signal or size jump by crop/zoom. Comfort requires user normal-speed playback.',
 'editorial':'Charcoal/light gray front proportion then cream/cocoa shallow turn and return. Same short-jacket/high-waist/straight-leg theme. First shot quiet; viewer usefulness and magazine feeling remain unvalidated.',
 'technical_limits':'Only four diagnostic generations. Exact angle/pose control did not consistently follow prompts, so repeatable production is not established. Native tiny hand/shoe/bag details not certified on every frame.'}
p=OUT/'review_v1/technical_receipt.json';d=read(p);d.update({'visual_review':'frame_review_completed_user_normal_speed_review_pending','review':review});save(p,d)
p=OUT/'edit_receipt.json';d=read(p);d.update({'status':'candidate_ready_for_user_normal_speed_review','review':review});save(p,d)
trial=read(OUT/'trial.json')
trial.update({'status':'candidate_ready_for_user_normal_speed_review','actual_generation_count':4,'actual_retries_by_look':{'L01':1,'L02':1},'selected_attempts_in_screen_order':['B_attempt_02','A_attempt_01'],'actual_seconds':8.0,'final_file':d['file'],'edit_receipt':'edit_receipt.json','editorial_replan':d['replan'],'repeatability_validated':False,'formal_full_proof_carousel_delivery_complete':False,'time_measurement_note':'Browser receipts contain submission-to-download elapsed wall time, which includes parallel QA/editorial work. Active production minutes and pure generation wait were not measured independently; remain null.'})
trial['planned_join']['actual_interval_selection_pending']=False
trial['planned_join']['superseded_by']='Actual retained B02 0-4s then A01 0-4.75s;0.75s overlap;8s total. Planning11.25s is not claimed achieved.'
trial['protected_w41_originals_after']=d['protected_w41_originals']
save(OUT/'trial.json',trial)
report='''# M05 E02 動態輪廓試作 — 2026-10-13

## 原始目標與本輪問題

做出親切、精緻的日常服裝雜誌影像，讓動作增加服裝資訊，剪輯舒服，並能持續每週生產。流量與收入須由發布後資料驗證。這次用「短外套＋高腰直筒褲」測正面比例與淺側身輪廓；兩套屬同一主題，不設定誰比較好。

## 實際交付

- 試片：`review_v1/M05_E02_silhouette_two_looks_v1.mp4`，8秒、720×1280、24fps。
- 第一鏡：M05 L02 炭灰短外套／淺灰褲，B第二次生成0–4秒，正面與小幅重心變化。
- 第二鏡：M05 L01 奶油白短外套／可可棕褲，A初次生成0–4.75秒，淺側轉再回正。
- 3.25–4秒為0.75秒疊化；來源原速，僅剪掉較長尾段停留。沒有字幕或音軌；此輪不需另加文字。
- 這是同樣柔和剪接的另一種觀看目的，不宣稱新剪輯技術。

## 四次生成與調整原因

|素材|實際動作|處理|
|---|---|---|
|A初次|正面、淺側轉、回正|起初不符合「只換重心」角色；後來改作輪廓鏡並採用|
|A修正一次|基本維持正面、小幅換重心|保留為備選，未進成片|
|B初次|轉到背面再回正|超出分鏡、背部設計未驗證，不採用|
|B修正一次|基本維持正面|不符合原定側轉，但可作正面比例鏡，採用|

兩鏡各只重試一次。改排現有合格段落，沒有第五次生成。實際觀看順序改成L02→L01。這是利用素材完成可評估試片，尚不能證明提示詞能穩定複製分鏡。

## 檢查與限制

192格全片解碼成功，未出現黑格候選。已看全部縮圖、25張較大全身畫面、5張臉部畫面、21張轉場與邊界畫面，以及來源原尺寸的轉身／站姿畫面。檢查中人物、服裝與固定背景大致穩定；轉場有短暫雙輪廓與臉部重影，並非無差別換裝。縮圖與抽格檢查不等於正常速度完整播放；整支節奏、觀看舒適度與最終核准待使用者播放回饋。微小手指、鞋包細節沒有逐格原尺寸認證。

第一鏡仍偏安靜。需確認正面閱讀時間是否適當，以及第二鏡的側轉有沒有讓衣長與褲管更容易看懂。若僅是好看的展示，下一輪应提升觀看路線與服裝資訊，不以更快動作或更多轉場當作改善的證據。

## 每週生產是否可行

本輪4次生成，兩套各1次重試；動作控制未完全符合要求。不能由此推算成功率，也未達成已驗證量產。主動製作與純生成等待未分別計時，欄位留空；瀏覽器收據的送出至下載時間包含其他檢查，不當作純等待。影片尚未發布，因此沒有IG成效結論。

## 檔案保護與素材狀態

原W41五支已交付影片製作前後雜湊相同；原發布檔與Drive未被覆蓋。沒有Drive／GitHub／IG寫入。兩張第一幀沿用2026-10-08精確核准檔；固定Mira M05 v1 face參照在Grok選取。本機全身人物參照只作身分核對，不宣稱已在Grok選取。既有proof候選仍待核准，本輪不等於正式full＋proof＋Carousel整套完成。

詳細來源、提示詞、生成設定、網址、區段、雜湊、驗收與缺失見`trial.json`、`edit_receipt.json`及各attempt收據。

## 接續

先取得這支整體觀看回饋，再決定E02是否值得複測；若可接受，可接E01日常片段測試，讓接近／停留／離開承接服裝觀看，避免全部試片都變成兩套對比。新起始圖仍須先視覺核准。只做原始目標需要的實驗，保留可发布批次與成效追蹤路徑。
'''
(OUT/'REVIEW.md').write_text(report,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8');start=s.index('## Media trial resumed');end=s.index('\n## Six detailed',start)
s=s[:start]+'''## E02 M05 silhouette trial ready for normal-speed user review — 2026-10-13

User resumes media trial explicitly. Four Grok generations completed, one retry per look, exact approved W41 M05 full stills and selected Mira M05 v1 face reference. A01 performed a useful shallow turn; A02 and B02 stayed mostly frontal; B01 exposed an unverified back and was excluded. Replanned order B02(L02) front0–4s → A01(L01) shallow turn/return0–4.75s. Research candidate `03_research/reel_presentation_study_2026-10-12/E02_silhouette_2026-10-13/review_v1/M05_E02_silhouette_two_looks_v1.mp4`:8s,720×1280,24fps,192frames, original speed,0.75s dissolve at3.25–4s, no text/audio. All film thumbnails,25 whole,5 face and21 join samples plus native source stance/turn frames reviewed; recognizable identity/wardrobe and fixed background broadly retained, transient double outlines remain in dissolve. Normal-speed whole-film user comfort and approval pending; no assistant continuous-watch claim. Exact motion control and repeatable production not validated; four generations are diagnostic only. Original five W41 delivered videos hash-verified unchanged before/after; no Drive/GitHub/IG writes. Proof candidates remain unapproved; not a completed formal full/proof/Carousel package. Receipts and findings in `trial.json`, `edit_receipt.json`, `REVIEW.md`. Previous planning-only hold revoked; historical entries below retained. Next: obtain film feedback, then select a purpose-driven follow-on experiment toward approachable editorial/useful clothing viewing/sustainable weekly production; growth claims await actual publishing data.
''' +s[end:];p.write_text(s,encoding='utf-8')
p=OUT.parent/'editorial_presentations/PLANNING_INDEX.md';s=p.read_text(encoding='utf-8');s='# Active execution update — 2026-10-13\n\nUser explicitly resumed media experiments. E02 M05 has an8s research candidate ready for normal-speed user review; see `../E02_silhouette_2026-10-13/REVIEW.md`. Exact pose control and repeatable weekly production remain unvalidated; original delivery protected. Older planning-only statements below are historical and superseded for this resumed trial. Other concept cards are plans, not completed films.\n\n'+s;p.write_text(s,encoding='utf-8')
assert all(hashlib.sha256((ROOT/x['source_path']).read_bytes()).hexdigest()==x['sha256'] for x in trial['protected_w41_originals_before'])
print('Review and status saved; protected five delivery sources unchanged.')
