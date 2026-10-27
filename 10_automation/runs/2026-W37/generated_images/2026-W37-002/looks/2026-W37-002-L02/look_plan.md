# Mira Look Image Job

- carousel_id: `2026-W37-002`
- look_id: `2026-W37-002-L02`
- model_profile_id: `M05`
- theme: 短外層配長流動下身
- look_name: 沙色短外套配霧灰寬褲
- dressing_decision: 寬褲配短外套時讓腰頭露出，避免上下兩件都蓋住腰線
- clothing_item: 沙色腰骨長度薄棉短夾克；白色圓領短袖上衣紮入腰頭；霧灰高腰薄料長寬褲；深棕低跟包鞋；黑色小肩包
- scene: 陶藝展館的明亮入口展廊，石質展台與開放門廊
- visible_action: 一手輕推開展廊的木門
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-002-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
