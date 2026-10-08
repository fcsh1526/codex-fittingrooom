# Mira Look Image Job

- carousel_id: `2026-W41-005`
- look_id: `2026-W41-005-L02`
- model_profile_id: `M04`
- theme: 亮色包款與首飾單點
- look_name: 白襯衫黑中長裙配鈷藍小包
- dressing_decision: 用一只鈷藍小肩包當唯一亮色，其餘服裝維持白、灰、黑。
- clothing_item: 白色短袖棉襯衫整齊紮入；黑色高腰小腿中長A字棉裙；黑色圓方頭平底便鞋；鈷藍霧面小肩包、短肩帶；小型銀色幾何耳針
- scene: 週末書店旁的淡灰門廊，背景少量木框且沒有彩色物；中性色背景讓鈷藍包成唯一亮色，兩套維持同一機位
- visible_action: 空手輕扶肩包短帶一次後放下，鈷藍包仍停在腰胯旁、不跨到衣服中央
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- carousel_variants: `A, B, C`
- required_surface_jobs: `reel, carousel`
- reel_plan: `A = native 9:16 full-person source`
- carousel_plan: `A = full-person Hero; B = scene application; C = accessory detail`
- status: `waiting_for_both_surface_jobs`

Run both surface jobs before marking the look asset-complete: `prepare_daily_image_job.py --look-id 2026-W41-005-L02 --surface reel`, then repeat with `--surface carousel`.
Each look receives its own accepted Hero lock; another look under the same theme may share the model, but not the Hero image.
