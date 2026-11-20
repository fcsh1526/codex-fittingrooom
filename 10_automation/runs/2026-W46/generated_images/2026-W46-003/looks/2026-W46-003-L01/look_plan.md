# Mira Look Image Job

- carousel_id: `2026-W46-003`
- look_id: `2026-W46-003-L01`
- model_profile_id: `M03`
- theme: 方巾繫腰還是包把？
- look_name: 腰側方巾 × 紮入式上衣
- dressing_decision: 上衣紮起，方巾只佔一個腰側位置
- clothing_item: 米白棉短袖小翻領上衣紮入、深海軍藍高腰薄棉直筒長褲、酒紅米白印花絲質方巾穿左前褲耳打短側結、黑低跟便士鞋、深棕小提包、金色小耳環
- scene: 市集花材攤外緣
- visible_action: 用右手提包、往左側看攤位招牌
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-003-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
