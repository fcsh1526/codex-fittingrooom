# Mira Look Image Job

- carousel_id: `2026-W36-005`
- look_id: `2026-W36-005-L02`
- model_profile_id: `M03`
- theme: 深紅色小面積亮點
- look_name: 黑色襯衫洋裝＋酒紅低跟鞋
- dressing_decision: 黑色短袖襯衫洋裝維持單色，只用酒紅低跟鞋加入一個深紅亮點
- clothing_item: 黑色短袖棉質襯衫中長洋裝；酒紅尖頭低跟鞋；黑色小型光滑皮革肩背包；銀色細耳環
- scene: 小型劇場的明亮入口與深色海報牆
- visible_action: 拿著紙本票走向驗票口，雙腳自然錯步並留下可信的鞋底接觸影
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-005-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
