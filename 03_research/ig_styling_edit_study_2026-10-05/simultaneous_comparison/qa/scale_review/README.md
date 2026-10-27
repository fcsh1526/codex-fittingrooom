# M02 parallel comparison: size review

Reviewed existing native A/B PNGs at frames0,36,72,108,143 and output v2 midpoint. Manual estimates only (approximately ±4px); no segmentation or continuous-playback pass.

Left/A is typically larger after its opening step: its head is about15–19 native pixels higher and lowest shoe about18–21px lower than B. The initial frame is an exception because both heads start at the same height while feet/stances differ. A single fixed correction can improve the normal comparison phase; it cannot make every pose identical without changing the native motion.

Root's proposed A wider crop `[132,0,488,1280]` into nominal352×924 at fixed y176, with B retained as `[145,0,470,1280]` into nominal352×958 at y161, reduces A's scale about3.69%. The inspected later head/foot pairs become approximately1–4 output pixels apart. The opening remains about12px different at head top and5px at lowest shoe; this should be reviewed at normal speed and recorded, rather than hidden by animated correction.

Expanding A's horizontal window from145..615 to132..620 retains its sampled dress, hands and bag and does not introduce a new crop in these five frames. Actual rounded output dimensions and all motion boundaries still require root's new render QA. Keep all144 selected native frames at24fps with unchanged actions/speed. No video or cloud files were changed in this review.

Detailed measurements and nominal transformed coordinates: `manual_scale_estimates.json`.
