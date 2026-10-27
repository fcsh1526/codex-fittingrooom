# Mira Daily Image Job

- carousel_id: `2026-W37-003`
- look_id: `2026-W37-003-L01`
- look_name: 海軍藍肩線外套配緞面裙
- model_profile_id: `M04`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 柔軟材質配結構輪廓
- clothing_item: 深海軍藍無內裡肩線清楚的輕薄外套；米白圓領無袖緞面中長洋裝；黑色低跟樂福鞋；黑色小腋下包；細銀耳環
- occasion: 藝文活動／書店
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W37\generated_images\2026-W37-003\looks\2026-W37-003-L01\carousel\codex_generation_handoff.md
```