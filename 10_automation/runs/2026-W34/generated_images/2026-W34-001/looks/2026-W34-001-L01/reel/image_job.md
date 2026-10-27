# Mira Daily Image Job

- carousel_id: `2026-W34-001`
- look_id: `2026-W34-001-L01`
- look_name: 海軍藍牛津襯衫＋淺藍牛仔褲
- model_profile_id: `M03`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 寬版牛津襯衫日常穿法
- clothing_item: 海軍藍寬版純棉牛津襯衫；淺藍高腰直筒牛仔褲；白色帆布鞋；深棕帆布側背包
- occasion: 通勤／日常外出
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W34\generated_images\2026-W34-001\looks\2026-W34-001-L01\reel\codex_generation_handoff.md
```