# W30-005 Controlled Reel Test v2 Hypothesis

Status: preview rejected for frame-rate stutter; not published

## Problem carried forward

- Test v1 reached 102 accounts, all non-followers.
- Average watch time improved to 2 seconds, but skip rate remained 97%.
- A single still with a subtle push-in did not create enough first-second visual payoff.

## Test hypothesis

An obvious visual reveal within the first 0.8 seconds will reduce early skipping more than a continuous subtle push-in.

## Selected unpublished source assets

1. Opening detail: `../generated_images/2026-W30-005/2026-W30-005_M02_candidate_C.png`
2. Motion reveal: `../generated_images/2026-W30-005/2026-W30-005_M02_candidate_B.png`

Both assets belong to the accepted W30-005 Hero session and preserve the same model, outfit, scene, and lighting logic.

## Controlled variables

- Length: approximately 6 seconds
- Outfit and topic: unchanged
- Opening headline: unchanged
- Instagram music: same W30-003 instrumental track at the same low volume
- Caption and hashtags: unchanged
- AI label: enabled
- Advertising and cross-platform distribution: off

## Changed visual treatment

Replace the one-image continuous push-in with an obvious four-beat editorial cut:

- `0.00–0.72 s`: tight scarf-at-waist detail with a fast pull-back.
- `0.72–2.25 s`: hard cut to the B Motion face-and-torso view with lateral movement.
- `2.25–3.85 s`: return to the outfit-detail view with a downward move toward the scarf.
- `3.85–6.00 s`: finish on the B Motion view with a clearer push and lateral move.

## Generated preview

- Video: `W30-005_controlled_reel_v2_preview.mp4`
- Poster: `W30-005_controlled_reel_v2_poster.png`
- Canvas: 1080 x 1920 px
- Duration: 6.005 seconds
- Encoding: H.264 MP4
- Audio: none in preview

## Preview rejection

- User review: motion appears poor and stutters.
- Playback inspection: 135 total frames across 6.005 seconds, approximately 22.5 fps rather than the intended 30 fps.
- Diagnostic playback also reported 11 dropped frames and 0 corrupted frames.
- Decision: do not publish or reuse this render.
- Required correction: pre-crop the source images before animation and render a new fixed-30-fps preview with lighter per-frame transforms.

## Directional success threshold

- Average watch time reaches at least 3 seconds.
- Skip rate falls below 90%.
- Wider distribution is evaluated only after retention improves.
