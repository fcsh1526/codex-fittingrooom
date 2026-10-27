# Mira Daily Image Job

- carousel_id: `2026-W37-002`
- look_id: `2026-W37-002-L01`
- look_name: 白色短夾克配靛藍寬褲
- model_profile_id: `M05`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 短外層配長流動下身
- clothing_item: 光學白無鋪棉短版薄斜紋夾克；淡藍短袖棉襯衫紮入腰頭；深靛藍高腰薄料長寬褲；黑色平底樂福鞋；焦糖棕小方包
- occasion: 上班／看展
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W37\generated_images\2026-W37-002\looks\2026-W37-002-L01\carousel\codex_generation_handoff.md
```