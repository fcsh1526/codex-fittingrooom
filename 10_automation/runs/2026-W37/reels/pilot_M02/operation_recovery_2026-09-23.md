# Operation recovery — 2026-09-23

## Two distinct failures

1. The user-visible `{"detail":"Bad Request"}` is confirmed in the local Codex log as an HTTP 400 from the model `/responses` request, followed by a turn error. It occurred with both `gpt-6-sol` and `gpt-6-astra`. Recorded Taiwan times include 11:12:55, 11:28:28, 11:30:08, 11:30:59, 11:34:10 and 11:35:39. The response does not identify the rejected parameter or establish a root cause. It is not evidence of incomplete Grok verification. Current turn has successfully executed browser and local tools; this does not establish a permanent fix.
2. Grok's browser console separately recorded Cloudflare Turnstile widget reset failures. Before recovery, the composer showed two portrait thumbnails and did not establish a valid S02 outfit attachment. No generation was submitted from that uncertain state.

## Recovery performed

- Reloaded the existing Grok Imagine tab; no new tab opened.
- Uploaded the approved S02 PNG once through the file chooser.
- Confirmed its full filename in Grok's selected-upload checkbox and the correct gray-shirt/cream-dress thumbnail.
- Selected saved `Mira M02 v3`, then reassigned the outfit image to First frame.
- Verified 720p, 6s, 9:16 and audio off, and submitted `prompts/S02_comparison_v2_motion_v1.md`.
- No additional CAPTCHA appeared during this recovered upload/submission.

S02 result successfully played at 720×1280, 6.041667s: `https://grok.com/imagine/post/3686029e-88ed-4476-8ea9-be0248004fda?conversation=89b4f9be-afb7-4688-8cbc-e5b85d2cbfad`. Download button and a documented player download action did not yield a confirmed local file; local saving remains unresolved. Returned through the page's Back link to prepare S03 in the same tab. Opening the upload panel then displayed a new actual Cloudflare checkbox. The user was asked to complete this specific challenge; no S03 upload or generation was attempted through it.

## QA extraction correction

The earlier WPF paused-seek extraction returned the same visual frame at different requested timestamps. `S01_frame_2p8_qa.png` and all six PNGs in `qa/S01_comparison_v2_01/` are invalid as timestamp evidence and must not be used to claim dynamic QA. `S01_frame_5p0_test.png` is an approximate seek-plus-play experiment, not an exact 5.0s sample. Source videos are unaffected; continuous motion QA remains pending.

## Support evidence, if the Codex error recurs

Most recent recorded failed request: 2026-09-23 11:35:39 Asia/Taipei, `gpt-6-astra`, request ID `c0bbb58c-f618-488d-8475-e60b4c73d27a`. Earlier `gpt-6-sol` failure: 11:34:10, request ID `ea3d64af-b501-4321-a7ee-aeb1b1b6b16e`. Do not include authentication files, signed asset URLs, or full conversation logs in a support report.
