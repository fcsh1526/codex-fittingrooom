# Mira Look Image Job

- carousel_id: `2026-W35-003`
- look_id: `2026-W35-003-L01`
- model_profile_id: `M03`
- theme: 運動外層配裙裝
- look_name: 海軍藍運動薄外套＋深灰直筒裙
- dressing_decision: 用一件短版輕量運動外層降低直筒中長裙的正式感，運動語彙只留在外套
- clothing_item: 深海軍藍短版立領薄尼龍運動外套；灰白合身棉質短袖；深灰高腰直筒中長裙；白色低調平底球鞋；黑色小型肩背包
- scene: 辦公街區有棚人行道與午間自然反光
- visible_action: 走出便利商店時一手拿無標誌紙袋，另一手把肩背包帶往肩上推回
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-003-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
