# Independent recovered-angle source review

Date: 2026-10-05. Reviewer: orientation_review_readiness_oct05.

## Evidence inspected

- A/B `native_25_checkpoints.jpg` and `face_5_checkpoints.jpg`: all displayed checkpoint tiles, frames 0,6,...,144 at native24fps.
- Original720x1280 A frames0,24,48,72,144; B frames24,84,90,96,108,144.
- Approved identity anchor `02_brand/reference_models/M02_start_v3_face.png`.
- Inspection receipts report each source720x1280,24fps,145 decoded frames/6.0417s, no black/near-identical technical candidates. Those signals do not establish visual quality.
- Exact source hashes: A `9e62f66f6562c9a059600f03e5cd3fcc313df00b77ac71915e41d1801353eb83`; B `db36cdaca6158eb2b6ac0755ceb1603a7b52bff0f5ced1673d3d4b61a339cfce`.

## Sampled quality

No obvious sampled identity swap, wardrobe-color/neckline jump, missing shoe or major background-geometry warp. Faces retain the visible eye/nose/jaw relationships of the approved M02 anchor; A smiles with visible teeth while B changes toward a closed-mouth expression. Expression differences are not, on these stills, proof of identity drift. Fine fingers, contact/foot sliding and inter-frame facial continuity remain unverified by this still review.

Both clips include an opening step/stance adjustment before the turn, contrary to the prompt's stationary-feet intention. The actual torso turn is visibly more side-on than a nominal shallow30-degree turn; no measured angle is claimed. A reaches the turned pose around2.5-3s, B around4-4.5s. Actions/timings must be preserved, not retimed into synchronization. Bookcase, window, seat and table remain broadly stable in the inspected views; subject size changes cannot alone be described as camera zoom.

## Information utility and limitation

The turn adds a side sleeve/rolled-cuff view and dress side silhouette relative to the frontal color/neckline view. A also exposes part of the shirt's lower rear hem below its shoulder bag. Both bags obscure the torso-side shirt area, especially B's large tote; B cannot be presented as an unobstructed demonstration of lower shirt-side drape. This is a limited but real added viewing angle, not a demonstrated full clothing-material/fit test.

A native-time parallel composition is a reasonable next diagnostic before requesting another generation. Its asymmetrical turn timing and the tote obstruction must be judged in the combined mobile-size film. No universal format adoption or audience-performance inference follows.

## Constant composition recommendation

For these inspected points, a common constant native window x145..615, y0..1280 (`[145,0,470,1280]`) appears to retain full head/shoes, sleeves, hands, skirt and bags. A's broad front skirt in frame24 has rightmost hem aroundx580-586. B's tote is most rightward in the inspected frame84, roughlyx595-600, leaving only about15-20native pixels before x615. These are manual approximate observations, not segmentation or all-frame bounds. Recheck B's neighboring pivot frames and the actual render.

These new clips show similar overall native head/shoe scale; the old3.69% A reduction is not justified by the prior clip's measurements. Begin from a shared proportional contain scale, then assess actual head/waist/shoe placement at front and turn phases before any small constant adjustment. Use equal image rectangles and safe padding; do not copy old15/19px ambient trims without checking the new heads/shoes. If more width is needed, expand the fixed window and accept smaller figures rather than cut the demonstrated silhouette or tote.

No moving crop, pose change, stretch, freeze, reversal, replay or retime is recommended. Any selected last frame (e.g.143 for a6s/144-frame selection) still needs output QA; this source sample ends at144. No interior cut means no added dissolve; any later cut remains approximately0.75s.

## Review limits and writes

This is sampled source QA for composition planning. It is not normal-speed continuous playback, every-frame boundary certification, final output QA or user approval. No browser operation, source alteration, rendering or protected-output change was performed. This review Markdown is the only write during visual review.

## Exact v2 output sampled review

Output: `orientation_study/M02_parallel_angle_review_v2.mp4`. Independently read back SHA256 `9831b95eb5e88b1f13295a650c9a7faaf18fe3223f3cfb9a3336cde4ef26c569`. Its receipt records720x1280,24fps,144frames/6s, using each native source's frames[0,144), start inclusive/end exclusive. The failed earlier v1 is not this reviewed file.

Inspected the output's five-point `qa/output_v2/checkpoints.jpg` (frames0,36,72,108,143), plus original-size output frames24,84,143. The shared fixed source window[135,0,490,1280] ends atx625; equal352x920 image rectangles at local[4,180] give matching top/bottom panel edges without the historical A-only shrink.

- At these points, both heads, shoes, hands, sleeves, dress hems and bags remain complete. Critical A frame24 skirt has visible space before its panel's right edge; B frame84 tote remains complete with roughly20output pixels of space at its rightmost corner. These are manual approximate observations, not measured segmentation or every-frame certification.
- Shared scale is visually reasonable. Front/end head and foot positions are close; front pose/foot stance and transient turn differences still change the apparent height. At frame84 B's head sits roughly10output pixels higher while A is already turned. Do not claim identical size/pose at all times or animate a correction to hide the native action difference.
- No obvious sampled new face jump, clothing-color/neckline swap, stretched figure or library-geometry fault introduced by this composition. Both image panels and padding align. Continuous facial/hand/foot behavior and every-frame background stability remain separate checks.
- The side-view sleeve and dress-outline information survives the half-width composition. B's tote still obscures much of the lower shirt-side area. Fine garment detail/phone readability and attention split between an earlier A turn and later B turn require normal-speed full-film/user review.

Recommendation: this exact v2 is suitable for the next full-film visual review, with the above limits recorded. Do not generate another source solely from these sampled results. No continuous playback pass, user approval, publishability, general format adoption or exposure result is asserted. No output/source file or browser was changed in this independent review; only this Markdown was appended.
