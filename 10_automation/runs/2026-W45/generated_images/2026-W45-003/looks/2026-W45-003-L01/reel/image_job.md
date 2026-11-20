# Mira Daily Image Job

- carousel_id: `2026-W45-003`
- look_id: `2026-W45-003-L01`
- look_name: 同件海軍藍西外＋炭灰直褲
- model_profile_id: `M03`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M03_start_v3_full.png`
- attach_reference_images: `required`
- trend: 一件柔肩西外，直褲到淺裙
- clothing_item: 深海軍藍薄料柔肩單排扣西裝外套敞開、白棉圓領短袖T、炭灰高腰直筒長褲、黑低跟樂福鞋、黑小肩包、細銀項鍊
- occasion: 日常外出／赴約
- frame_plan: Reel: native 9:16 full A + reviewed styling-proof; Carousel: A full / B scene / C detail
- required_frames: Reel A+proof; Carousel A+B+C
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review the native 9:16 full-person Reel A; it is the only still required for this surface.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W45\generated_images\2026-W45-003\looks\2026-W45-003-L01\reel\codex_generation_handoff.md
```