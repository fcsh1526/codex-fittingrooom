# Mira Daily Image Job

- carousel_id: `2026-W37-004`
- look_id: `2026-W37-004-L02`
- look_name: 黑色中長裙配奶油白T字帶鞋
- model_profile_id: `M01`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 復古 T 字帶鞋日常化
- clothing_item: 黑色短袖棉質上衣；黑色高腰中長A字裙；奶油白方頭低粗跟T字帶鞋，腳背直帶連接橫帶；黑色小肩包；細銀耳釘
- occasion: 通勤／畫廊
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W37\generated_images\2026-W37-004\looks\2026-W37-004-L02\carousel\codex_generation_handoff.md
```