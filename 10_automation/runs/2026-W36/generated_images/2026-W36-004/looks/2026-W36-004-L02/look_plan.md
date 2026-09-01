# Mira Look Image Job

- carousel_id: `2026-W36-004`
- look_id: `2026-W36-004-L02`
- model_profile_id: `M04`
- theme: 絲巾效果與緞面垂墜
- look_name: 酒紅緞面斜裁裙＋奶油白短袖上衣
- dressing_decision: 奶油白短袖上衣配酒紅斜裁緞面中長裙，裙身有垂墜，其他單品不再增加光澤
- clothing_item: 奶油白合身短袖細針織上衣；酒紅高腰斜裁緞面中長裙；深棕方頭低跟鞋；深棕小型肩背包；小型金色耳釘
- scene: 藝文中心演出廳外的票務長廊與均勻室內光
- visible_action: 從自助取票機取出紙票後沿長廊走向入口，肩背包貼近身側
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-004-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
