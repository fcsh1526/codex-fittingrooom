# W26 M02 Polka Dot Image Test Brief

Purpose: first image-generation test for the new Mira daily magazine workflow.

Source item:

```text
carousel_id = 2026-W26-002
model_profile_id = M02
trend = 波點洋裝/套裝（Polka Dots）
clothing_item = 波點洋裝
occasion = 約會 / 週末咖啡廳
palette = 黑白波點 / small red accent
fabric = satin or chiffon
fit = straight or subtle A-line
```

## M02 Production Profile

Use this only for image consistency. Do not publish the model ID or role.

```text
Taiwanese woman, mid to late 20s, slightly round face, long dark brown hair with soft movement, natural makeup, relaxed posture, average height and healthy slim build.
```

The reader should feel:

```text
This is a weekend/date outfit I could imagine wearing in Taiwan, not a celebrity shoot.
```

## Candidate A - Cafe Window Full Body

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand in Taiwan.

Use internal model M02 only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
Taiwanese woman, mid to late 20s, slightly round face, long dark brown hair with soft movement, natural makeup, relaxed posture, average height and healthy slim build.

Outfit:
A black-and-white polka dot midi dress, satin or chiffon texture, straight or subtle A-line fit. Add one small red accent such as lipstick, slim belt, small bag charm, or simple flats detail. Keep the whole outfit under three main colors.

Scene:
Taipei cafe window in soft afternoon daylight, quiet and believable, not a luxury venue. The model is standing naturally near the window, one hand lightly holding a small shoulder bag, full outfit visible.

Composition:
Vertical 4:5 image. Full outfit readable within one second. Natural posture. Soft daylight. Real skin texture. Clothes are clear. Face is natural, calm, and approachable. Fashion magazine quality, but everyday and wearable.

Avoid:
supermodel proportions, runway pose, luxury resort, plastic skin, flawless beauty render, excessive filters, sexualized pose, childlike styling, celebrity likeness, visible logos, text, watermark, bridal styling, heavy glamour pose.
```

## Candidate B - Bookstore Street Movement

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand in Taiwan.

Use internal model M02 only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
Taiwanese woman, mid to late 20s, slightly round face, long dark brown hair with soft movement, natural makeup, relaxed posture, average height and healthy slim build.

Outfit:
A black-and-white polka dot dress, satin or chiffon texture, straight or subtle A-line fit, styled with Mary Jane flats or simple ballet flats and a small shoulder bag. Add a restrained red accent only if it looks natural.

Scene:
Quiet Taiwan bookstore street or cafe street in afternoon light. The model is walking slowly, dress movement visible, posture relaxed and unposed. Background should be softly detailed but not distracting.

Composition:
Vertical 4:5 image. Outfit must be readable from head to shoes. Keep camera around chest height, not extreme low angle. Fashion magazine realism with ordinary-life warmth.

Avoid:
supermodel proportions, runway pose, luxury resort, plastic skin, flawless beauty render, excessive filters, sexualized pose, childlike styling, celebrity likeness, visible logos, text, watermark, bridal styling, heavy glamour pose.
```

## Candidate C - Department Store Fitting Area

```text
Create a realistic vertical lifestyle fashion image for Mira, an AI fashion magazine brand in Taiwan.

Use internal model M02 only as a private production profile. Do not render or include the model ID, name, text, watermark, logo, or caption in the image.

Model profile:
Taiwanese woman, mid to late 20s, slightly round face, long dark brown hair with soft movement, natural makeup, relaxed posture, average height and healthy slim build.

Outfit:
A black-and-white polka dot midi dress with soft satin or chiffon texture, straight or subtle A-line fit. Keep styling simple: small shoulder bag, ballet flats or Mary Janes, delicate earrings, no visible logos.

Scene:
Clean Taiwan department store fitting area or mirror corner, warm neutral light, realistic and understated. The model is adjusting the bag strap or checking the dress silhouette, not posing like a model.

Composition:
Vertical 4:5 image. Full outfit readable, with room for future crop details of dress fabric, bag, or shoes. Natural skin texture and believable lighting.

Avoid:
supermodel proportions, runway pose, luxury resort, plastic skin, flawless beauty render, excessive filters, sexualized pose, childlike styling, celebrity likeness, visible logos, text, watermark, bridal styling, heavy glamour pose.
```

## Review Instruction

After generating candidates, save usable files under:

```text
10_automation/runs/2026-W26/generated_images/
```

Then fill:

```text
10_automation/runs/2026-W26/image_review_template.csv
```

Minimum acceptance:

```text
outfit_clarity >= 4
ai_realism >= 4
reader_relatability >= 4
```

If none pass, revise toward more ordinary daily-life realism before touching Canva.

