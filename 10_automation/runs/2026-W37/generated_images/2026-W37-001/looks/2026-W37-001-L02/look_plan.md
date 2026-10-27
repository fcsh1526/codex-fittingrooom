# Mira Look Image Job

- carousel_id: `2026-W37-001`
- look_id: `2026-W37-001-L02`
- model_profile_id: `M02`
- theme: 可拆式輕薄疊穿
- look_name: 霧藍薄襯衫配深藍洋裝
- dressing_decision: 以可脫襯衫調節室內外溫差，避免外套與內搭都厚重
- clothing_item: 霧藍無內裡亞麻混紡薄襯衫；深海軍藍方領寬肩帶中長洋裝；米白帆布便鞋；灰色帆布小托特包；銀色耳釘
- scene: 採光明亮的花藝工作坊，入口木桌放著素色花瓶
- visible_action: 一手拿起桌上一枝白色桔梗，另一手自然垂下
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-001-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
