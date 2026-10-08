# Mira Daily Image Job

- carousel_id: `2026-W41-005`
- look_id: `2026-W41-005-L01`
- look_name: 白T炭灰長褲配鈷藍小包
- model_profile_id: `M04`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M04_start_v3_full.png`
- attach_reference_images: `required`
- trend: 亮色包款與首飾單點
- clothing_item: 白色圓領棉短袖紮入；炭灰高腰直筒長褲；黑色無鋪棉薄短外套敞開；黑色低跟便鞋；鈷藍霧面小肩包、短肩帶；小型銀色幾何耳針
- occasion: 通勤
- frame_plan: carousel:hero_full+scene_application+accessory_detail;reel:hero_full_9x16
- required_frames: 3
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review the native 9:16 full-person Reel A; it is the only still required for this surface.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W41\generated_images\2026-W41-005\looks\2026-W41-005-L01\reel\codex_generation_handoff.md
```