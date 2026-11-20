from pathlib import Path
import json,hashlib,copy
from PIL import Image
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;O=RUN/'editorial_reset_v3_2026-10-28'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(R).as_posix()
stats=read(O/'projection_checks.json');space=read(O/'shared_space.json')
looks=[{'id':'2026-W44-001-R3-L01','model_id':'M02','wardrobe_summary':'皇家紫薄V領開襟衫＋白圓領短袖T＋炭灰高腰直筒褲＋白灰低筒鞋＋黑小肩包＋細銀耳環','source_asset_ids':['source_W44']},{'id':'2026-W44-001-R3-L02','model_id':'M02','wardrobe_summary':'白圓領短袖T內搭深藍不透霧面細肩帶及小腿直身洋裝＋白灰低筒鞋＋深棕小肩包＋細銀耳環；不穿紫外搭','source_asset_ids':['source_W44']}]
plan=read(R/'11_skills/mira-reel-director/assets/production_plan.template.json')
plan.update({'plan_id':'2026-W44-001-editorial-reset-v3','status':'proposed_user_review_required_generation_hold','path_base':'project','weeks':{'source':['2026-W44'],'content':'2026-W44','delivery':None},'editorial':{'audience':'台灣成年女性工作日／週末的日常穿搭靈感','takeaway':'同一段出門路線，看紫色外搭褲裝的俐落輪廓，轉成白T內搭深藍洋裝的輕鬆裙裝輪廓。','visual_theme':'走過街角，換一種出門狀態','selection_rationale':'回應衣服變換不明顯、畫面不有趣、缺少長鏡頭趣味；先讓服裝輪廓、空間揭露與相機視角一起發展。'},'presentation':{'layout_id':'single_sequential','recipe_id':'continuous_route'},'models':[{'id':'M02','identity_asset_ids':['M02_face','M02_full']}],'looks':looks,'film':{'fps':24,'frame_count':384,'duration_seconds':16,'aspect_ratio':'9:16','native_speed':True,'baked_text':False},'space':space,'shared_space_asset_id':'common_space','missing_assets':['新主題、第二套裙裝與本v3分鏡／共同預演尚待使用者確認；前次ok只授權重想企劃','兩段來源需各有8.25及8.5秒原速可用區間；現行工具可選時長／參照控制未核對，若僅6秒則本計畫不能直接執行','新場地與雙路徑未校準到現有照片；現有已核准照片只作人物／第一套服裝參考，不直接當新片首幀','所有符合新時間／構圖的起始及必要接點圖未生成／未逐張核准','原始影片、18幀換裝窗口與整片原速舒服度均未驗證；示意同位混合不證明AI影片無雙影','只重設第一支提案，其他四系列仍待此方向定案後重新協調；正式每人兩套契約保持']})
paths=[('common_space','space_plan',O/'shared_space.json'),('board','storyboard',O/'connected_storyboard_v3.png'),('previs','previs',O/'shared_route_previs_16s.gif'),('overhead','overhead',O/'shared_route_previs_16s.gif'),('source_W44','source',RUN/'source_perplexity.csv'),('M02_face','identity',R/'02_brand/reference_models/M02_start_v3_face.png'),('M02_full','identity',R/'02_brand/reference_models/M02_start_v3_full.png')]
plan['assets']=[]
for aid,kind,p in paths:
 a={'id':aid,'kind':kind,'path':rel(p),'sha256':sha(p)}
 if kind in ['previs','overhead']:a['derived_from']={'asset_id':'common_space','sha256':sha(O/'shared_space.json')}
 plan['assets'].append(a)
