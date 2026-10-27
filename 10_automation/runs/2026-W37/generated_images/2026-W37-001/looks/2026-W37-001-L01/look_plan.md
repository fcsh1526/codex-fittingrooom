# Mira Look Image Job

- carousel_id: `2026-W37-001`
- look_id: `2026-W37-001-L01`
- model_profile_id: `M02`
- theme: 可拆式輕薄疊穿
- look_name: 霧灰薄襯衫配奶油白洋裝
- dressing_decision: 冷氣房用可脫薄襯衫罩住肩臂，洋裝本身可以單穿
- clothing_item: 霧灰無內裡棉質薄襯衫；奶油白不透膚細肩帶小腿中長洋裝；白色低筒帆布鞋；深海軍藍小肩包；細銀耳環
- scene: 有大片側窗的社區圖書館入口閱讀區，木書架與石磨地板
- visible_action: 站在還書桌旁把一本無字素封面書放到桌上
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-001-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
