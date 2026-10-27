# Mira Look Image Job

- carousel_id: `2026-W37-004`
- look_id: `2026-W37-004-L01`
- model_profile_id: `M01`
- theme: 復古 T 字帶鞋日常化
- look_name: 白襯衫配酒紅T字帶鞋
- dressing_decision: 基本款配T字帶鞋時縮短褲長，露出腳背的T字結構
- clothing_item: 白色短袖棉府綢襯衫；深灰高腰及踝直筒褲；酒紅色低粗跟T字帶鞋，腳背中央直帶連接踝前橫帶、包頭；黑色小肩包；黑色窄皮帶
- scene: 城市街角烘焙店的開放式騎樓，上午側光
- visible_action: 站在窗口前把一個無字紙袋接到手中
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-004-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
