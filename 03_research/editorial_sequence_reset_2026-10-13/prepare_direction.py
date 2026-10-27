from pathlib import Path
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (ROOT/'02_brand/mira_reference_images.csv').open(encoding='utf-8-sig',newline='') as f:ref=next(r for r in csv.DictReader(f) if r['model_profile_id']=='M03')
assert ref['status']=='approved'
refs=[]
for key in ['reference_face_path','reference_full_path']:
 p=ROOT/ref[key];assert p.is_file();refs.append({'path':ref[key],'sha256':sha(p),'registry_status':ref['status']})
with (ROOT/'10_automation/runs/2026-W41/weekly_look_plan.csv').open(encoding='utf-8-sig',newline='') as f:looks=[r for r in csv.DictReader(f) if r['model_profile_id']=='M03']
assert [r['look_id'] for r in looks]==['2026-W41-004-L01','2026-W41-004-L02']
roster=json.loads((ROOT/'02_brand/mira_model_roster.json').read_text(encoding='utf-8-sig'))
profile=next(p for p in roster['profiles'] if p['model_profile_id']=='M03')
sources=[{'url':'https://www.instagram.com/fudge_magazine/reel/DdavjIjThdp/','account':'fudge_magazine','status':'new_browser_autoplay_samples_observed','evidence':'fudge_daily/samples.json','samples':46,'observed_mechanisms':['Same everyday outing links front walking, lateral travel, lower garment detail and a later seated rest.','Street/shop/tree locations have a role in the outing rather than arbitrary backgrounds.'],'representative_brackets':[{'indices':[37,38,39],'purpose':'Front walking with full outfit around12.9-14.9s'},{'indices':[40,41,42],'purpose':'Lateral travel and garment side around15.7-17.6s'},{'indices':[6,7,8,9],'purpose':'Lower body/shirt and moving garment detail around26.6-29.5s'},{'indices':[17,18,19,20],'purpose':'Later seated outdoor rest around36.9-39.9s'}],'commercial_context':'Visible brand partnership and bicycle promotion; not a non-ad source.','limits':'Muted browser screenshots, roughly one persecond, spanning a playback wrap. Not exact cut times, original frames, uninterrupted audiovisual review or verified clothing-account performance.'},
 {'url':'https://www.instagram.com/pazzo/reel/DdYmOpBPfxs/','account':'pazzo','status':'new_browser_autoplay_samples_observed','evidence':'pazzo_daily/samples.json','samples':20,'observed_mechanisms':['Wall-side body angle, wider seated clothing views and an upper/lower simultaneous detail/full arrangement appear.'],'commercial_context':'Clothing product promotion with burned-in claims/words.','limits':'Not copied as Mira format. Reclining poses, large text, product performance claims, split layout and exact source rhythm are not adopted. Muted screenshot sampling only.'}]
