# Mira Daily Image Job

- carousel_id: `2026-W35-005`
- look_id: `2026-W35-005-L02`
- look_name: 淡紫灰垂墜上衣＋深藍直筒丹寧
- model_profile_id: `M04`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深色直筒丹寧與柔和上衣
- clothing_item: 淡紫灰短袖嫘縈垂墜上衣；深藍中高腰直筒薄丹寧褲；奶油白尖頭平底鞋；酒紅小型結構手提包
- occasion: 週末午餐／展覽
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-005\looks\2026-W35-005-L02\carousel\codex_generation_handoff.md
```