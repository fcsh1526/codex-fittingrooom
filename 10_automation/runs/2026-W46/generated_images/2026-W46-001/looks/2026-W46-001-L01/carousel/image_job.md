# W46 draft · Mira Daily Image Job

- carousel_id: `2026-W46-001`
- look_id: `2026-W46-001-L01`
- look_name: 黑丁字帶鞋 × 黑九分褲
- model_profile_id: `M01`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 九分褲要留多少鞋面？
- clothing_item: 米白短袖細針織圓領上衣紮入、炭黑九分直筒西裝褲、黑色霧面圓方頭丁字帶平底鞋、可可棕小型肩包、銀色小圈耳環
- occasion: 台北騎樓內側的咖啡店窗邊候位區
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- required_frames: Reel A+proof; Carousel A+B+C
- canva_template: `v3-D` / Mira Template Master v3 - D Cross-Boundary Full-Bleed
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W46\generated_images\2026-W46-001\looks\2026-W46-001-L01\carousel\codex_generation_handoff.md
```