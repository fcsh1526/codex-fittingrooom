# Mira Look Image Job

- carousel_id: `2026-W35-005`
- look_id: `2026-W35-005-L01`
- model_profile_id: `M04`
- theme: 深色直筒丹寧與柔和上衣
- look_name: 柔霧粉薄緞面上衣＋深靛直筒丹寧
- dressing_decision: 用一件柔霧薄緞面上衣與低跟鞋，把深靛直筒丹寧從週末感轉進通勤場合
- clothing_item: 柔霧粉短袖薄緞面垂墜上衣；深靛藍中高腰直筒薄丹寧褲；深棕方頭低跟鞋；深棕結構小型肩背包；細版銀色耳環
- scene: 採光設計工作室的簡報區入口與側窗自然光
- visible_action: 拿著平板電腦走向簡報桌，另一手自然穩住肩背包帶
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-005-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
