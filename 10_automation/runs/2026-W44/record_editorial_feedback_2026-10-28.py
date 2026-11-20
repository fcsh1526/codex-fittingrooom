from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[3];RUN=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
quote='稍等，我知道弱點在哪裡了。這週的企劃因為第一套起始圖，搭配線稿之後，發現我們這樣的呈現方式，1.衣服變換不明顯2.畫面還是不有趣3.預定的運鏡沒有之前長鏡頭的趣味'
receipt={'actor':'user','date':'2026-10-28','timezone':'Asia/Taipei','quote':quote,'decision':'editorial_direction_review_requested_generation_hold','scope':'Current W44 presentation approach, diagnosed from the first series stills plus storyboard. Review the weekly direction; do not infer rejection of every individual accepted still or all historical films.','issues':['Outfit change insufficiently visible','Visual experience uninteresting','Planned camera movement lacks the interest of the previous long-take approach'],'hold':'No further image/video generation while discussing this direction','prior_approvals':'L01 full/proof exact still approvals preserved; previous v2 planning approval retained historically, current execution superseded by this feedback','observed_plan_evidence':{'source':'planning/shared_space.json','person_x_center':0.5,'person_height_fraction_range_at_key_samples':[0.6105772785052521,0.6350433408976703],'interpretation':'Camera drawing has independent curves but the projected subject remains nearly centered and same-sized. This does not establish compelling long-take viewing.'},'assistant_diagnosis':'Same purple cardigan/white tee with only charcoal trousers changed to brown denim offers limited silhouette/bright-color contrast. Film lacks an unfolding visual event. Source-image-first execution and near-constant front view reduce movement interest. These are editorial interpretations, not measured audience performance.','next':'Discuss whole-film clothing contrast, spatial progression and projected camera experience before revising the board or requesting any new still. Do not automatically regenerate.'}
write(RUN/'user_editorial_feedback_2026-10-28.json',receipt)
p=RUN/'planning/series_01/production_plan.json';v=read(p);v['status']='editorial_revision_requested_generation_hold';v['latest_feedback_receipt']='10_automation/runs/2026-W44/user_editorial_feedback_2026-10-28.json';v['missing_assets'].append('Current user editorial direction review: outfit contrast, visual interest and long-take camera experience unresolved. Generation on hold.');write(p,v)
p=R/'04_prompts/material_pool/series_registry.json';v=read(p)
for s in v['series']:
 if s['series_id'].startswith('W44_PROPOSAL_'):
  s['status']='editorial_revision_requested_generation_hold' if s['series_id']=='W44_PROPOSAL_01' else 'weekly_presentation_review_generation_hold'
  s['latest_feedback_receipt']='10_automation/runs/2026-W44/user_editorial_feedback_2026-10-28.json'
write(p,v)
heading='## W44呈現方向需重審，停止新增影像 — 2026-10-28'
body='使用者指出：衣服變換不明顯、畫面不有趣、預定運鏡缺少先前長鏡頭趣味，並說「稍等」。精確回饋見 `10_automation/runs/2026-W44/user_editorial_feedback_2026-10-28.json`。當前W44呈現方向回到整片編輯討論，暫停新增AI照片／影片；不再追問第二套造型候選是否可用，也不直接換褲或補特效繼續製作。\n\n現有第一系列兩套同紫外搭／白T、僅灰褲換棕丹寧，輪廓差有限；共同預演的人物水平中心固定0.5、關鍵點高度約61–64%，畫框內角度／尺度發展不足。這是資料與編輯診斷，不是實際影片或受眾成效測試。下一步先討論整支片的服裝反差、沿路畫面發展及相機在實際畫框中的觀看經驗，再決定是否改系列／分鏡與缺圖。\n\nL01 full/proof逐張靜態核准與所有原始素材保留；本回饋不推定撤銷每張照片或舊片核准。其他四系列需跟隨本週方向重審，不自行宣稱已被逐支否決。此回饋取代下方繼續產圖／待L02核准的執行下一步。'
for name in ['CURRENT_STATUS.md','10_automation/MIRA_EDITORIAL_HANDOFF.md','10_automation/runs/2026-W44/publishing_structure.md']:
 p=R/name;t=p.read_text(encoding='utf-8-sig')
 if heading not in t:first,rest=t.split('\n',1);p.write_text(first+'\n\n'+heading+'\n\n'+body+'\n'+rest,encoding='utf-8')
print('Feedback recorded; no image or video generation.')