shots=[
 {'id':'A1','look_id':looks[0]['look_id'],'source_seconds_budget':3.75,'framing':'Native9:16 full person, visible head and shoes; camera chest-height/level/50mm view.','scene':'Quiet covered lunch-shop walkway by a plain window and fixed wooden bench; soft daylight from image-left.','start':'Model left of center in shallow front-three-quarter view, frontal readable face; front foot planted, trailing toe grounded; walking path remains inside frame.','action':'One or two ordinary steps diagonally toward image-right, no torso turn/cloth touch/camera approach.','camera':'Fixed; no zoom or simulated slowdown.','clothing_information':'Complete open cream blazer/white tee/navy straight trouser proportion and natural garment motion.','end':'Still moving slightly; do not wait for pose or look directly at viewer.','required_still':'New full-person movement-start image, not reuse the centered stance just for convenience.'},
 {'id':'A2','look_id':looks[0]['look_id'],'source_seconds_budget':3.25,'framing':'Head to knees, comfortable front-three-quarter seated view; lapels/tee waist and bent trouser line remain visible.','scene':'Same window/bench/light; physically consistent photographed angle change.','start':'Already seated upright, feet supported on ground outside or within frame; shoulders relaxed, hands resting simply on thighs away from lapel/waist.','action':'One small natural torso lean toward the daylight, then relaxed settle. No full sit-down choreography.','camera':'Fixed chest-height relative to seated subject, level50mm view; different viewpoint is a cut, not an implied camera move.','clothing_information':'How open lapels, cotton tee neckline and trouser folds relate in a everyday seated posture. No comfort or fabric-performance claim.','end':'Head and chest near planned B1 entry position.','required_still':'New seated image derived from visually approved A1 wardrobe/scene lock plus approved identity anchors.'},
 {'id':'B1','look_id':looks[1]['look_id'],'source_seconds_budget':3.25,'framing':'Same head-to-knees seated frame, scale and lapel/waist focus as A2.','scene':'Same bench/window/daylight; second outfit is another styling example, not literal instantaneous clothing change.','start':'Seated, front-three-quarter face visible; hands simply resting.','action':'Small upper-body change of attention toward the walkway, no touch/standing transition.','camera':'Fixed same seated chest-height level50mm viewpoint as A2.','clothing_information':'Navy lapels around gray tee, plus light straight trousers; theme remains blazer with everyday cottontee.','end':'Keep a readable shoulder direction suitable for B2 departure viewpoint.','required_still':'New seated L02 image; cannot use L01 approval for L02.'},
 {'id':'B2','look_id':looks[1]['look_id'],'source_seconds_budget':4,'framing':'Full person and shoes, head visually placed near B1 ending focus; no abrupt wide-angle perspective.','scene':'Same covered walkway/bench; departure into clear space on image-right.','start':'Already standing, shallow front-three-quarter walking start, face has sufficient identity information.','action':'One or two steps across clear walkway toward image-right; keeps head and shoes in frame through retained interval.','camera':'Fixed chest-height level50mm view; no camera approach/retreat.','clothing_information':'Return to complete navy-blazer/light-trouser outfit after the seated layer view.','end':'Natural mid-walk exit direction; retain whole outfit, no forced loop.','required_still':'New L02 full-person start; reused source requires geometry/framing review first.'}
]
plan={'date':'2026-10-13','status':'reference_review_complete_storyboard_candidate_no_media_generated','working_title':'午休的小出走','model':'M03','look_ids':[r['look_id'] for r in looks],'wardrobe_locked':[{'look_id':r['look_id'],'outfit':r['clothing_item'],'dressing_decision':r['dressing_decision'],'visual_proof':r['visual_proof']} for r in looks],'identity_references':refs,'prompt_age_language':profile['prompt_age_language'],'original_goal':'Approachable refined everyday clothing magazine; clear outfits, comfortable whole-film viewing, sustainable weekly production; later validate account growth with publishing results.','actual_difference_to_E02':'Whole-film spatial/posture sequence: moving full outfit → same-look seated layer view → other-look seated layer view → moving full outfit. Cuts within one outfit establish an everyday moment. Not merely different standing poses or a concept rename.','history_caveat':'Full→medium→medium→full ordering already used in Mira v2/D-related studies. Four shots, close/full ordering and dissolve are not new techniques. Proposed new viewing experience comes from lateral travel, seated clothing context and same-occasion shot relationships; difference must be judged in actual film.','source_observations':sources,'shots':shots,'planned_dissolves':[{'from':'A1','to':'A2','seconds':0.75,'check':'Scale changes plus seated height require joint storyboard review: face/lapel focus and light matched, not superimposed standing/seated bodies as a trick. If sustained double scale is uncomfortable, redesign adjacent view, do not shorten user dissolve or revert to rejected two-full version.'},{'from':'A2','to':'B1','seconds':0.75,'check':'Same seated scale, head/waist and bench geometry; outfit changes only here. Not a comparison hook.'},{'from':'B1','to':'B2','seconds':0.75,'check':'Maintain face/lapel viewing location and light; no jump in gaze direction. Standing/seated change must feel like montage, not magic standing-up.'}],'duration_budget_seconds':12,'source_budgets_seconds':[3.75,3.25,3.25,4],'unoverlapped_reading_seconds':[3,1.75,1.75,3.25],'timing_note':'Planning budgets only, not exact source cutpoints, achieved media or IG-optimal length. Recompute after dynamic QA.','text':'none','music':'Optional manual IG addition later; no music/tempo conclusion from muted references.','control_and_risk':'Four shots cost more than two. First test A1+A2 as same-outfit sub-sequence; if new views cannot join comfortably, stop/replan rather than generating B or converting back into rejected fixed-full dissolve route. Each motion candidate has at most one retry.','still_gate':'Review new exact stills visually with user before Grok. Still approval is not film approval.','formal_asset_scope':'Each look still needs a native full9:16 plus useful proof and separate CarouselABC; this trial plan is not completed production.','accepted_weekly_files_changed':False,'next_action':'Prepare new L01 full movement-start candidate from the above entire storyboard. Use accepted A1 as same-look wardrobe/scene lock before A2. No automatic mass production.'}
save(OUT/'storyboard_candidate.json',plan)
report='''# 回到整支影片：參考拆解與下一版候選

2026-10-13。最新M05 E02已被否決，保留作研究證據。這次完成新一輪實際頁面播放取樣，沒有生成圖片或影片。

## 實際看到的機制

[FUDGE日常外出片](https://www.instagram.com/fudge_magazine/reel/DdavjIjThdp/)：完整行走、側向移動、下半身細節與後段坐下休息組成同一次外出。人物不只面向相機輪流展示衣服。拍到的範圍與時間區間見46張頁面截圖及samples.json。此片明確為自行車品牌合作；借其生活片刻的組織，不複製雙人、自行車、產品廣告與文字。

[PAZZO服裝片](https://www.instagram.com/pazzo/reel/DdYmOpBPfxs/)：本輪20張頁面截圖可見靠牆、坐姿、衣服近景，以及上下同時顯示細節與較完整造型。它不是Mira下一版模板；不採躺姿、露腹造型、大字、產品性能主張或上下版面。它僅補充「不同身體姿態會提供不同服裝資訊」的可見例子。

兩支均靜音取樣，沒有取得精確切點、音樂節拍、留存與可比較曝光。截圖區間不是鏡頭起止。未下載原影片，不宣稱完整逐格或連續有聲觀看。

## 下一版：午休的小出走

M03，沿用W41兩套既定西外＋棉T，不新增服裝、不編優劣比較。午餐店外同一有頂走道、木椅與窗光，服裝先在行走中呈現，再在坐姿看清外層與棉T的關係。日常動作承接鏡頭，衣服是觀看主體。

|鏡頭|画面與主要動作|新增看到什麼|
|---|---|---|
|A1，第一套|米白西外／白T／深藍褲，全身自然走過一至兩步|完整比例、走動中的外套與褲管|
|A2，同一套|已坐在窗邊木椅，頭至膝的斜正面；小幅自然前傾|翻領與棉T圓領、坐姿中的外套開口和褲線|
|B1，第二套|深藍西外／淺灰T／奶油白褲，同類坐姿構圖；視線自然轉向走道|相同日常搭法的另一個造型，不改為評比|
|B2，同一套|全身走向右側清楚空間，不走向攝影機|補完整第二套輪廓，讓片段有離開的收束|

## 與舊片的實際差異與界線

四鏡和「全身→中景→中景→全身」順序都曾試過，不冒充新剪輯技術。這版要改的是整支體驗：同一套跨行走與坐姿視點，兩套共同構成外出片刻；不再每套只有一段原地擺拍，也不靠換裝瞬間承擔全部內容。它是否足夠不同，仍須由成片判定。

人物不站好等待切鏡，攝影機不推拉，角色不走近退後。行走採斜正面保留臉與敞開翻領；坐姿保留棉T、腰部與褲子上下文。避免整理袖口、提包、開門等細小接觸，亦不把閱讀、喝咖啡當無資訊的填充。

## 銜接與製作成本

暫定四段3.75／3.25／3.25／4秒，三次0.75秒疊化，共12秒；這是製作預算。未被疊化覆蓋的觀看時間約3／1.75／1.75／3.25秒。保持原速、無字。音樂日後由IG另加，沒有從靜音樣本定BPM。

全身與坐姿中景仍有尺度風險。先畫出臉、翻領與腰部的視線位置，匹配窗光、姿勢方向與接點；不是預設0.75秒能解決。先驗第一套A1→A2連續觀看，失敗便重設視點，不能退回剛被否決的兩段固定全身。每鏡最多一次重試；4鏡產能成本須記錄，不先宣稱能達每支30–60分鐘。

## 起始圖需求與下一個具體動作

四鏡需按鏡頭起點準備畫面；不能把舊居中站姿勉強當走路來源。第一套先製作原生9:16全身行走起點A1，核准後才以它鎖定服裝與場景準備坐姿A2；第二套分開建立自己的服裝鎖。已核對M03approved face/full都存在，準確look IDs為2026-W41-004-L01／L02。新圖逐張視覺核准後才能送Grok。詳細角度、景別、動作起止、場景、服裝、風險與參照雜湊見storyboard_candidate.json。

既有W37／W41發布檔與Drive保持原狀；本案不是新週量產，也尚未完成full＋proof＋Carousel正式資產。下一步是第一套的新全身起始圖候選，而非再改M05 E02的動作或疊化。
'''
(OUT/'README.md').write_text(report,encoding='utf-8')
p=ROOT/'CURRENT_STATUS.md';s=p.read_text(encoding='utf-8');i=s.index('\n## ');s=s[:i]+'''\n## New reference pass and everyday walk/seated storyboard candidate — 2026-10-13

After E02 rejection and user「ok」, reviewed46 full-page muted autoplay samples of FUDGE DdavjIjThdp and20 of PAZZO DdYmOpBPfxs, spanning playback wraps. Actual observations: front/lateral everyday travel, lower-garment views and later seated rest in FUDGE; wall-side/seated/detail and stacked frames in PAZZO. Not precise cuts, audio, retention or verified performance. FUDGE is bicycle brand partnership; no copying bike/two-person/branding. Candidate M03「午休的小出走」uses W41-004-L01/L02, not W41-003:full walking A→seated layer view A→matched seated B→full departure B,12s planning budget/three0.75s dissolves/no text. Four-shot/full-medium order already used historically; proposed change is whole-film spatial/posture structure, not new technology. Full/seated scale switches remain comfort risk; first prove A1→A2, no reverting to rejected two-full layout. Approved M03 face/full exist, hashed. Saved `03_research/editorial_sequence_reset_2026-10-13/README.md`, `storyboard_candidate.json` and actual browser evidence. No new still/Grok/edit/Drive/IG mutation this reference/planning step. Next concrete production action:new native9:16 L01 walking-start candidate from this complete storyboard; user exact still approval before Grok. Candidate creative difference/whole-film acceptance and weekly production sustainability remain unvalidated.
''' +s[i:];p.write_text(s,encoding='utf-8')
print('Reference review and storyboard saved; approved M03 reference pair exists; no media generated.')
