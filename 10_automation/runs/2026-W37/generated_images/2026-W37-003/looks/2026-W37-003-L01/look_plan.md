# Mira Look Image Job

- carousel_id: `2026-W37-003`
- look_id: `2026-W37-003-L01`
- model_profile_id: `M04`
- theme: 柔軟材質配結構輪廓
- look_name: 海軍藍肩線外套配緞面裙
- dressing_decision: 只用肩線明確的外套增加結構，洋裝保留柔軟垂墜
- clothing_item: 深海軍藍無內裡肩線清楚的輕薄外套；米白圓領無袖緞面中長洋裝；黑色低跟樂福鞋；黑色小腋下包；細銀耳環
- scene: 室內小型室內樂演出場地的側窗休息廳
- visible_action: 將一張素色無字節目冊放在窄桌上
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-003-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
