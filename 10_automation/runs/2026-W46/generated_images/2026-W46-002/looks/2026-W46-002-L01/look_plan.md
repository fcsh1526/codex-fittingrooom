# Mira Look Image Job

- carousel_id: `2026-W46-002`
- look_id: `2026-W46-002-L01`
- model_profile_id: `M02`
- theme: 深靛牛仔褲，怎麼穿得像要上班？
- look_name: 通勤白襯衫 × 深靛直筒
- dressing_decision: 要俐落時保留硬挺白領與鞋面
- clothing_item: 白色挺薄棉小尖領長袖襯衫袖口折一折、深靛無刷破中高腰直筒丹寧九分長、黑皮便士樂福鞋、酒紅扁方肩包、銀色小耳釘
- scene: 共享工作室門邊
- visible_action: 看見同事推開門，抬眼微笑打招呼
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-002-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
