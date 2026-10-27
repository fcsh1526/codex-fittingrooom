# Mira Look Image Job

- carousel_id: `2026-W37-003`
- look_id: `2026-W37-003-L02`
- model_profile_id: `M04`
- theme: 柔軟材質配結構輪廓
- look_name: 挺版無袖上衣配垂墜長裙
- dressing_decision: 天熱時把結構放在薄上衣的立領，其餘用柔軟裙身平衡
- clothing_item: 米白無袖立領棉府綢上衣；墨藍高腰緞面中長直裙；黑色低跟尖方頭鞋；黑色小肩包；銀色耳釘
- scene: 設計書店的白牆展示桌區，大片玻璃窗側光
- visible_action: 一手輕翻展示桌上的無字圖像書
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-003-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
