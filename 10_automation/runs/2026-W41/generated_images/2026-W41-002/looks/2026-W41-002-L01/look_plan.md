# Mira Look Image Job

- carousel_id: `2026-W41-002`
- look_id: `2026-W41-002-L01`
- model_profile_id: `M01`
- theme: 格紋單品與素色留白
- look_name: 奶油白海軍藍格紋配炭灰褲
- dressing_decision: 讓薄格紋襯衫成為唯一圖案，搭深色直筒褲和素色配件。
- clothing_item: 奶油白海軍藍薄棉格紋襯衫，尖領、袖口翻一折、下襬整齊紮入；炭灰高腰直筒長褲；黑色低跟便鞋；黑色小方肩包；小型銀耳針
- scene: 書店外有頂人行入口，素米灰牆面與一小段木窗框；圖案衣服靠素背景及素色下身讀清，兩套沿用同一鏡位
- visible_action: 空手輕順已翻折的襯衫袖口後放下，保留格紋上衣與素色下身的完整關係
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W41-002-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
