# Mira Daily Image Job

- carousel_id: `2026-W37-005`
- look_id: `2026-W37-005-L02`
- look_name: 淺藍襯衫裙配巧克力麂皮包
- model_profile_id: `M03`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 麂皮與皮革一件亮點
- clothing_item: 淺藍短袖棉質襯衫中長洋裝，配同布腰帶；巧克力棕短毛麂皮小肩包；黑色平底包鞋；銀色耳釘
- occasion: 咖啡廳／週末採買
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W37\generated_images\2026-W37-005\looks\2026-W37-005-L02\carousel\codex_generation_handoff.md
```