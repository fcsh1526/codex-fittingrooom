# Mira Daily Image Job

- carousel_id: `2026-W46-002`
- look_id: `2026-W46-002-L01`
- look_name: 通勤白襯衫 × 深靛直筒
- model_profile_id: `M02`
- delivery_surface: `reel`
- reference_face_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_face.png`
- reference_full_image: `C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M02_start_v3_full.png`
- attach_reference_images: `required`
- trend: 深靛牛仔褲，怎麼穿得像要上班？
- clothing_item: 白色挺薄棉小尖領長袖襯衫袖口折一折、深靛無刷破中高腰直筒丹寧九分長、黑皮便士樂福鞋、酒紅扁方肩包、銀色小耳釘
- occasion: 有遮簷的共享工作室與週末雜貨店
- frame_plan: Reel 原生9:16全身＋直幅proof；Carousel A全身、B情境、C配件
- required_frames: Reel A+proof; Carousel A+B+C
- direct_reel_frame: `1080x1920` / `9:16`
- reel_frame_targets: `reel_frame_targets.json`
- canva_crop_limit_applies: `no`

Generate and review the native 9:16 full-person Reel A; it is the only still required for this surface.
Do not reuse one surface's crop as the other surface's source.
Keep anatomy, identity, contact-shadow, crop-safety, and platform checks in review_sheet.csv rather than adding them to the generation prompt.

Codex handoff:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W46\generated_images\2026-W46-002\looks\2026-W46-002-L01\reel\codex_generation_handoff.md
```