# Mira Look Image Job

- carousel_id: `2026-W37-004`
- look_id: `2026-W37-004-L02`
- model_profile_id: `M01`
- theme: 復古 T 字帶鞋日常化
- look_name: 黑色中長裙配奶油白T字带鞋
- dressing_decision: 中長裙用單色簡潔剪裁，讓淺色T字帶鞋清楚呈現
- clothing_item: 黑色短袖棉質上衣；黑色高腰中長A字裙；奶油白方頭低粗跟T字帶鞋，腳背直帶連接橫帶；黑色小肩包；細銀耳釘
- scene: 街區小型畫廊的半戶外石階平台，柔和午後光
- visible_action: 平穩走向敞開的畫廊門口
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-004-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
