# Mira Look Image Job

- carousel_id: `2026-W35-004`
- look_id: `2026-W35-004-L02`
- model_profile_id: `M02`
- theme: 窄領巾與蝴蝶結細節
- look_name: 奶油白無袖上衣＋酒紅窄領巾＋深棕長褲
- dressing_decision: 用酒紅窄領巾替奶油白上衣建立單一領口焦點，鞋包只做低調色彩呼應
- clothing_item: 奶油白合身無袖立領上衣；酒紅窄版絲巾在頸側打小單結並留短邊；深棕高腰直筒長褲；酒紅尖頭低跟鞋；深棕小型手提包
- scene: 街區餐館安靜候位區與傍晚窗邊暖冷混合光
- visible_action: 把紙本菜單放回入口層架後轉身走向座位，手提包自然垂在身側
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W35-004-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
