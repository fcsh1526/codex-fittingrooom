# Mira Look Image Job

- carousel_id: `2026-W36-003`
- look_id: `2026-W36-003-L02`
- model_profile_id: `M01`
- theme: 麂皮質感小面積入秋
- look_name: 黑色棉麻洋裝＋焦糖麂皮扁包
- dressing_decision: 黑色棉麻洋裝保持透氣，焦糖麂皮只放在貼身的扁平肩背包，其他配件維持光滑材質
- clothing_item: 黑色無袖棉麻直身中長洋裝；焦糖棕扁平半月形麂皮肩背包；奶油白方頭平底鞋；銀色細耳環
- scene: 獨立書店的木質新書桌與街窗午後光
- visible_action: 從展示桌拿起一本薄雜誌翻看，麂皮包自然貼在身側且背帶受力可信
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-003-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
