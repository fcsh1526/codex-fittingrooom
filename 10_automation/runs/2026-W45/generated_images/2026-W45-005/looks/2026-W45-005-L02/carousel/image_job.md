# Mira Daily Image Job

- carousel_id: `2026-W45-005`
- look_id: `2026-W45-005-L02`
- look_name: 同套白T深藍褲＋灰藍薄外層
- model_profile_id: `M05`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M05_start_v1_full.png`
- attach_reference_images: `required`
- trend: 短袖底層，一件薄外層應付冷氣房
- clothing_item: 同款白棉短袖T、灰藍薄棉平織長袖襯衫外套敞開、同款深藍直筒長褲、同款白灰低筒球鞋、同款深棕小肩包、細銀耳環
- occasion: 日常外出／赴約
- frame_plan: Reel: native 9:16 full A + reviewed styling-proof; Carousel: A full / B scene / C detail
- required_frames: Reel A+proof; Carousel A+B+C
- canva_template: `v3-A` / Mira Template Master v3 - A Cross-Boundary Contact Sheet
- canva_slot_targets: `canva_slot_targets.json`
- canva_crop_limit: `15%`

Generate Carousel A first. After acceptance, B Scene Application and C Accessory Detail are both required.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W45\generated_images\2026-W45-005\looks\2026-W45-005-L02\carousel\codex_generation_handoff.md
```