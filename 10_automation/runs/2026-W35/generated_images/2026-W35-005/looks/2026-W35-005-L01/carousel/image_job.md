# Mira Daily Image Job

- carousel_id: `2026-W35-005`
- look_id: `2026-W35-005-L01`
- look_name: 柔霧粉薄緞面上衣＋深靛直筒丹寧
- model_profile_id: `M04`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深色直筒丹寧與柔和上衣
- clothing_item: 柔霧粉短袖薄緞面垂墜上衣；深靛藍中高腰直筒薄丹寧褲；深棕方頭低跟鞋；深棕結構小型肩背包；細版銀色耳環
- occasion: 通勤／簡報
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-005\looks\2026-W35-005-L01\carousel\codex_generation_handoff.md
```