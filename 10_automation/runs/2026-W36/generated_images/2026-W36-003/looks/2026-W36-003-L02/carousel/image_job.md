# Mira Daily Image Job

- carousel_id: `2026-W36-003`
- look_id: `2026-W36-003-L02`
- look_name: 黑色棉麻洋裝＋焦糖麂皮扁包
- model_profile_id: `M01`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 麂皮質感小面積入秋
- clothing_item: 黑色無袖棉麻直身中長洋裝；焦糖棕扁平半月形麂皮肩背包；奶油白方頭平底鞋；銀色細耳環
- occasion: 週末逛書店／咖啡
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- required_frames: 3
- canva_template: `v3-C` / Mira Template Master v3 - C Cross-Boundary Noir
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-003\looks\2026-W36-003-L02\carousel\codex_generation_handoff.md
```