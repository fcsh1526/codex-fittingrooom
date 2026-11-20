# Mira Daily Image Job

- carousel_id: `2026-W45-001`
- look_id: `2026-W45-001-L01`
- look_name: 沙卡其短工裝＋深藍直褲
- model_profile_id: `M01`
- delivery_surface: `carousel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png`
- attach_reference_images: `required`
- trend: 短工裝出門，褲裝與裙裝各有精神
- clothing_item: 沙卡其短版無鋪棉工裝外套敞開、白棉短袖T、深藍高腰直筒長褲、黑低筒休閒鞋、深棕小斜背包
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
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W45\generated_images\2026-W45-001\looks\2026-W45-001-L01\carousel\codex_generation_handoff.md
```