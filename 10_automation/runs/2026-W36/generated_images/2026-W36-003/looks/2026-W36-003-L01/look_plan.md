# Mira Look Image Job

- carousel_id: `2026-W36-003`
- look_id: `2026-W36-003-L01`
- model_profile_id: `M01`
- theme: 麂皮質感小面積入秋
- look_name: 奶油白棉麻套裝＋焦糖麂皮腰帶
- dressing_decision: 奶油白棉麻上衣與長裙維持輕薄，只用一條焦糖麂皮腰帶增加秋季觸感
- clothing_item: 奶油白短袖棉麻開領上衣；奶油白高腰A字中長裙；焦糖棕窄版霧面麂皮腰帶；黑色薄底涼鞋；黑色小型光滑皮革手提包
- scene: 有遮棚的週末花市與柔和上午日光
- visible_action: 站在攤位旁挑選一小束花，一手拿花、另一手自然扶住手提包把手
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-003-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
