# Mira Look Image Job

- carousel_id: `2026-W35-001`
- look_id: `2026-W35-001-L02`
- model_profile_id: `M05`
- theme: 輕量高領外套
- look_name: 米灰高領薄外套＋深灰直筒裙
- dressing_decision: 用短版無裡高領外套平衡直筒中長裙，室內外切換時不增加厚重感
- clothing_item: 米灰無裡短版高領薄外套；白色合身無袖棉質上衣；深灰高腰直筒中長裙；白色尖頭平底鞋；黑色小型手提包
- scene: 當代美術館明亮入口與混凝土票務區
- visible_action: 從自助取票機抽出紙票後轉身走向展場，手提包貼近身側
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-001-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
