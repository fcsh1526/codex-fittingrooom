# Mira Daily Image Job

- carousel_id: `2026-W41-002`
- look_id: `2026-W41-002-L01`
- look_name: 奶油白海軍藍格紋配炭灰褲
- model_profile_id: `M01`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 格紋單品與素色留白
- clothing_item: 奶油白海軍藍薄棉格紋襯衫，尖領、袖口翻一折、下襬整齊紮入；炭灰高腰直筒長褲；黑色低跟便鞋；黑色小方肩包；小型銀耳針
- occasion: 通勤
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W41\generated_images\2026-W41-002\looks\2026-W41-002-L01\carousel\codex_generation_handoff.md
```