# Mira Daily Image Job

- carousel_id: `2026-W36-004`
- look_id: `2026-W36-004-L02`
- look_name: 酒紅緞面斜裁裙＋奶油白短袖上衣
- model_profile_id: `M04`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 絲巾效果與緞面垂墜
- clothing_item: 奶油白合身短袖細針織上衣；酒紅高腰斜裁緞面中長裙；深棕方頭低跟鞋；深棕小型肩背包；小型金色耳釘
- occasion: 旅行晚餐／藝文活動
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- required_frames: 3
- canva_template: `v3-A` / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-004\looks\2026-W36-004-L02\carousel\codex_generation_handoff.md
```