# Mira Look Image Job

- carousel_id: `2026-W46-002`
- look_id: `2026-W46-002-L02`
- model_profile_id: `M02`
- theme: 深靛牛仔褲，怎麼穿得像要上班？
- look_name: 週末白T × 同件深靛直筒
- dressing_decision: 保留原褲，用圓領和帆布鞋降低正式度
- clothing_item: 白色透氣短袖圓領T、同件深靛無刷破中高腰直筒丹寧九分長、灰白低筒帆布鞋、灰藍棉帆布托特包、銀色小耳釘
- scene: 週末雜貨店外的遮簷窗邊
- visible_action: 托住袋底，抬眼和店員微笑道謝
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-002-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
