# Mira Look Image Job

- carousel_id: `2026-W46-003`
- look_id: `2026-W46-003-L02`
- model_profile_id: `M03`
- theme: 方巾繫腰還是包把？
- look_name: 包把方巾 × 放下衣襬
- dressing_decision: 上衣不紮時，把同一條方巾移到包上
- clothing_item: 石灰米棉質短袖長襯衫自然垂至臀上、淺卡其直筒長褲、黑低跟便士鞋、深棕小提包外側把手繫同條酒紅米白方巾、金色小耳環
- scene: 市集紙品攤外緣
- visible_action: 把提包放在櫃面外緣方便拿卡片
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-003-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
