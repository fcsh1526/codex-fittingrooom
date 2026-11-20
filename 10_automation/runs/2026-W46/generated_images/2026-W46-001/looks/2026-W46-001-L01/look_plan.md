# Mira Look Image Job

- carousel_id: `2026-W46-001`
- look_id: `2026-W46-001-L01`
- model_profile_id: `M01`
- theme: 九分褲要留多少鞋面？
- look_name: 黑丁字帶鞋 × 黑九分褲
- dressing_decision: 九分直褲留出腳背扣帶上方一段空隙
- clothing_item: 米白短袖細針織圓領上衣紮入、炭黑九分直筒西裝褲、黑色霧面圓方頭丁字帶平底鞋、可可棕小型肩包、銀色小圈耳環
- scene: 窗邊候位長椅前
- visible_action: 找到靠窗空位，稍轉肩笑著回應友人，再坐下
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-001-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
