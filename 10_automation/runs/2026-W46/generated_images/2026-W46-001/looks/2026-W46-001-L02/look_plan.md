# Mira Look Image Job

- carousel_id: `2026-W46-001`
- look_id: `2026-W46-001-L02`
- model_profile_id: `M01`
- theme: 九分褲要留多少鞋面？
- look_name: 酒紅丁字帶鞋 × 米白中長裙
- dressing_decision: 中長裙選小腿中段，讓鞋獨立成一個色點
- clothing_item: 深灰藍棉質短袖、米白棉斜紋小腿中段A字裙、暗酒紅圓方頭丁字帶平底鞋、深灰小肩包、銀色小耳釘
- scene: 自然光書店窗邊
- visible_action: 將選好的書放在窗沿並側身看封面
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-001-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
