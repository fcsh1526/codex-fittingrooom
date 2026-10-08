# Mira Daily Image Job

- carousel_id: `2026-W41-002`
- look_id: `2026-W41-002-L02`
- look_name: 可可棕奶油白格紋配深藍褲
- model_profile_id: `M01`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 格紋單品與素色留白
- clothing_item: 可可棕奶油白細格薄棉襯衫，尖領、袖口翻一折、下襬整齊紮入；深海軍藍高腰直筒長褲；深棕低跟便鞋；深棕小方肩包；小型銀耳針
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W41\generated_images\2026-W41-002\looks\2026-W41-002-L02\reel\codex_generation_handoff.md
```