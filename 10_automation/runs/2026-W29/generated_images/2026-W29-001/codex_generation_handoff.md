# Codex Generation Handoff - 2026-W29-001 / M01

Use this file to generate the carousel image candidates inside Codex.

## Reference Images

Attach both approved reference start images to the image-generation request:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
```

## Output Filenames

Save generated candidates as:

```text
2026-W29-001_M01_v2_candidate_A.png
2026-W29-001_M01_v2_candidate_B.png
2026-W29-001_M01_v2_candidate_C.png
```

## Candidate Prompts

Candidate A: safest full-body daily lifestyle image

Attach both reference start images to the image-generation request. File paths alone are not enough:
- Face anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
- Full-body anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
- Wardrobe-lock reference: Candidate A is created in this step

Create a realistic vertical 4:5 lifestyle fashion image for Mira, an AI fashion magazine brand.

Use internal model M01 only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
Prompt visual age language: early 20s

Reference-anchor use lock:
The face image locks identity, facial geometry, skin character, and hair baseline only. The full-body image locks identity and body proportions only. Do not copy the references' neutral expression, straight-on passport angle, centered stance, hand position, studio background, lighting, or reference outfit. Preserve identity while creating a genuinely new lifestyle photograph.

Body proportion lock:
Treat the approved full-body anchor as an anatomical measurement reference, not merely a style reference. Match its head size relative to total height, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not infer or exaggerate anatomy from the new high-waisted clothing. Do not shrink the head, narrow the torso, raise the crotch, lengthen the thighs or shins, or create fashion-illustration / nine-head proportions unless they are visibly present in the approved anchor. A, B, and C must show the same body proportions.

Camera geometry lock:
Use a normal-to-short-telephoto 70mm full-frame-equivalent perspective. Keep the camera at lower-chest to sternum height with a level optical axis, no upward or downward tilt. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation. Keep the same focal length, camera height, subject distance, horizon, and person scale across A, B, and C; movement should be mostly lateral rather than toward the lens. The crown-to-sole figure should occupy about 78-82% of the frame height with comfortable headroom and floor visible beneath both shoes.

Age rendering rules:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Trend and outfit:
Global trend signal: 輕透層次 透膚疊穿
Clothing item: 透膚網紗長袖上衣 ＋ 緞面細肩帶背心 ＋ 寬褲
Palette: mist gray + cream
Fabric: mesh + satin
Fit: slim top / relaxed bottom
Occasion: 通勤
Styling rules: keep outfit logo-free; emphasize material texture and layered styling; balanced proportions (fitted top + volume bottom or vice versa)

Outfit continuity lock:
Candidates A, B, and C are three photographs from the same outfit session. Keep the exact same top layers, neckline, sleeve length, trousers or skirt, hem length, fabric, palette, shoes, bag, jewelry, and scarf placement in all three candidates. Only lateral position, body angle, pose, gaze, hand interaction, and expression may change. Do not change camera geometry or reinterpret the trend into a different outfit for B or C.

Scene:
Use a believable daily-life fashion magazine scene that fits the occasion and outfit. Existing scene hint: clean studio with soft daylight, minimal props. Do not force Taiwan if another global daily setting better fits the trend, but keep the image wearable and relatable.

Lighting integration lock:
First establish one physically plausible key-light source inside the scene, such as daylight from a visible window or open street. Its direction and color temperature must affect the entire person consistently: forehead, cheeks, nose shadow, neck, arms, clothing folds, shoes, and bag. The side facing away from the source must be visibly darker and pick up the scene's ambient color. Add grounded contact shadows under both shoes and natural cast shadows on nearby surfaces. Match subject contrast, white balance, grain, depth of field, and edge softness to the background. The person must look photographed in the location, never cut out and pasted onto a background. No frontal beauty light, ring-light catchlights, shadowless face, studio fill, halo edges, or independent subject lighting.

Composition:
Full outfit readable within one second. Natural posture. Real skin texture. Clothes are clear. Face remains consistent with the attached face anchor, and measured body proportions remain consistent with the attached full-body anchor. The environment fills the 4:5 frame edge to edge, while the crown-to-sole figure occupies about 78-82% of frame height. Keep both shoes and floor contact visible with no white border or letterboxing.

Candidate-specific direction:
Use an asymmetric three-quarter standing pose with a natural weight shift. Keep the eyes attentive and add a restrained micro-smile or relaxed engaged expression. At least one hand should interact naturally with the bag, jacket, pocket, railing, or nearby object; do not leave both arms straight and symmetrical.

Avoid:
tiny head, oversized head, supermodel or nine-head proportions, elongated thighs or shins, raised crotch, narrow stretched torso, inconsistent body-to-leg ratio, low camera angle, wide-angle distortion, perspective leg stretching, runway pose, luxury hotel ad, resort fantasy, plastic skin, excessive filters, pasted-on subject, mismatched key light, shadowless face, missing contact shadows, outfit changes between candidates, repeated A/B/C pose, repeated expression, centered ID-photo stance, both arms hanging symmetrically, frozen face, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, visible logos, image text, watermark, wrinkle-based age cues, numeric true-age labels.


---

Candidate B: movement or street-style variation

Attach both reference start images to the image-generation request. File paths alone are not enough:
- Face anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
- Full-body anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
- Wardrobe-lock reference: accepted Candidate A from this same job

Create a realistic vertical 4:5 lifestyle fashion image for Mira, an AI fashion magazine brand.

Use internal model M01 only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
Prompt visual age language: early 20s

Reference-anchor use lock:
The face image locks identity, facial geometry, skin character, and hair baseline only. The full-body image locks identity and body proportions only. Do not copy the references' neutral expression, straight-on passport angle, centered stance, hand position, studio background, lighting, or reference outfit. Preserve identity while creating a genuinely new lifestyle photograph.

Body proportion lock:
Treat the approved full-body anchor as an anatomical measurement reference, not merely a style reference. Match its head size relative to total height, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not infer or exaggerate anatomy from the new high-waisted clothing. Do not shrink the head, narrow the torso, raise the crotch, lengthen the thighs or shins, or create fashion-illustration / nine-head proportions unless they are visibly present in the approved anchor. A, B, and C must show the same body proportions.

Camera geometry lock:
Use a normal-to-short-telephoto 70mm full-frame-equivalent perspective. Keep the camera at lower-chest to sternum height with a level optical axis, no upward or downward tilt. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation. Keep the same focal length, camera height, subject distance, horizon, and person scale across A, B, and C; movement should be mostly lateral rather than toward the lens. The crown-to-sole figure should occupy about 78-82% of the frame height with comfortable headroom and floor visible beneath both shoes.

Age rendering rules:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Trend and outfit:
Global trend signal: 輕透層次 透膚疊穿
Clothing item: 透膚網紗長袖上衣 ＋ 緞面細肩帶背心 ＋ 寬褲
Palette: mist gray + cream
Fabric: mesh + satin
Fit: slim top / relaxed bottom
Occasion: 通勤
Styling rules: keep outfit logo-free; emphasize material texture and layered styling; balanced proportions (fitted top + volume bottom or vice versa)

Outfit continuity lock:
Candidates A, B, and C are three photographs from the same outfit session. Keep the exact same top layers, neckline, sleeve length, trousers or skirt, hem length, fabric, palette, shoes, bag, jewelry, and scarf placement in all three candidates. Only lateral position, body angle, pose, gaze, hand interaction, and expression may change. Do not change camera geometry or reinterpret the trend into a different outfit for B or C.

Scene:
Use a believable daily-life fashion magazine scene that fits the occasion and outfit. Existing scene hint: clean studio with soft daylight, minimal props. Do not force Taiwan if another global daily setting better fits the trend, but keep the image wearable and relatable.

Lighting integration lock:
First establish one physically plausible key-light source inside the scene, such as daylight from a visible window or open street. Its direction and color temperature must affect the entire person consistently: forehead, cheeks, nose shadow, neck, arms, clothing folds, shoes, and bag. The side facing away from the source must be visibly darker and pick up the scene's ambient color. Add grounded contact shadows under both shoes and natural cast shadows on nearby surfaces. Match subject contrast, white balance, grain, depth of field, and edge softness to the background. The person must look photographed in the location, never cut out and pasted onto a background. No frontal beauty light, ring-light catchlights, shadowless face, studio fill, halo edges, or independent subject lighting.

Composition:
Full outfit readable within one second. Natural posture. Real skin texture. Clothes are clear. Face remains consistent with the attached face anchor, and measured body proportions remain consistent with the attached full-body anchor. The environment fills the 4:5 frame edge to edge, while the crown-to-sole figure occupies about 78-82% of frame height. Keep both shoes and floor contact visible with no white border or letterboxing.

Candidate-specific direction:
Capture a candid mid-step or turning moment with visible body movement. Use an off-camera gaze or a brief glance back toward camera, natural hair and fabric motion, and one hand adjusting the bag, scarf, sleeve, or hair. Do not repeat Candidate A's stance or expression.

Avoid:
tiny head, oversized head, supermodel or nine-head proportions, elongated thighs or shins, raised crotch, narrow stretched torso, inconsistent body-to-leg ratio, low camera angle, wide-angle distortion, perspective leg stretching, runway pose, luxury hotel ad, resort fantasy, plastic skin, excessive filters, pasted-on subject, mismatched key light, shadowless face, missing contact shadows, outfit changes between candidates, repeated A/B/C pose, repeated expression, centered ID-photo stance, both arms hanging symmetrically, frozen face, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, visible logos, image text, watermark, wrinkle-based age cues, numeric true-age labels.


---

Candidate C: closer outfit-detail-friendly variation while keeping the outfit readable

Attach both reference start images to the image-generation request. File paths alone are not enough:
- Face anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_face.png
- Full-body anchor: C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\02_brand\reference_models\M01_start_v4_full.png
- Wardrobe-lock reference: accepted Candidate A from this same job

Create a realistic vertical 4:5 lifestyle fashion image for Mira, an AI fashion magazine brand.

Use internal model M01 only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
East Asian woman with an early-20s youthful adult look, fresh soft cheeks, a lighter jawline, natural warm skin with visible human texture, jaw-length dark brown bob with natural movement, approachable practical expression, petite-to-medium healthy proportions, clean casual polish.
Prompt visual age language: early 20s

Reference-anchor use lock:
The face image locks identity, facial geometry, skin character, and hair baseline only. The full-body image locks identity and body proportions only. Do not copy the references' neutral expression, straight-on passport angle, centered stance, hand position, studio background, lighting, or reference outfit. Preserve identity while creating a genuinely new lifestyle photograph.

Body proportion lock:
Treat the approved full-body anchor as an anatomical measurement reference, not merely a style reference. Match its head size relative to total height, shoulder width, torso length, natural waist and hip placement, crotch height, knee height, thigh length, lower-leg length, arm length, and hand size. Do not infer or exaggerate anatomy from the new high-waisted clothing. Do not shrink the head, narrow the torso, raise the crotch, lengthen the thighs or shins, or create fashion-illustration / nine-head proportions unless they are visibly present in the approved anchor. A, B, and C must show the same body proportions.

Camera geometry lock:
Use a normal-to-short-telephoto 70mm full-frame-equivalent perspective. Keep the camera at lower-chest to sternum height with a level optical axis, no upward or downward tilt. No low angle, wide angle, phone-lens distortion, forced perspective, or leg elongation. Keep the same focal length, camera height, subject distance, horizon, and person scale across A, B, and C; movement should be mostly lateral rather than toward the lens. The crown-to-sole figure should occupy about 78-82% of the frame height with comfortable headroom and floor visible beneath both shoes.

Age rendering rules:
Express age through styling and presence, NOT wrinkles.
East Asian women look significantly younger than Western age norms.
Skin is smooth and well-maintained.

Trend and outfit:
Global trend signal: 輕透層次 透膚疊穿
Clothing item: 透膚網紗長袖上衣 ＋ 緞面細肩帶背心 ＋ 寬褲
Palette: mist gray + cream
Fabric: mesh + satin
Fit: slim top / relaxed bottom
Occasion: 通勤
Styling rules: keep outfit logo-free; emphasize material texture and layered styling; balanced proportions (fitted top + volume bottom or vice versa)

Outfit continuity lock:
Candidates A, B, and C are three photographs from the same outfit session. Keep the exact same top layers, neckline, sleeve length, trousers or skirt, hem length, fabric, palette, shoes, bag, jewelry, and scarf placement in all three candidates. Only lateral position, body angle, pose, gaze, hand interaction, and expression may change. Do not change camera geometry or reinterpret the trend into a different outfit for B or C.

Scene:
Use a believable daily-life fashion magazine scene that fits the occasion and outfit. Existing scene hint: clean studio with soft daylight, minimal props. Do not force Taiwan if another global daily setting better fits the trend, but keep the image wearable and relatable.

Lighting integration lock:
First establish one physically plausible key-light source inside the scene, such as daylight from a visible window or open street. Its direction and color temperature must affect the entire person consistently: forehead, cheeks, nose shadow, neck, arms, clothing folds, shoes, and bag. The side facing away from the source must be visibly darker and pick up the scene's ambient color. Add grounded contact shadows under both shoes and natural cast shadows on nearby surfaces. Match subject contrast, white balance, grain, depth of field, and edge softness to the background. The person must look photographed in the location, never cut out and pasted onto a background. No frontal beauty light, ring-light catchlights, shadowless face, studio fill, halo edges, or independent subject lighting.

Composition:
Full outfit readable within one second. Natural posture. Real skin texture. Clothes are clear. Face remains consistent with the attached face anchor, and measured body proportions remain consistent with the attached full-body anchor. The environment fills the 4:5 frame edge to edge, while the crown-to-sole figure occupies about 78-82% of frame height. Keep both shoes and floor contact visible with no white border or letterboxing.

Candidate-specific direction:
Use an outfit-detail-friendly three-quarter pose at the same camera height, lens, distance, and subject scale as A and B. The model may lean lightly, pause beside furniture, or turn across the frame while keeping the full outfit readable; Canva will create any closer crop later. Use a warm attentive expression different from A and B; avoid a centered passport-photo stance.

Avoid:
tiny head, oversized head, supermodel or nine-head proportions, elongated thighs or shins, raised crotch, narrow stretched torso, inconsistent body-to-leg ratio, low camera angle, wide-angle distortion, perspective leg stretching, runway pose, luxury hotel ad, resort fantasy, plastic skin, excessive filters, pasted-on subject, mismatched key light, shadowless face, missing contact shadows, outfit changes between candidates, repeated A/B/C pose, repeated expression, centered ID-photo stance, both arms hanging symmetrically, frozen face, white border, letterboxing, sexualized pose, childlike styling, celebrity likeness, visible logos, image text, watermark, wrinkle-based age cues, numeric true-age labels.


## After Generation

Update:

```text
C:\Users\Brandon_ChangChien\Documents\Codex\人物試衣間\10_automation\runs\2026-W29\generated_images\2026-W29-001\review_sheet.csv
```