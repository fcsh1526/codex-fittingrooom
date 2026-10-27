# F04 deterministic geometry reset

Scope: only the existing company-front crossing segment, after the three failed F04 motion sources. No further AI/Grok call, existing image edit or movie is performed here. Earlier files remain unchanged.

## Reused project geometry

- `continuous_route_storyboard_2026-10-16/route_plan.json`: existing company facade z8.8, road z2.5–5.4, shared crossing x11.5–13.5, same approach route. Units are schematic, not surveyed metres.
- `continuous_route_storyboard_2026-10-16/render_route.py`: `position(t)` Hermite person path; shared world geometry; actual painted rectangles are x11.35–13.7, z2.65+n×0.46, thickness0.23, n0..5. These are six rectangles. The slight difference from the plan's nominal crossing width is existing code, not a new site proposal.
- `static_key_views_2026-10-16/build_key_views.py`: corrected perspective/right-vector convention in `KeyWorld.project`; eye height1.30, horizon0.42.
- `accepted_keys_previs_2026-10-16/build_previs.py`: `camera_values(t)` interpolates the accepted camera locations/look targets/focal ratio; original K3 t13.4 uses145° rear-quarter key direction.

The new preview reads those helpers without invoking their rendering entrypoints. It extracts101 camera/person states only from F04's existing schematic t11.25–15.75 interval. Slider percentage is a route position, **not** a claim about six-second generated-video timing.

## Direction conflict revealed

This preview deliberately retains the original six world rectangles and original camera curve. Its central white rectangle long edge projects at approximately0.86°/14.10°/31.95° from horizontal for start/mid/end. Thus the original middle is nearly horizontal, **unlike the newly approved midpoint image's long strips extending from the bottom into depth**. It must not be labelled as matching that new midpoint.

One later decision must resolve the camera/paint layout globally within this same site. A suitable camera change may preserve the fixed original paint; alternatively one explicitly approved global paint orientation could be used across the whole segment. Rotating or stretching the paint separately in start/mid/end is forbidden. This preview does not silently choose either correction or override the approved image direction.

## Outputs and limits

- `f04-fixed-crosswalk.html`: theme-aware fragment, same-six-stripe perspective view plus matching small plan, one position slider and start/mid/end buttons. No animation loop, fetch or external API.
- `f04-fixed-crosswalk-three-views.svg`: deterministic start/mid/end projection of those same vertices.
- `geometry_plan.json`: immutable stripe vertices and sampled original camera/person states.
- `geometry_preview_receipt.json`: input/output hashes, projection audit and limitations.

This is a geometry/shot-planning illustration, not photoreal scene calibration. It does not match the approved source pixels, original plant details, face, outfit, body motion or generator feasibility. The line person is only a world-position marker. Text is planning annotation, never rendered into a Reel. Original protected images, accepted film, failed sources and publishing packages remain unchanged.
