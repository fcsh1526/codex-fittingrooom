# Mira Look Image Job

- carousel_id: `2026-W35-002`
- look_id: `2026-W35-002-L02`
- model_profile_id: `M01`
- theme: 深棕麂皮觸感
- look_name: 奶油白洋裝＋深棕麂皮低跟鞋
- dressing_decision: 用一雙深棕麂皮低跟鞋替薄棉洋裝增加換季觸感，其餘配件維持光滑材質
- clothing_item: 奶油白無袖薄棉直身中長洋裝；巧克力棕方頭麂皮低跟鞋；黑色小型光滑皮革肩背包；細版銀色耳環
- scene: 台北安靜選物店的木質展示桌與街窗自然光
- visible_action: 站在展示桌旁拿起一只小型陶杯查看，雙腳自然錯步並留下可信鞋底接觸影
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-002-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
