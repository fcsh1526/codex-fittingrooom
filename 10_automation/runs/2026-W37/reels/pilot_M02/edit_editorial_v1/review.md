# M02 L01 editorial two-shot review

Review candidate, not a QA pass or final Reel. Formal Reel still needs the same model's L02.

- Source 1: `../videos/S01_editorial_02.mp4`, selected 0–3.00 s. The later source interval is excluded because book cover/pages lift despite a no-lift prompt.
- Source 2: `../videos/S02_editorial_01.mp4`, selected 1.25–4.75 s. The initial toothy smile is excluded to reduce the expression jump from S01.
- Output: `M02_L01_S01_S02_clean_v1.mp4`, 6.5 s target, 720×1280 at 24 fps, direct cut, no captions or source audio. Rendering uses `10_automation/assemble_reel_sample.py`.
- QA: `qa_cut/checkpoints.jpg` samples 2.50–3.50 s across the cut. At the cut, gaze and outfit direction broadly match. Head angle, hand/book geometry and smile still change slightly. Visual sample requires normal-speed human review for the perceived jump, pacing and identity; extracted frames alone cannot approve it.
- Do not add a dissolve or push transition to mask a mismatched frame. If the cut fails, refine the S02 starting image/selected interval before another motion generation.
