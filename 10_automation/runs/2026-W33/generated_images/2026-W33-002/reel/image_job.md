# Mira Daily Image Job

- carousel_id: `2026-W33-002`
- model_profile_id: `M02`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 縮短比例
- clothing_item: 七分褲／褲裙／九分直筒褲
- occasion: 咖啡廳／創意辦公室
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review Hero A only. Do not generate B/C before user acceptance.
B Motion and C Detail are optional production derivatives, not A/B tests; create them only when the publishing format needs them.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W33\generated_images\2026-W33-002\reel\codex_generation_handoff.md
```