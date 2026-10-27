# Mira Look Image Job

- carousel_id: `2026-W37-005`
- look_id: `2026-W37-005-L01`
- model_profile_id: `M03`
- theme: 麂皮與皮革一件亮點
- look_name: 奶油白棉麻配焦糖麂皮包
- dressing_decision: 入秋先用麂皮小包，衣服保留薄棉麻
- clothing_item: 奶油白無袖棉麻襯衫；深咖啡高腰薄棉麻直筒褲；焦糖色短毛麂皮小肩包；黑色低跟樂福鞋；細銀耳環
- scene: 社區咖啡店外有遮蔭的長木椅旁
- visible_action: 一手扶著椅背準備坐下，肩包自然垂在腰側
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W37-005-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
