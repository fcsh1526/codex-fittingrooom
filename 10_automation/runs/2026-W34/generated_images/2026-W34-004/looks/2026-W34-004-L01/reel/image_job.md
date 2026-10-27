# Mira Daily Image Job

- carousel_id: `2026-W34-004`
- look_id: `2026-W34-004-L01`
- look_name: 黑色吊帶洋裝＋白色短袖
- model_profile_id: `M05`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 黑色吊帶洋裝日常疊穿
- clothing_item: 合身白色棉質圓領短袖；霧面黑色直身吊帶洋裝；黑色平底鞋；酒紅小型肩背包
- occasion: 日常外出／看電影
- frame_plan: hero+alternate_view
- required_frames: 2
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review Hero A only. Do not generate B/C before user acceptance.
B Alternate View and C Detail are optional production assets, not chronological action continuations or A/B tests; create them only when the publishing format needs them.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W34\generated_images\2026-W34-004\looks\2026-W34-004-L01\reel\codex_generation_handoff.md
```