# Mira Look Image Job

- carousel_id: `2026-W35-003`
- look_id: `2026-W35-003-L02`
- model_profile_id: `M03`
- theme: 運動外層配裙裝
- look_name: 灰白拉鍊外套＋柔粉中長裙
- dressing_decision: 用灰白短版拉鍊外套壓低柔粉裙的甜度，鞋包改用黑色維持乾淨輪廓
- clothing_item: 灰白短版薄棉立領拉鍊外套；白色合身無袖上衣；柔霧粉高腰A字中長裙；黑色方頭平底鞋；黑色小型肩背包
- scene: 獨立電影院的明亮側廊與霧面玻璃窗
- visible_action: 沿側廊走向影廳時一手拿空白票券，另一手自然整理外套下擺
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-003-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
