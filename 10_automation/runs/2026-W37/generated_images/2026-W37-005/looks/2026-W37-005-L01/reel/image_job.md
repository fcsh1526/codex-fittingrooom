# Mira Daily Image Job

- carousel_id: `2026-W37-005`
- look_id: `2026-W37-005-L01`
- look_name: 奶油白棉麻配焦糖麂皮包
- model_profile_id: `M03`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 麂皮與皮革一件亮點
- clothing_item: 奶油白無袖棉麻襯衫；深咖啡高腰薄棉麻直筒褲；焦糖色短毛麂皮小肩包；黑色低跟樂福鞋；細銀耳環
- occasion: 咖啡廳／週末採買
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W37\generated_images\2026-W37-005\looks\2026-W37-005-L01\reel\codex_generation_handoff.md
```