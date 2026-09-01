# Mira Look Image Job

- carousel_id: `2026-W36-002`
- look_id: `2026-W36-002-L01`
- model_profile_id: `M02`
- theme: 短外套配長流動下身
- look_name: 深靛短夾克＋炭灰長寬褲
- dressing_decision: 深靛短夾克停在腰骨附近，配高腰炭灰長寬褲，讓寬鬆輪廓仍有清楚的長短分段
- clothing_item: 深靛藍短版薄棉斜紋夾克；光學白合身圓領短袖上衣；炭灰高腰薄西裝料長寬褲；黑色方頭平底鞋；黑色小型公事肩背包
- scene: 商務中心一樓共享等候區與大面窗自然光
- visible_action: 從文件架抽出一份薄資料後轉身走向電梯，肩背包貼近身側
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-002-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
