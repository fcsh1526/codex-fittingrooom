# Mira Daily Image Job

- carousel_id: `2026-W34-001`
- look_id: `2026-W34-001-L02`
- look_name: 細條紋牛津襯衫＋西裝短褲
- model_profile_id: `M03`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 寬版牛津襯衫日常穿法
- clothing_item: 淺藍白細條紋寬版牛津襯衫；深海軍藍高腰直筒西裝短褲；黑色低跟樂福鞋；黑色帆布托特包
- occasion: 上課／週末
- frame_plan: hero+alternate_view
- required_frames: 2
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review Hero A only. Do not generate B/C before user acceptance.
B Alternate View and C Detail are optional production assets, not chronological action continuations or A/B tests; create them only when the publishing format needs them.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W34\generated_images\2026-W34-001\looks\2026-W34-001-L02\reel\codex_generation_handoff.md
```