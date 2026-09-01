# Mira Look Image Job

- carousel_id: `2026-W36-001`
- look_id: `2026-W36-001-L02`
- model_profile_id: `M05`
- theme: 輕薄機能疊穿
- look_name: 奶油白薄風衣＋霧藍背心洋裝
- dressing_decision: 可收納的奶油白薄風衣配霧藍背心洋裝，外層有防風結構但不增加厚度
- clothing_item: 奶油白可收納連帽薄風衣；霧藍細肩帶方領棉質中長洋裝；炭灰薄底芭蕾平底鞋；橄欖綠小型托特包
- scene: 社區超市外的半戶外購物廊與午後柔光
- visible_action: 離開冷氣區時一手把折好的購物清單收進托特包，另一手自然拉住風衣拉鍊頭
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-001-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
