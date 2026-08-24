# Mira Look Image Job

- carousel_id: `2026-W35-002`
- look_id: `2026-W35-002-L01`
- model_profile_id: `M01`
- theme: 深棕麂皮觸感
- look_name: 白色短袖＋深靛丹寧＋深棕麂皮包
- dressing_decision: 把深棕麂皮只放在肩背包，讓白上衣與深靛丹寧維持八月的輕薄感
- clothing_item: 挺度適中的白色棉質圓領短袖；深靛藍高腰直筒薄丹寧褲；深棕皮革樂福鞋；巧克力棕中小型柔軟方形麂皮肩背包
- scene: 街區咖啡店窗邊外帶櫃檯與午後自然光
- visible_action: 接過外帶咖啡後把紙杯放到窗邊層板，另一手扶住麂皮包帶
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-002-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
