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