plan['shots']=[{'id':'S01','look_ids':[looks[0]['id']],'frames':[0,198],'clothing_purpose':'前段讀紫外搭、白T、直筒褲及鞋；相機從斜前方轉向側前方，柱與開闊處逐步進入畫面','clear_read_intervals':[[0,162]],'storyboard_asset_id':'board','previs_asset_id':'previs','overhead_asset_id':'overhead','input_asset_ids':[],'scene_reference_asset_ids':['common_space'],'space_mode':'shared_world','action_start':'沿騎樓自然前進，服裝全貌可讀','action_end':'經過固定前景柱、仍沿同一時間路線前進','camera':'獨立曲線＋同時間朝向；固定40度垂直FOV，非鏡頭變焦'},{'id':'S02','look_ids':[looks[1]['id']],'frames':[180,384],'clothing_purpose':'同一段柱前重疊後揭開深藍洋裝，先讀完整裙裝，再在後段靠近讀白T領口與肩帶','clear_read_intervals':[[216,384]],'storyboard_asset_id':'board','previs_asset_id':'previs','overhead_asset_id':'overhead','input_asset_ids':[],'scene_reference_asset_ids':['common_space'],'space_mode':'shared_world','action_start':'與S01同世界時間及位置，在柱前窗口換套','action_end':'進入較開闊處，鏡頭靠近到含臉中景，腳離框是預先設計','camera':'獨立時間曲線延續，後段接近；不把後製裁腳當作運鏡'}]
plan['transitions']=[{'from_shot':'S01','to_shot':'S02','frames':[180,198],'overlap_frames':18,'method':'cross_dissolve','note':'既有0.75秒比較基準，安排在前景柱通過窗口；未改為硬切／延長疊化，不宣稱生成後自然舒適。'}]
plan['workflow_state']=plan['status'];plan['status']='draft'
for shot in plan['shots']:shot['scene_reference_asset_ids']=[]
dump(O/'production_plan.json',plan)
dump(O/'planning_authorization_2026-10-28.json',{'actor':'user','quote':'ok','recorded_at':'2026-10-28','scope':'Proceed with reconsidering clothing contrast, whole-film spatial progression and projected camera experience after feedback; keep AI image/video generation on hold','context':'Reply to the diagnosis that whole-film design must precede new starting images','limits':'Not approval of this newly proposed dress look, scene, curves, storyboard or final film.'})
doc='''# Mira W44 整片改案 v3：走過街角，換一種出門狀態

2026-10-28。**待審提案，只做線稿／幾何預演；照片與影片生成維持暫停。**

## 觀眾要看什麼

一位女性走過同一段街角，從工作日的紫色外搭褲裝，轉為週末白T內搭深藍洋裝。看點是兩種出門狀態、明顯的褲裙輪廓與層次差，以及跟著她走出騎樓的畫面發展。前景柱提供換段的空間依據；不是再用特效補一組差異很小的衣服。

這是第一支的改案，**不再以「同件紫色外搭一件多搭」作主題**。第二套為本次提出的新搭配，尚未核准；也不把改案自動套給其他四支或改變五位各兩套的週產規格。

## 兩套造型與來源

- 工作日：皇家紫薄V領開襟衫、白圓領短袖T、炭灰高腰直筒褲、白灰低筒鞋、黑小肩包、細銀耳環。W44-P001；已有照片可參考人物與衣服，構圖／場地不直接沿用。
- 週末：白圓領短袖T內搭深藍不透霧面細肩帶及小腿直身洋裝、白灰低筒鞋、深棕小肩包、細銀耳環。W44-P006；裙裝、露出的白袖口與肩帶層次屬編輯搭配提案，不是生成商品的功能證明。

色塊由「紫／白／灰」轉成「白／深藍」，長袖外層轉成短袖內搭，兩條褲腿轉為連續裙身。棕丹寧候選保留歷史，本案不繼續補它。

## 16秒觀看走向

|時間|畫面發展|衣服資訊／相機用途|
|---|---|---|
|0–3秒|斜前方完整褲裝，人物前進、相機逐步移向側前方|先認出紫外搭與長褲；保持頭鞋可讀|
|3–6.75秒|人物持續走，柱與建築邊緣逐步進入畫框|角度變化用來讀輪廓，近柱與遠景形成視差|
|7.5–8.25秒|固定前景柱通過，保留0.75秒柔接窗口|兩來源描述同一段世界時間；示意對位不等於實片無雙影|
|9–13秒左右|柱後揭開洋裝，沿路進入開闊處|讓白T、肩帶、連續裙身和鞋有完整觀看時間|
|最後約2–3秒|相機與人物距離縮短，結尾讀領口／肩帶|腳離框是預定景別變化；先前完整造型仍須成立|

162–180及198–216幀留作柱前／柱後餘裕，不計清楚讀衣。關鍵點與過渡要以實際預演畫面判斷，不以表格宣稱其已好看。

## 這次怎麼檢查運鏡

人物與攝影機使用獨立曲線、共同場地和整片時鐘。人物按曲線弧長前進，不在換套時重新起步；攝影機有自己的平滑時間曲線，垂直FOV保持40度，後段靠近來自相對位置改變。

投影可見人物在畫框的位置、大小和相對角度發展，旁邊俯視圖使用同一份資料。**這些只是示意設計，不是精密場地測量、動作物理或Grok控制保證。** 混合窗口由同位簡化人形顯示衣服切換，不能用它宣稱實際生成來源已對齊或疊影舒適。

請先看 `shared_route_previs_16s.gif` 的完整16秒，再看 `connected_storyboard_v3.png`。已逐張檢查關鍵視角與數值邊界；助手未以原速連續播放完成審美驗收。GIF為8fps規劃示意，正式時間設計為24fps／384幀。

## 執行前仍要解決的限制

兩個來源需提供8.25與8.5秒可用原速片段，扣0.75秒交疊後才有16秒。**目前尚未核對介面是否支援此時長與控制；若仍只有6秒，此版不能直接生成。** 應先核對能力，再縮短或拆鏡並回到同一時序預演，不能以慢放、循環或凍結湊長。

現有已核准照片的建築、比例和光線與新示意場地不相同，保留為人物／衣服參考，不當作新片首幀。改案確認後才導出最少必要首／中／末圖和重疊窗口，逐張照片核准，再逐鏡、相鄰接點及整片驗收。這輪沒有生成新AI照片／影片、沒有改動已接受照片或發布包。

## 這一輪的確認範圍

先確認：褲裝→洋裝的風格差異是否值得看；柱前到柱後是否有畫面發展；相機角度與接近是否比原先置中跟拍有趣。若這三點仍不成立，繼續改影片設計，不先產圖。
'''
(O/'REVIEW.md').write_text(doc,encoding='utf-8')
html='''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>Mira W44 v3 整片改案</title><style>body{background:#f3efe6;color:#293944;font:18px "Microsoft JhengHei",sans-serif;max-width:1100px;margin:40px auto;padding:20px}p{line-height:1.8}img{max-width:100%;height:auto}a{color:#22677c}.note{background:#fff;padding:20px;border-radius:12px}</style><h1>走過街角，換一種出門狀態</h1><p>W44整片改案v3 · M02一人兩套 · 待審，未生成照片或影片</p><div class="note"><p>紫色外搭＋俐落褲裝 → 白短袖內搭深藍細肩帶洋裝。人物沿路走，鏡頭從斜前方經側前方、前景柱，再逐步接近；先看完整16秒。</p><p>下方為同場地／時鐘的雙路徑與相機投影，簡化人形不代表身份或實際步態。0.75秒仍是柔接基準，實片舒服度尚未驗證。</p></div><p><img src="shared_route_previs_16s.gif" alt="16秒同步雙路徑與相機視角示意預演"></p><h2>連貫分鏡</h2><img src="connected_storyboard_v3.png" alt="八個關鍵視角"><p><a href="REVIEW.md">完整提案、兩套服裝、時序與執行缺口</a></p><p>目前需要8.25與8.5秒原速來源；工具時長／控制尚未核對，若僅6秒，不能直接執行。既有照片只作身份／服裝參考。改案確認前不生成新圖。</p></html>'''
(O/'review.html').write_text(html,encoding='utf-8')
gif=Image.open(O/'shared_route_previs_16s.gif');duration=0
for i in range(gif.n_frames):gif.seek(i);duration+=gif.info.get('duration',0)
dump(O/'render_receipt.json',{'date':'2026-10-28','status':'new_proposal_pending_user_review','common_space_sha256':sha(O/'shared_space.json'),'storyboard_sha256':sha(O/'connected_storyboard_v3.png'),'previs_sha256':sha(O/'shared_route_previs_16s.gif'),'gif_frames':gif.n_frames,'actual_gif_duration_ms':duration,'projection_checks':stats,'implementation':'Perspective pinhole with triangle per-pixel depth buffer; earlier polygon-average occlusion bug found and repaired before review export. Line/garment diagrams only, no raster photoreal image generation.','visual_review':'Key-frame contact sheet and column-window close view inspected; no continuous normal-speed human playback claim','approvals':[],'ai_still_generation_calls':0,'ai_video_generation_calls':0,'limits':'Unmeasured fictional scene, schematic avatar/sine gait, no cloth physics, tool adherence or final comfort validation.'})
heading='## W44整片改案v3待審：褲裝轉洋裝、柱前後與獨立曲線 — 2026-10-28'
body='使用者對回到整片設計回覆「ok」，授權企劃／分鏡重想，沒有恢復AI照片／影片生成。新提案存 `10_automation/runs/2026-W44/editorial_reset_v3_2026-10-28/REVIEW.md`，同步16秒示意GIF與八格分鏡同資料夾。只重設第一支M02：紫外搭白T灰褲→白T內搭深藍細肩帶中長洋裝；新主題「走過街角，換一種出門狀態」。第二套、前景柱與新共同場地／曲線皆為待審，不能沿用舊企劃核准。\n\n兩路徑共用場地與時鐘，人物弧長行進，相機獨立時間曲線、固定40度VFOV；從斜前方／側前方，經前景柱7.5–8.25秒柔接窗口，再接近。投影位置／尺度／角度變化與靜態頭鞋邊界有數值檢查，深度遮擋錯誤已修；這是幾何與關鍵圖檢查，不是實際影片／精密相機／物理步態／舒適度或完整原速目視通過。\n\n16秒設計需兩來源各8.25與8.5秒可用原速；工具介面能力尚未核對，若只有6秒不可直接執行，須先調時序／拆鏡再重預演。現有照片保留為人物／衣服參考，不因省圖綁住新場地或直接當新首幀。正式五位各兩套契約保持；其他四支尚待首支方向確認後協調。下一步審本v3整片的服裝反差、空間發展與相機觀看趣味，未自動產圖／動態／外部發布。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W44/publishing_structure.md']:
 p=R/name;t=p.read_text(encoding='utf-8-sig')
 if heading not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+heading+'\n\n'+body+'\n'+rest,encoding='utf-8')
dump(O/'STATUS.json',{'status':'proposed_user_review_required_generation_hold','review':'review.html','plan':'production_plan.json','previous_feedback':'../user_editorial_feedback_2026-10-28.json','generation_allowed':False})
print(json.dumps({'gif_duration_ms':duration,'gif_frames':gif.n_frames,'proposal':rel(O/'REVIEW.md'),'ready_for_generation':False}))
