# Mira Look Image Job

- carousel_id: `2026-W46-004`
- look_id: `2026-W46-004-L02`
- model_profile_id: `M04`
- theme: 紫色靠近臉，怎麼搭才好讀？
- look_name: 霧紫薄開襟 × 炭灰長裙
- dressing_decision: 用開襟露出米白底，把其餘顏色收在炭灰與黑
- clothing_item: 霧紫細針距薄開襟衫敞開、米白短袖棉T、炭灰直身中長裙、黑方頭平底鞋、黑小提包、銀色小耳釘
- scene: 室內閱讀桌靠窗
- visible_action: 把讀完的書放回桌面後轉向窗
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-004-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
