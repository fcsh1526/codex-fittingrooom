# Mira Look Image Job

- carousel_id: `2026-W36-001`
- look_id: `2026-W36-001-L01`
- model_profile_id: `M05`
- theme: 輕薄機能疊穿
- look_name: 霧灰薄風衣＋橄欖綠背心洋裝
- dressing_decision: 無鋪棉薄風衣罩在完整的背心洋裝外，外套脫下後仍是一套可單穿的通勤造型
- clothing_item: 霧灰無鋪棉短版薄風衣；橄欖綠棉質背心襯衫洋裝；奶油白低跟包鞋；深灰小型尼龍肩背包；銀色細耳環
- scene: 辦公大樓外的開放式有棚步道與早晨自然反光
- visible_action: 沿有棚步道走向辦公大樓入口，一手自然整理敞開風衣前襟，另一手扶住肩背包帶
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W36-001-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
