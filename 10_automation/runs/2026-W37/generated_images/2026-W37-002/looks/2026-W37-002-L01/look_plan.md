# Mira Look Image Job

- carousel_id: `2026-W37-002`
- look_id: `2026-W37-002-L01`
- model_profile_id: `M05`
- theme: 短外層配長流動下身
- look_name: 白色短夾克配靛藍寬褲
- dressing_decision: 上身用腰骨長度的短外套，讓寬褲腰線與垂墜清楚可見
- clothing_item: 光學白無鋪棉短版薄斜紋夾克；淡藍短袖棉襯衫紮入腰頭；深靛藍高腰薄料長寬褲；黑色平底樂福鞋；焦糖棕小方包
- scene: 小型建築事務所的開放式樣品桌旁，側窗日光
- visible_action: 把一片材質樣板平放在桌角
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-002-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
