# W29 Photorealism Pilot

## Test 1 - Codex improved workflow

- Model: M01
- Theme: sheer mesh top, satin camisole, ivory wide-leg trousers
- References: approved M01 face and full-body anchors only
- Old W29 generated images: not used as references
- User sample image: quality benchmark only; not passed to image generation

Production changes:

- concise prompt instead of a long negative-constraint stack
- one coherent lifestyle photograph rather than a catalog full-body plate
- physical interaction with a real foreground object
- shared window light, contact shadows, ambient color spill, grain, and depth of field
- natural adult proportions with a non-shrunken head
- one Hero image first; no B/C generation until the Hero passes

Success criteria:

- person does not look pasted onto the environment
- hand/object and shoe/floor contact are physically plausible
- head-to-body ratio is natural and consistent with M01
- skin, clothing, foreground, and background share one photographic treatment
- outfit remains readable despite natural foreground overlap

Target output:

`2026-W29-001_M01_codex_photoreal_pilot_A.png`

## Execution status - 2026-07-15

- Attempt 1: image generation service returned HTTP 520 after several minutes.
- Attempt 2: no output or error after an extended wait; the hung request was terminated.
- Assessment: infrastructure failure, not a visual-quality failure. Test 1 remains pending.
- Retry rule: rerun the same single M01 Hero test when the Codex image service is responsive. Do not generate B/C or apply anything to Canva before the Hero passes review.
- Fallback rule: move to ChatGPT web Images 2.0 only if a successfully generated Codex Hero still fails the visual criteria above. Do not switch to the separately billed API without explicit approval.

## Successful retry - 2026-07-15

Built-in Codex image generation completed successfully on the next retry.

Outputs:

- `2026-W29-001_M01_codex_photoreal_pilot_A.png`: initial integrated-scene Hero.
- `2026-W29-001_M01_codex_photoreal_pilot_A_refined_v2.png`: targeted lighting and camera-finish refinement. Identity, outfit, composition, and proportions were locked during the edit.

Assessment:

- PASS: M01 identity remains recognizable.
- PASS: head-to-body ratio and overall adult proportions are plausible.
- PASS: hand-to-stone and shoe-to-floor contact are physically grounded.
- PASS: outfit components remain readable and structurally coherent.
- IMPROVED: window light, reflected light, contact shadows, and environmental depth are more unified in the refined version.
- PARTIAL: the person no longer has the strong pasted-on appearance seen in earlier W29 runs, but the result still reads as cleaner and more controlled than a real candid photograph.
- PARTIAL: front-facing stance and facial finish retain some catalog-image stiffness and synthetic smoothness.

Decision at the initial comparison checkpoint:

- Hold B/C and Canva until the user accepts or rejects the Codex method.
- Codex Test 1 is technically successful and materially improved, but it does not fully match the natural photographic realism of the user's ChatGPT web benchmark.
- The next controlled comparison should use ChatGPT web Images 2.0 with the same M01 references, outfit, scene, and scoring criteria. No separately billed API is required for that comparison.

## Trial activation - 2026-07-15

The user accepted the improved Codex method as the active trial workflow. The web comparison is deferred.

W29-001 production assets:

- `../generated_images/2026-W29-001/2026-W29-001_M01_photoreal_pilot_candidate_A.png`
- `../generated_images/2026-W29-001/2026-W29-001_M01_photoreal_pilot_candidate_B.png`
- `../generated_images/2026-W29-001/2026-W29-001_M01_photoreal_pilot_candidate_C.png`

Operational result:

- A is the accepted refined Hero and session lock.
- B was derived from A as a movement/gaze variation.
- C was derived from A as an outfit-detail composition.
- All three passed the pilot review and are selected for W29-001.
- W29-002 through W29-005 were reset to `needs_review`; old W29 v2 selections cannot be used for new Canva work.
- Review page: `../W29-001_PHOTOREAL_PILOT_REVIEW.html`.
