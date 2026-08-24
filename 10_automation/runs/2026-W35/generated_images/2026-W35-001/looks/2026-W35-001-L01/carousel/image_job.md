# Mira Daily Image Job

- carousel_id: `2026-W35-001`
- look_id: `2026-W35-001-L01`
- look_name: 石墨黑高領薄夾克＋米灰直筒褲
- model_profile_id: `M05`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 輕量高領外套
- clothing_item: 石墨黑無鋪棉短版高領薄夾克；奶油白合身棉質短袖上衣；米灰高腰窄直筒褲；黑色方頭樂福鞋；深灰小型肩背包
- occasion: 通勤／空調辦公室
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-001\looks\2026-W35-001-L01\carousel\codex_generation_handoff.md
```