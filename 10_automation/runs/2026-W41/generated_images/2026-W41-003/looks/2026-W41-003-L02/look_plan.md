# Mira Look Image Job

- carousel_id: `2026-W41-003`
- look_id: `2026-W41-003-L02`
- model_profile_id: `M02`
- theme: 可可棕直筒丹寧
- look_name: 白短袖襯衫配可可棕丹寧
- dressing_decision: 用可可棕直筒丹寧配奶油白棉上衣，鞋包固定黑色。
- clothing_item: 白色棉質短袖尖領襯衫，整齊紮入；可可棕高腰直筒丹寧褲，無刷破、褲腳停在鞋面；黑色低跟便鞋；黑色小方肩包；黑色窄皮帶
- scene: 街角咖啡店外的遮蔭步道，灰米色牆面與石地；短距離移重心展示牛仔褲腰線與褲腳，兩套保留同一光向
- visible_action: 往前短跨一步後自然停住，褲腳與鞋子保持可見，手臂放鬆不插口袋
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W41-003-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
