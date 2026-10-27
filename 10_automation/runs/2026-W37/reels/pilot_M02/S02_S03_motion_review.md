# M02 comparison v2 — middle-pair motion review

## Four-shot assembly checkpoint — 2026-09-24

The user approved the S04 full-person still; S04 motion was generated and saved. S02 attempt 02 and S03 attempt 02 were assembled with S01 and S04 into a silent, caption-free technical rough cut (`videos/M02_comparison_v2_roughcut_01_seekable.webm`). The selected S03 source ends at 2.75s, before the observed shoulder-slip defect after about 3.47s. Output cut positions are approximately 2.55s, 5.00s and 7.65s. The browser replay showed all four shots at normal speed and sampled cut neighborhoods without a black interruption or a rapid opening flash. This is a provisional review; complete frame-level dynamic QA and user visual approval remain pending. Provenance and limits are in `comparison_v2_roughcut_01.json`.

Status 2026-09-23: S02 and S03 starting stills approved by user (`可以`). After recovery of the existing Grok tab, S02 attempt 01 generated and played at 720×1280, 6.041667s. See `S02_comparison_v2_motion_01.json`. Local download and dynamic QA remain unconfirmed; S03 motion pending. The user-visible Codex HTTP 400 and the separate Grok verification/attachment failures are distinguished in `operation_recovery_2026-09-23.md`.

## Review correction — 2026-09-24

Both attempt-01 videos are downloaded locally. The Grok player was paused and scrubbed at approximately 0.25, 1.55, 3.0 and 5.65 seconds. S02 moved the cream dress/skirt widely at about 1.55s instead of only opening the gray shirt at the waist. S03 pulled the pale-blue shirt off the viewer-left shoulder during the action; by about 3s its shoulder is bare and a dress strap is exposed, contrary to the desired layering. Both attempt-01 clips fail the intended styling-proof action. Their roughly stable face/scene in sampled moments is insufficient for a full dynamic QA pass. One narrower garment-action retry is specified in `prompts/S02_comparison_v2_motion_v2.md` and `prompts/S03_comparison_v2_motion_v2.md`.

The prior WPF paused-seek samples, including the newer `qa/S02_comparison_v2_01_validated/` and `qa/S03_comparison_v2_01_validated/` directories, returned duplicate frames despite different timestamp labels. These folders are **invalid** as time-series evidence. The later fresh-player playback outputs also returned duplicate frames despite reported playback times. The actual review above is grounded in the Grok browser player and its visible time readout; no local extracted-frame QA is claimed.

## Intended cut

S01 L01 full → S02 L01 close → S03 L02 close → S04 L02 full. S02/S03 are the matched center of the film. Their job is to let the viewer compare the gray-shirt/cream-dress neckline and open front with the pale-blue-shirt/navy-square-neck combination, not to hold two portrait photos on screen.

## Retry checkpoint — 2026-09-24

- S02 attempt 02 is downloaded and sampled at about 1s, 2.5s and 3s. The free hand briefly pinches the gray shirt hem, then lowers; the cream dress stays in place. This is a provisional action match. Full continuous dynamic QA and the S01→S02 cut still need review.
- S03 attempt 02 is downloaded. At 1.66, 2.10, 2.50 and 2.97s, the blue shirt remains on both shoulders; at 3.47s the viewer-left shoulder drops and exposes the navy dress strap, persisting near 5.65s. Reject the full clip. The 0–2.8s range is a possible trim, not a QA pass. Do not retry the same gesture again; the plan allows only one candidate retry before reducing movement or changing the shot.
- S02 around 2.5s and S03 near the start were inspected in the Grok player. Face position, shoulder scale and daylight are similar enough for a direct-cut test; the outfit change is immediately visible. Whether the moving pair feels natural is still unverified without an assembled normal-speed cut.
- A user-review S04 full-person still candidate has been saved. Do not animate it until the user visually approves the still. See `S04_comparison_v2_generation.json`.

The local paused-seek WPF image samples remained duplicates and are not timing evidence. The above timestamps come from the Grok player's current time and screenshot. The entire selected intervals and complete edit have not yet passed normal-speed QA.

## What to record after each generation

| Check | S02 | S03 |
| --- | --- | --- |
| Grok URL / local file / actual pixels / duration | pending | pending |
| First frame plus `@Mira M02 v3` verified before send | pending | pending |
| Natural gesture starts promptly and ends without long idle hold | pending | pending |
| Face and hairstyle through start, 25%, 50%, 75%, end | pending | pending |
| Shirt, dress neckline/waist, bag and hands through gesture | pending | pending |
| Usable interval, retry count, active time, waiting time | pending | pending |
| Full playback at normal speed | pending | pending |

Pair review: check cut at S02→S03 for eye-line position, shoulder scale, light direction, shirt-front position and whether the outfit difference reads immediately. Reject a flashing or presentation-slide effect even if both source clips pass individually. Do not use speed changes or decorative transitions to hide an uncomfortable cut.
