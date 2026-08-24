# Mira Daily Image Job

- carousel_id: `2026-W35-001`
- look_id: `2026-W35-001-L02`
- look_name: 米灰高領薄外套＋深灰直筒裙
- model_profile_id: `M05`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 輕量高領外套
- clothing_item: 米灰無裡短版高領薄外套；白色合身無袖棉質上衣；深灰高腰直筒中長裙；白色尖頭平底鞋；黑色小型手提包
- occasion: 看展／空調空間
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-001\looks\2026-W35-001-L02\carousel\codex_generation_handoff.md
```