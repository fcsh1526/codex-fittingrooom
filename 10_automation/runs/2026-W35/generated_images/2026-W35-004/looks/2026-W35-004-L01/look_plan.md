# Mira Look Image Job

- carousel_id: `2026-W35-004`
- look_id: `2026-W35-004-L01`
- model_profile_id: `M02`
- theme: 窄領巾與蝴蝶結細節
- look_name: 白襯衫＋黑白窄領巾＋深藍直筒褲
- dressing_decision: 在白襯衫鎖骨下方打一個黑白窄領巾小結，胸前不再增加項鍊
- clothing_item: 白色自然合身純棉襯衫；黑白細窄絲巾在鎖骨下方打小蝴蝶結；深海軍藍高腰直筒西裝褲；黑色尖頭平底鞋；黑色小型肩背包
- scene: 共享辦公室的玻璃會議室入口與均勻日光
- visible_action: 抱著一份薄文件走出會議室，另一手輕扶門把，領巾結保持完整可見
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-004-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
