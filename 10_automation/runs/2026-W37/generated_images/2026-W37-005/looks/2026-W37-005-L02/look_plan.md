# Mira Look Image Job

- carousel_id: `2026-W37-005`
- look_id: `2026-W37-005-L02`
- model_profile_id: `M03`
- theme: 麂皮與皮革一件亮點
- look_name: 淺藍襯衫裙配巧克力麂皮包
- dressing_decision: 薄襯衫裙搭一個深棕麂皮包，以小面積換材質
- clothing_item: 淺藍短袖棉質襯衫中長洋裝，配同布腰帶；巧克力棕短毛麂皮小肩包；黑色平底包鞋；銀色耳釘
- scene: 河岸附近的獨立雜貨店門廊，明亮漫射日光
- visible_action: 一手提起桌上的素色陶杯查看杯形
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-005-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
