# Mira Look Image Job

- carousel_id: `2026-W36-005`
- look_id: `2026-W36-005-L01`
- model_profile_id: `M03`
- theme: 深紅色小面積亮點
- look_name: 炭灰針織上衣＋黑褲＋櫻桃紅小包
- dressing_decision: 炭灰上衣與黑色直筒褲維持安靜底色，只用一個櫻桃紅小包做日常可控制的亮點
- clothing_item: 炭灰合身短袖細針織上衣；黑色高腰窄直筒長褲；櫻桃紅小型光滑皮革腋下包；黑色方頭樂福鞋；銀色細耳環
- scene: 車站生活選品店的結帳區與傍晚窗光
- visible_action: 把收據折好收進櫻桃紅包包，另一手提著無標誌的小紙袋
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-005-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
