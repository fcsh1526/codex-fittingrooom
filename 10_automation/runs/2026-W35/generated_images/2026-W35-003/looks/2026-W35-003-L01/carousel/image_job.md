# Mira Daily Image Job

- carousel_id: `2026-W35-003`
- look_id: `2026-W35-003-L01`
- look_name: 海軍藍運動薄外套＋深灰直筒裙
- model_profile_id: `M03`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 運動外層配裙裝
- clothing_item: 深海軍藍短版立領薄尼龍運動外套；灰白合身棉質短袖；深灰高腰直筒中長裙；白色低調平底球鞋；黑色小型肩背包
- occasion: 上班／午間外出
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W35\generated_images\2026-W35-003\looks\2026-W35-003-L01\carousel\codex_generation_handoff.md
```