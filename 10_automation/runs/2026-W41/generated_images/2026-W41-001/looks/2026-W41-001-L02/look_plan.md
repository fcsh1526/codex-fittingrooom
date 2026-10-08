# Mira Look Image Job

- carousel_id: `2026-W41-001`
- look_id: `2026-W41-001-L02`
- model_profile_id: `M05`
- theme: 短領口薄外套與俐落短比例
- look_name: 炭灰短外套配淺灰直筒褲
- dressing_decision: 選一件無鋪棉短版立領外套，搭短袖棉上衣和直筒褲，室內扣上、室外敞開。
- clothing_item: 炭灰短版無鋪棉立領外套，敞開；奶油白圓領棉短袖；淺灰高腰直筒斜紋長褲；黑色低跟樂福鞋；黑色小方肩包；窄黑皮帶
- scene: 社區辦公樓的明亮有頂入口，淺灰牆、短木長椅與完整地面；用於出門前整理可敞開薄外層，兩套沿用同一光向與拍攝位置
- visible_action: 空手在外套腰側前緣輕扶一下後自然放下，露出短袖與短衣長；包在另一側且不遮腰線
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W41-001-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
