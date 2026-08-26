# Mira Daily Image Job

- carousel_id: `2026-W35-003`
- look_id: `2026-W35-003-L02`
- look_name: 灰白拉鍊外套＋柔粉中長裙
- model_profile_id: `M03`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 運動外套配長裙
- clothing_item: 灰白短版薄棉立領拉鍊外套；白色合身無袖上衣；柔霧粉高腰A字中長裙；黑色方頭平底鞋；黑色小型肩背包
- occasion: 週末約會／看電影
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- required_frames: 3
- canva_template: `v3-B` / Mira Template Master v3 - B Cross-Boundary Symmetric
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-003\looks\2026-W35-003-L02\carousel\codex_generation_handoff.md
```