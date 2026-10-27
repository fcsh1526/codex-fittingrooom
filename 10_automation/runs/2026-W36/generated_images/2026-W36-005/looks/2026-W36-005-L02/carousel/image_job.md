# Mira Daily Image Job

- carousel_id: `2026-W36-005`
- look_id: `2026-W36-005-L02`
- look_name: 黑色襯衫洋裝＋酒紅低跟鞋
- model_profile_id: `M03`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深紅色小面積亮點
- clothing_item: 黑色短袖棉質襯衫中長洋裝；酒紅尖頭低跟鞋；黑色小型光滑皮革肩背包；銀色細耳環
- occasion: 晚間看戲／聚餐
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-005\looks\2026-W36-005-L02\carousel\codex_generation_handoff.md
```