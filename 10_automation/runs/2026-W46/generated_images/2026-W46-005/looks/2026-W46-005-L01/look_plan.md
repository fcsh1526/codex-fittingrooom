# Mira Look Image Job

- carousel_id: `2026-W46-005`
- look_id: `2026-W46-005-L01`
- model_profile_id: `M05`
- theme: 深底花卉放上身或裙擺？
- look_name: 暗莓花襯衫 × 石米直褲
- dressing_decision: 花在上身時用一整塊淺素色下身托住
- clothing_item: 黑底細莓紅花薄棉小尖領襯衫、石米色高腰直筒長褲、黑色圓頭平底鞋、黑小方肩包、細銀耳釘
- scene: 日光展場前廳
- visible_action: 看完牆上的展覽資訊，再望向等候的朋友
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-005-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
