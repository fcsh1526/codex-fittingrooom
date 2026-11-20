from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent;V=RUN/'editorial_reset_v3_2026-10-28'
O=V/'execution_4segments';O.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(R).as_posix()
feedback={'actor':'user','quote':'有','recorded_at':'2026-10-28','decision':'directional_improvement_confirmed','scope':'The proposed outfit contrast and viewing route are closer to the desired interest, replying to that exact question.','question':'看完一輪後，這次的換裝差異與觀看路線，有更接近你要的趣味嗎？','targets':[{'path':rel(V/'shared_route_previs_16s.gif'),'sha256':sha(V/'shared_route_previs_16s.gif')},{'path':rel(V/'connected_storyboard_v3.png'),'sha256':sha(V/'connected_storyboard_v3.png')}],'limits':'Does not say every garment/shot/technical setting is final, report continuous playback, resume new image/video generation explicitly or approve an ungenerated still/film/publication. Keep media hold while resolving executable source requirements.'}
dump(V/'user_direction_feedback_2026-10-28.json',feedback)
capability={'checked_date':'2026-10-28','url':'https://grok.com/imagine/agent/f040d332-48df-47c4-86d4-28e85c97d5b5?conversation=3f0241af-1184-4a74-9ced-b0b4715a1a95','method':'in-app browser, existing Mira canvas URL','observed_title':'請稍候...','observed_text':['正在執行安全驗證','此網站使用安全服務抵禦惡意機器人。當網站驗證並確認您不是機器人時，便會顯示此頁面。'],'status':'controls_not_visible_security_verification','current_duration_options':None,'current_first_last_keyframe_controls':None,'current_identity_inputs':None,'historical_evidence':'Prior October tests produced about6s raw clips and reported picture references plus first/keyframe support. Historical reports do not verify current controls.','actions':'Read only; no challenge interaction, upload, prompt submission or generation.','limits':'Cannot claim current6s/10s availability or precise camera-curve support from this blocked page.'}
dump(O/'capability_check_2026-10-28.json',capability)
old=read(V/'production_plan.json');space=copy.deepcopy(old['space']);samples=read(V/'projection_samples.json')
definitions=[('A',0,114,0,'紫外搭褲裝，斜前方走向側前方','new first still at global0, plus late composition guide at global114'),('B',96,198,0,'同套褲裝繼續走到柱後窗口','actual approved A source extract corresponding to global96; independent late guide global198'),('C',180,294,1,'柱前開始的同時間換裝窗口，揭開深藍洋裝','actual approved B source extract corresponding to global180; new dress replacement candidate must be visually approved before use'),('D',276,384,1,'同套洋裝延續靠近，讀白T與肩帶','actual approved C source extract corresponding to global276; late closer composition guide global384')]
plan=copy.deepcopy(old);plan['plan_id']='2026-W44-001-v3-4segment-execution-proposal';plan['status']='draft';plan['workflow_state']='direction_closer_controls_unverified_media_hold';plan['shots']=[];plan['transitions']=[];space['routes']=[]
cards=[]
for idx,(label,start,end,look,purpose,input_rule) in enumerate(definitions):
 sid='S0'+str(idx+1);ts=[start,(start+end)//2,end]
 route={'shot_id':sid,'character_samples':[],'camera_samples':[],'projected_samples':[]}
 for f in ts:
  a=samples[f]
  route['character_samples'].append({'frame':f,'position':a['character_position'],'heading_degrees':a['heading_degrees'],'gait_phase':'schematic sine phase only; actual native gait must be reviewed'})
  route['camera_samples'].append({'frame':f,'position':a['camera_position'],'target':a['target'],'vertical_fov_degrees':a['vertical_fov_degrees']})
  route['projected_samples'].append({'frame':f,'person_center_uv':a['person_center_uv'],'person_height_fraction':a['person_height_fraction'],'visible_landmark_ids':[],'visible_clothing':purpose})
 space['routes'].append(route)
 # Existing v3 GIF describes the same world and clock but not newly added source joins.
 # It cannot be re-labelled as an audited execution-join preview.
 shot={'id':sid,'look_ids':[plan['looks'][look]['id']],'frames':[start,end],'clothing_purpose':purpose,'clear_read_intervals':[],'storyboard_asset_id':'board','previs_asset_id':None,'overhead_asset_id':None,'input_asset_ids':[],'scene_reference_asset_ids':[],'space_mode':'shared_world','execution_note':input_rule}
 # Explicit clear windows exclude all three18f mixes and leave column margins.
 for interval in ([[0,96]],[[114,162]],[[216,276]],[[294,384]])[idx]:shot['clear_read_intervals'].append(interval)
 plan['shots'].append(shot)
 if idx:plan['transitions'].append({'from_shot':'S0'+str(idx),'to_shot':sid,'frames':[start,definitions[idx-1][2]],'overlap_frames':18,'method':'cross_dissolve','role':'wardrobe_change_behind_column' if idx==2 else 'same_outfit_continuity_join'})
 cards.append({'segment':label,'shot_id':sid,'look_id':plan['looks'][look]['id'],'global_frames':[start,end],'useful_frames':end-start,'useful_seconds':(end-start)/24,'candidate_generation_duration_seconds':6,'duration_status':'historical6s path only; current UI not verified','planned_source_interval':'[0,'+str(end-start)+') if valid at native24fps; otherwise reselect measured interval and update lineage','purpose':purpose,'source_input_rule':input_rule,'late_guide_global_frame':end,'late_guide_relative_seconds':(end-start)/24,'controls_limit':'Do not set a6s last frame and pretend it pins a4.25–4.75s selected endpoint. First/last/keyframe roles and actual timestamp rounding must be verified in current UI; no unsupported curve parameters.','acceptance':['actual raw duration/fps/size and selected interval recorded','identity, wardrobe, bag/hands, gait and fixed architecture individually stable','new source overlaps previous source over the same full18f world-time interval','source phase/scale/light/landmarks checked, then whole context at native speed','at most one bounded retry per necessary shot; preserve failure and classify cause'], 'status':'planning_only_not_submitted'})
plan['space']=space;plan['shared_space_asset_id']='common_space'
dump(O/'shared_space.json',space)
plan['assets']=[a for a in plan['assets'] if a['kind'] not in ['previs','overhead']]
for a in plan['assets']:
 if a['id']=='common_space':a['path']=rel(O/'shared_space.json');a['sha256']=sha(O/'shared_space.json')
plan['missing_assets']=['Current tool settings cannot be read until site security verification completes; no current duration/control claim','Added same-look joins [96,114) and [276,294) require their own preview/context review; original v3 GIF does not validate them','4-segment shared-space source and late/matching views not generated or approved','User confirmed direction is more interesting, not every technical split or new still','Raw clips, source lineage and native-speed shot/join/whole-film QA pending']
dump(O/'production_plan.json',plan);dump(O/'shot_cards.json',cards)
text='''# v3執行草案：保留16秒觀看路線，拆成四段來源

2026-10-28。使用者回「有」，確認換裝／觀看路線更接近期待。這是方向回饋，未推定新照片、技術拆鏡或整片發布核准。影像生成仍暫停。

## 已核對的工具狀態

原Mira Grok畫布停在「正在執行安全驗證」，尚未進入控制介面。此次沒有上傳或送生成。**目前可選片長、人物參照與首／尾／片內圖控制均未核實。** 過去6秒來源可作執行草案的基準，不能寫成今天已確認。

## 四段可用畫面的預算

|段|整片時間|可用原速長度|造型／作用|
|---|---|---|---|
|A|0–4.75秒|4.75秒|紫外搭褲裝，斜前方逐步到側前方|
|B|4–8.25秒|4.25秒|同套前進，接近柱與換裝窗口|
|C|7.5–12.25秒|4.75秒|洋裝從柱後揭露，延續同路線|
|D|11.5–16秒|4.5秒|同套洋裝繼續靠近，讀白T及肩帶|

來源使用長度合計18.25秒，減去三處各0.75秒交疊＝16秒。每段均短於歷史6秒來源，但仍須核對今天工具與下載後真正可用區間。原速、不循環、不凍結、不拉慢。

**代價是多了4–4.75秒與11.5–12.25秒兩處同套接點。** 原v3 GIF只有換裝的混合示意，沒有模擬這兩處實際來源差異；不能宣稱它們已柔順。必須在相同世界時間驗完整18幀的姿態、尺度、腳步、光線及背景，並看完整上下文。若工具能直接提供足夠長且穩定的來源，可保留原兩段方案減少接點，但不能在未見控制前承諾。

## 最少必要素材與製作次序

1. 先核對當前工具的時長與圖片控制。新世界的首張照片須依v3首鏡另做，現有照片只作身份／第一套服裝參考。
2. A先做一段有界試作；原片與預定0–4.75秒逐項核對，再決定能否沿用路線。不要先把四段全部送出。
3. B起點優先使用A實際對應整片4秒的核准來源畫格，保留來源／幀號／hash。既有畫格提取不偽造新照片核准。
4. C在整片7.5秒的實際接入畫格上建立第二套洋裝候選，保持場景與人像對位；新AI改衣圖仍須逐張視覺核准。不得把舊的原地換褲圖當接入圖。
5. D同套起點優先用C實際對應整片11.5秒的來源畫格。必要的晚段構圖指南只在當前控制確實能使用時才製作。
6. 每段來源、相鄰接點、整片原速觀看分別驗收。若第一段不能大致遵循路線，先修設計／控制，不連續追生後三段。

若介面不能在預定的4.25–4.75秒放置合適的片內指引，不可用6秒尾幀假裝選段終點被鎖定；先記錄可選值和取整偏差，再調整來源時序或簡化。曲線與世界座標是導演設計，不是目前已證明可傳入引擎的參數。

## 下一步

完成原畫布安全驗證後讀取實際選項，確認採兩長段或四短段，再導出必要首／晚／接點圖。此草案與四段計畫的預演閘門刻意保留缺口，未標成ready。沒有新照片、影片或發布。
'''
(O/'EXECUTION_REVIEW.md').write_text(text,encoding='utf-8')
heading='## W44 v3方向更接近期望；工具控制仍未核實 — 2026-10-28'
body='使用者對v3預演的換裝差異／觀看路線是否更有趣回「有」，記錄為方向改善確認；沒有擴成每個鏡頭／新圖／發布核准。精確問題、回覆與預演hash見editorial_reset_v3_2026-10-28/user_direction_feedback_2026-10-28.json。\n\n原Mira Grok畫布以IAB查核，停在「正在執行安全驗證」，未上傳或送生成，今天時長／圖片控制未知。已先備兩長段與四短段的執行選擇：四短段整片區間[0,114)、[96,198)、[180,294)、[276,384)，可用原速長度4.75／4.25／4.75／4.5秒，三次18幀柔接後16秒。這是依歷史6秒來源作的條件草案，不是今日可用功能確認；多出的兩處同套接點須另驗，不冒稱原GIF已模擬它們。\n\n執行單與來源／接點規則見 `10_automation/runs/2026-W44/editorial_reset_v3_2026-10-28/execution_4segments/EXECUTION_REVIEW.md`。四段計畫的預演／接點／控制證據維持缺失。下一步完成安全驗證後核對UI，再選兩段或四段並導出必要新圖；圖像生成維持暫停，原照片與歷史核准保留。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W44/publishing_structure.md']:
 p=R/name;t=p.read_text(encoding='utf-8-sig')
 if heading not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+heading+'\n\n'+body+'\n'+rest,encoding='utf-8')
dump(O/'STATUS.json',{'status':'direction_closer_controls_not_visible_media_hold','generation_allowed':False,'current_blocker':'Grok site security verification','readiness':'No current tool settings or actual source/join proof','next':'Read controls after user completes site verification; no blind generation'})
print(rel(O/'EXECUTION_REVIEW.md'))
