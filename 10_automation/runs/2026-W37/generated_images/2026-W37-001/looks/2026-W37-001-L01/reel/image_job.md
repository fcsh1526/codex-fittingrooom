# Mira Daily Image Job

- carousel_id: `2026-W37-001`
- look_id: `2026-W37-001-L01`
- look_name: 霧灰薄襯衫配奶油白洋裝
- model_profile_id: `M02`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 可拆式輕薄疊穿
- clothing_item: 霧灰無內裡棉質薄襯衫；奶油白不透膚細肩帶小腿中長洋裝；白色低筒帆布鞋；深海軍藍小肩包；細銀耳環
- occasion: 冷氣房閱讀／花藝課
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W37\generated_images\2026-W37-001\looks\2026-W37-001-L01\reel\codex_generation_handoff.md
```