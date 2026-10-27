# Fourth-shot fixed-projection review

The final bounded proposal is `geometry-fixed-lens.html` plus `geometry-fixed-lens-three-views.png`. Its title is「第四鏡：跟拍過街，再繞到側後方」. Buttons are「起點／途中／終點」. This wording describes moving camera angle without implying a locked viewpoint.

## Camera and framing

The original-start abstract focal ratio0.9977551495587385 is constant in all101 states. Varying it was not necessary for head/feet framing. This removes the earlier proposal's projection-scale/zoom change; that original proposal remains preserved. A physical50mm lens calibration is still not proven by schematic ratios, and the Mira50mm production standard is not overridden.

The converged camera keeps the earlier4-unit-side proposal: offset knots are `[0.27223968171254675,-3.058957233179415]`, `[4,0]`, `[4,-1.3]`. The opening camera/aim/framing, existing person path and six world-space paint rectangles remain unchanged. New camera angle/movement is still a proposal awaiting user review; no photographic match is claimed.

All101 marker head/feet positions fit the frame. Person height is approximately55.26%/42.40%/40.33% at start/middle/end. Mid/end clothes are therefore smaller. The endpoint retains only the last stripe; the plan view keeps all six fixed paint identities visible. Point checks are not full sleeve/bag contour, walking or generated-footage QA.

## Exact fixed-version interaction check

`geometry-fixed-lens-interaction-check.json` records the check performed against the final **fixed-version HTML**, not the earlier variable-focal proposal. Simulated DOM execution passed initial render, all three buttons, pressed-state changes, all101 slider positions, valid SVG point coordinates, and state storage. It also verifies that every embedded frame uses exactly the same focal ratio.

This is a Node simulated-DOM check only. Actual browser/CUA visual validation was not completed because the localhost page timed out. The PNG was rendered directly from the same plan with existing Pillow and then visually inspected; no software installation, AI still generation or Grok call was used.

Root reviewed the PNG's route projections. Its final title-only revision changes no geometry; the previous title raster is retained as `geometry-fixed-lens-three-views-before-title-fix.png`. The exact updated PNG/HTML hashes are in `geometry-fixed-lens-receipt.json`, whose camera_offset_knots field now correctly contains all three knots. No earlier proposal, protected photo, accepted film, failed source, Drive package or status document was changed by this review helper.
