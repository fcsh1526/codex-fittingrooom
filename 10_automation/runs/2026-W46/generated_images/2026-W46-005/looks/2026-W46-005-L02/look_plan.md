# Mira Look Image Job

- carousel_id: `2026-W46-005`
- look_id: `2026-W46-005-L02`
- model_profile_id: `M05`
- theme: 深底花卉放上身或裙擺？
- look_name: 素米針織 × 暗花中長裙
- dressing_decision: 花在下身時，上衣以淺素色留出明暗分界
- clothing_item: 米白細針距短袖圓領上衣紮入、黑底暗莓紅花小腿中段A字裙、黑方頭平底鞋、深棕小肩包、銀耳釘
- scene: 展場休息區矮凳旁
- visible_action: 從矮凳起身，提包往同伴方向挪半步
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-005-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
