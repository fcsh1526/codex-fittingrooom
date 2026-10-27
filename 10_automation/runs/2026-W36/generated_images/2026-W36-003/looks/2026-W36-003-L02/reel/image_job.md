# Mira Daily Image Job

- carousel_id: `2026-W36-003`
- look_id: `2026-W36-003-L02`
- look_name: 黑色棉麻洋裝＋焦糖麂皮扁包
- model_profile_id: `M01`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 麂皮質感小面積入秋
- clothing_item: 黑色無袖棉麻直身中長洋裝；焦糖棕扁平半月形麂皮肩背包；奶油白方頭平底鞋；銀色細耳環
- occasion: 週末逛書店／咖啡
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W36\generated_images\2026-W36-003\looks\2026-W36-003-L02\reel\codex_generation_handoff.md
```