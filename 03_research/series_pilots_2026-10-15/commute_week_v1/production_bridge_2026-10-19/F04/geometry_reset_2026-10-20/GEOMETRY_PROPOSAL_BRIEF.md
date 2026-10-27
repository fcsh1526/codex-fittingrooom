# F04 camera-only proposal — not yet user approved

This is a new bounded photography proposal over the same existing crossing. It does not match or replace the earlier approved photos. It has not generated any still or video.

## Preserved and changed

- The six paint rectangles, road z2.5–5.4, two curb lines, company plane z8.8 and all101 person positions/headings are identical to `geometry_plan.json`.
- Original t11.25 camera location, look target and projection scale are retained at the opening.
- The camera's offset relative to the person passes through original `[0.27224,-3.05896]` → midpoint `[4,0]` → endpoint `[4,-1.3]` with piecewise continuous Hermite curves. Its world+x offset stays positive in all101 checked states; it does not cross to the opposite side of the person.
- At midpoint the camera is directly on the person's world+x side and aims at her. It then gradually moves slightly behind her toward the company side. No independent paint rotation is applied.
- Abstract projection focal ratio interpolates from the original0.99776 to1.45 at midpoint and1.15 at endpoint to retain full-body and a remaining view of the crossing. This is schematic field-of-view/framing control, **not physical lens metadata or a change/claim about the50mm production camera standard**.

## Measured projected direction

The same C3 long edge that was14.10° from horizontal in the original midpoint now projects at a directed102.39° from horizontal:12.39° away from vertical, equivalent to an acute77.61° from horizontal. This is meaningfully closer to the approved depthward/near-vertical white-strip direction. Other paint edges converge naturally through the same plane projection; no per-frame rotation or Y-shaped connection is introduced.

## Framing check and limitation

In all101 sampled states the person marker's head top and feet are inside the360×640 projection. On start/mid/end, the head/feet y pairs are approximately185.6/539.2,176.0/570.4,and198.8/496.3. The tested visible paint count is6/5/1 respectively. Thus paint is not entirely cropped away, but **only the final stripe remains at the endpoint**. Not all six strips remain readable throughout; the plan view preserves their fixed identities.

This checks marker points and projected paint polygons, not all sleeves/bag contours, real camera motion, walking anatomy, photographic background reconstruction or Grok feasibility. The new midpoint direction is a proposal, not proof of matching an approved photo or full-film approval.

## Outputs and verification

- `geometry-proposal.html`: only this proposed camera view, one slider and start/mid/end buttons, plus the matching fixed-site plan. No auto-play or network calls.
- `geometry-proposal-three-views.svg`: new deterministic start/mid/end sheet.
- `geometry-proposal-plan.json` and `geometry-proposal-receipt.json`: fixed geometry, new camera states, calculations and unchanged-input hashes.

Node simulated-DOM check passed initial drawing, buttons0/50/100,and all101 slider states, with no invalid SVG point coordinates. HTML is59,116 bytes. Real-browser layout/visual playback was not tested by this helper; root review remains necessary. Original conflict preview, receipt, photos, failed sources, accepted three-shot film and publishing packages remain untouched.
