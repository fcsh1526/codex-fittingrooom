# Mira Look Image Job

- carousel_id: `2026-W36-002`
- look_id: `2026-W36-002-L02`
- model_profile_id: `M02`
- theme: 短外套配長流動下身
- look_name: 淺灰短版西裝外套＋深藍長寬褲
- dressing_decision: 淺灰無內裡短版西裝外套配深藍高腰長寬褲，讓正式感來自剪裁而不是厚重布料
- clothing_item: 淺灰無內裡短版單釦西裝外套；奶油白合身無袖針織上衣；深海軍藍高腰長寬褲；深棕尖頭低跟鞋；深棕窄版手提包
- scene: 採光明亮的工作室簡報區與白牆走廊
- visible_action: 抱著平板電腦走向簡報桌，另一手短暫扶住手提包把手
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-002-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
