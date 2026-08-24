# Mira Look Image Job

- carousel_id: `2026-W35-005`
- look_id: `2026-W35-005-L02`
- model_profile_id: `M04`
- theme: 深色直筒丹寧與柔和上衣
- look_name: 淡紫灰垂墜上衣＋深藍直筒丹寧
- dressing_decision: 用淡紫灰垂墜上衣與結構包平衡深藍直筒丹寧，保留週末也能穿的俐落感
- clothing_item: 淡紫灰短袖嫘縈垂墜上衣；深藍中高腰直筒薄丹寧褲；奶油白尖頭平底鞋；酒紅小型結構手提包
- scene: 藝文園區的書店咖啡入口與柔和午後光
- visible_action: 從展示架拿起一本薄型展覽手冊，另一手提著結構包自然垂落
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-005-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
