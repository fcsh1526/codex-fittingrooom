# Mira Daily Image Job

- carousel_id: `2026-W35-002`
- look_id: `2026-W35-002-L01`
- look_name: 白色短袖＋深靛丹寧＋深棕麂皮包
- model_profile_id: `M01`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 深棕麂皮觸感
- clothing_item: 挺度適中的白色棉質圓領短袖；深靛藍高腰直筒薄丹寧褲；深棕皮革樂福鞋；巧克力棕中小型柔軟方形麂皮肩背包
- occasion: 咖啡廳／週末
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- required_frames: 3
- canva_template: `v3-E` / Mira Template Master v3 - E Cross-Boundary Weekend Air
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-002\looks\2026-W35-002-L01\carousel\codex_generation_handoff.md
```