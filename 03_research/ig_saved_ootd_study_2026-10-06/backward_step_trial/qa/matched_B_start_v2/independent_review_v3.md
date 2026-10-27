# Independent static review — matched B start v3

Date: 2026-10-06. Scope: the additional targeted wardrobe correction, compared with rejected v2 and the approved B wardrobe master. No generation or source-image edit was performed by this reviewer.

**Decision: the visible grey shoulder-strap correction passes this limited static review; V3 is suitable to present for individual user still approval. It remains an unapproved candidate.**

## Exact candidate

`10_automation/runs/2026-W37/generated_images/2026-W37-001/looks/2026-W37-001-L02/reel/body_distance_matched_start_v2/2026-W37-001-L02_M02_body_distance_matched_start_candidate_v3.png`

- Actual dimensions: 941×1672.
- Verified SHA256: `f8098adfefc9be66ffcfea9bc3bad424e3f5e34a30a343d50dc4478f10af16e6`.
- The rejected v2 and approved B hashes remain those listed in `independent_review.md`.
- Root reports this is an additional targeted grey-strap colour/width correction after the base generation and original distance correction. This review does not erase or reset that additional-edit count or change the global skill rule.

## Findings

The dark navy narrow shoulder strap seen in v2 has changed to a grey canvas-looking strap with appropriate visible width and edge construction. Its tone and construction now agree with the approved B grey tote much more closely. The grey tote body, holding hand and shoulder placement remain visible and plausible. The saved native crop comparison was inspected against all three versions.

The v2 person and room geometry are visibly retained: hair top approximately y185, dress waist/seam approximately y473, frontmost sole approximately y1020 on the common 720×1280 QA canvas. No major position or size change is discernible at the manual review tolerance of approximately ±5 pixels (waist ±10). The face, low bun, rolled shirt, navy square-front calf dress, cream unlaced slip-ons and visible stud remain consistent; no new obvious anatomy, identity, shoe, contact or wardrobe defect was seen.

Major background landmarks retain v2 positions: left window upright near x45–50, left wall/pillar boundary near x110, right bookshelf boundary near x563, rear wall/floor transition near y724–727, table top near y603–605 and shelf plant-pot base near y283–286. No new major scene or camera-position change is visible in the inspected boards. The result is a generative edit: this review confirms visible geometry and wardrobe correction, not pixel-identical retention of every fabric, book, leaf or floor detail.

## Residual limits

The prior A-frame mismatch remains approximately the same: relative to A near_A1 native frame 96, V3 hair top is about 7 pixels lower, the frontmost sole is about 44 pixels higher, and the hair-to-sole span is about 5.8% shorter. A/B stance and different dress waist construction remain. Shoulder-strap width of the **dress** is still covered by the shirt and cannot be independently established from this still. Fine background detail is not an exact registered match.

These limits do not prevent presenting V3 as the corrected still candidate, but they prevent claiming that the next B motion, dynamic identity, camera stability, dissolve double-face problem, combined-film comfort or normal-speed full-film QA has passed. User approval must name this exact V3 before any next motion action.

## Saved QA evidence

- `v2_v3_same_canvas_720_QA.jpg`: rejected V2 and corrected V3, proportional 720×1279 contain images on 720×1280 inspection canvases, with common head/waist/sole guides. Viewed.
- `v2_v3_approved_B_strap_QA.jpg`: native cropped shoulder/tote comparison of V2, V3 and approved B. Viewed.
- `qa_v3_input.json`: actual dimensions and verified candidate hash.
- `build_qa_v3.py`: reproducible QA derivatives only.

Delivery assets were not modified. V2 remains failed wardrobe and preserved; V3 remains pending individual user visual approval. No third correction, video generation, cloud action, approved-original replacement, status promotion or publication was performed by this reviewer.
