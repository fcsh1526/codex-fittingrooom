# Mira Look Image Job

- carousel_id: `2026-W46-004`
- look_id: `2026-W46-004-L01`
- model_profile_id: `M04`
- theme: 紫色靠近臉，怎麼搭才好讀？
- look_name: 莓紫淺V薄針織 × 淺石灰長褲
- dressing_decision: 亮色靠近臉時，領口留一線白並讓鞋包退到中性色
- clothing_item: 莓紫細針距棉混紡淺V長袖針織、薄白棉圓領T僅在V口露窄邊、淺石灰棉質直筒褲、黑平底皮鞋、灰褐小肩包、細銀耳環
- scene: 街角茶店側窗
- visible_action: 抬頭聽見店員叫號，笑著轉肩應聲
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W46-004-L01 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
