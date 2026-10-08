# Mira Look Image Job

- carousel_id: `2026-W41-004`
- look_id: `2026-W41-004-L01`
- model_profile_id: `M03`
- theme: 放鬆剪裁與輕薄西裝
- look_name: 米白西外配白T深藍褲
- dressing_decision: 用無鋪棉輕薄西外搭棉質短袖上衣和直筒褲，保留一件正式外層即可。
- clothing_item: 米白無鋪棉輕薄單排扣西裝外套，敞開、袖口翻一折；白色圓領棉短袖紮入；深藍高腰直筒長褲；黑色低跟便鞋；深棕肩背包；小型銀耳針
- scene: 辦公區午餐店旁的安靜有頂走道，米灰牆與一張簡單長椅；西外配棉T能連接上班與午餐，兩套同機位同光向
- visible_action: 空手輕順已翻折的西外袖口後放下，外套敞開，棉T圓領全程可見
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W41-004-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
