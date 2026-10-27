# F04 L02 close tracking — independent sampled review, 2026-10-21

## Decision

**Eligible for a separately named local research join**, with the tightening framing and unvalidated background fixture disclosed. No demonstrated fatal scene morph was found in the inspected views. This is not user dynamic approval, precise site reconstruction, seamless-join certification, or publishing acceptance. No automatic generation retry is justified by this review.

## Technical evidence

- Source `F04_close_source.mp4`: SHA256 `502951d7b908e24c7d5c21f60f9a2e0d369e9fc05f012cb9a1bb0fee16b73145`; 6,202,410 bytes.
- Entire source decoded: 145 frames, 24 fps, 720×1280; derived duration 6.0416667s. Container includes H264, AAC and attached MJPEG cover.
- Silent remux `F04_close_silent.mp4`: SHA256 `b7b33373701487ccf58ded07107d60fce14f451d30b005b1a5910ea461296f5f`; 6,027,348 bytes. Copies only the main H264, removes audio/cover, no crop/retiming/re-encoding/text.
- Source and silent H264 AnnexB SHA256 both `3be9adca3a95d007844da209c08cdf77ee165f2cc72f80a8bafe759e48ed6211`.
- Protected accepted331-frame prefix hash checked before/after unchanged: `f36b079261d6ba43bc1bf17f9504b4a1424efc393c24e5d53d9f4075165eaa33`.

## Visual inspection performed

25 whole-frame checkpoints; denser 3–5s every4frames; every-frame right-background windows84–120; all first18 and last18 contact-sheet frames; native f96/104/108/112 and side-by-side approved first/actual first/bridge endpoint. Actual bridge/L02 phase pairs127→0,136→9,144→17 were also inspected. This reviewer did not perform continuous normal-speed playback.

### Background fixture

The pale cylindrical/metal bollard-like object becomes visible at the **right picture boundary around f102–104 (~4.25–4.33s)**, moves left across successive frames as other background features do, and is subsequently hidden behind the moving subject around f112 onward. It does not appear to grow out of foliage or pop into the open middle of the image in the inspected dense sequence. Native f104/108/112 support an edge reveal and occlusion interpretation. It is unvalidated against the site's approved geometry, and its exact object type is uncertain; this review does not establish that it was physically present in the earlier shared scene. The evidence supports disclosure rather than a definitive morphing failure.

### Subject and framing

- Face/hair family, cream/navy checked collared shirt, rolled sleeves, charcoal waistband, and black near-shoulder bag remain coherent in samples. Grid lines deform with fabric/body movement; no abrupt replacement or grid disappearance was seen.
- Direction remains screen-right. Arm swing and visible hips suggest continued walking. Feet are outside this shot throughout: no foot-grounding or zero-sliding conclusion can be drawn.
- The camera progressively tightens more than the requested maintained head–mid-thigh framing. Face/upper garment become dominant and the bag's left corner leaves the frame late. This is a visible composition deviation, not a hidden pass on fixed-scale framing.
- Focus is naturally soft on the company/glass/planter background, but exact camera/world geometry is not reconstructed or measured by this inspection.

### Bridge join limits

Actual L02 first visually closely matches the approved L02 close starting still, and its scale/face placement is close to the bridge's actual final image. However, a 0.75s overlap begins18frames earlier than that final image. The paired sample board shows head/shoulder scale/position and arm/leg-phase differences during that interval. A dissolve may retain double edges; a local research preview is warranted to assess comfort, **not an assertion that the join is seamless**. No film was rendered by this reviewer and no accepted prefix or earlier media were edited.

## Files for root review

- `checkpoints_25.jpg`
- `dense_3_to_5s.jpg`
- `dense_object_3p5_to_5s.jpg`
- `frame_000096.png`, `frame_000104.png`, `frame_000108.png`, `frame_000112.png`
- `anchor_comparison.jpg`
- `overlap_phase_pairs.jpg`, `first18.jpg`, `last18.jpg`
- `technical_report.json`, `ffmpeg_stream_info.txt`, `silent_remux_log.txt`

No browser, generation, joining, canonical/status edits, publishing, Drive/GitHub changes or outside-folder writes were performed by this reviewer.
