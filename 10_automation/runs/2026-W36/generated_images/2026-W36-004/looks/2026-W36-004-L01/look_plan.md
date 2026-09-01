# Mira Look Image Job

- carousel_id: `2026-W36-004`
- look_id: `2026-W36-004-L01`
- model_profile_id: `M04`
- theme: 絲巾效果與緞面垂墜
- look_name: 香檳緞面裹身裙＋黑色針織背心
- dressing_decision: 黑色素面背心配香檳緞面裹身中長裙，讓光澤與斜向垂墜成為全身唯一主張
- clothing_item: 黑色合身方領細針織背心；香檳色高腰裹身緞面中長裙；黑色尖頭平底鞋；黑色小型硬挺手提包；細版金色耳環
- scene: 街區餐館入口的霧面玻璃與傍晚自然暖光
- visible_action: 把預約卡交給接待人員後往座位方向轉身，手提包自然垂在身側
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-004-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
