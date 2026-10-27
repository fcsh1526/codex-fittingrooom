# Fifth-look full-to-half research append — v1 rendered, awaiting user feedback

2026-10-22: v1/review.mp4 rendered and sampled by root;511f/21.2917s, SHA e4ed855809463e9c8421c5c7d4292f62bdf3f12f1c5f30af8f5c0e0a4edd32dc. See root_visual_review.json and user_review_request.json. Original full-normal-speed visual/user approval remains pending.

Only run after root inspects the **new** `../F05_half_source.mp4` and permits it in a research edit. Do not substitute any old F05 source. The builder stops without creating an output when the new source is missing, its exact hash differs, or its native format is not upright 720×1280 at24fps with at least144decoded frames.

## Fixed edit

- Accepted four-look film SHA`3c0f3fa5bb0c90d0d9b5d434ada37cd5dbe130658d5bff24c01143feb77f1f94`: frames[0,367) unchanged in composition.
- Output[367,385): accepted prefix[367,385) blends into NEW F05[0,18),0.75seconds, incoming alpha`(i+1)/18`.
- Output[385,511): NEW F05[18,144). Total511frames /21.2917seconds.
- Native frame order/full raster; no crop, zoom, retime, freeze, text or audio. Camera push-in must exist in the new source itself.
- Original files are read only. New version output is exclusive; existing/partial versions cause a stop.

## Use after source review

From this folder in PowerShell, replace the hash with the exact downloaded source hash:

```powershell
& 'C:/Users/Brandon_ChangChien/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' ./build_review.py --source-sha 'EXACT_LOWERCASE_SHA256' --preflight-only
& 'C:/Users/Brandon_ChangChien/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' ./build_review.py --source-sha 'EXACT_LOWERCASE_SHA256' --source-qa-eligible --version v1
```

Output: `v1/review.mp4`, `v1/edit_receipt.json`, and `v1/QA/` with25uniform checkpoints, dense J45 overlap plus8frames on each side, F05progress sheet and native frames. All511decoded output frames are compared to the intended composite using the established CRF18codec tolerance; the367pure prefix frames get separate fidelity statistics. This is expected lossy re-encoding, not pixel or byte identity of output frames.

Full decoding / fidelity success is technical verification only. Root must still inspect full-outfit reading time, continuous push-in, face/clothes/bag, gait, background and J45; complete normal-speed playback and user approval remain separate. No Drive/GitHub/IG action is included.
