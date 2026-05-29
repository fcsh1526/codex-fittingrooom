# Canva Panorama Carousel SOP

Purpose: create a continuous Instagram carousel that feels like one wide editorial canvas split into 5 slides.

## Canvas Setup

Create a custom Canva design:

```text
5400 x 1350 px
```

This exports to:

```text
5 slides x 1080 x 1350 px
```

Add vertical guides at:

```text
x = 1080
x = 2160
x = 3240
x = 4320
```

Keep important text at least `80 px` away from each guide.

## Placeholder Fields

Use one independent text box per placeholder:

```text
{{slide1_title}}
{{slide1_subtitle}}
{{slide1_disclosure}}

{{slide2_kicker}}
{{slide2_title}}
{{slide2_body}}

{{slide3_kicker}}
{{slide3_title}}
{{slide3_body}}

{{slide4_kicker}}
{{slide4_title}}
{{slide4_body}}

{{slide5_title}}
{{slide5_cta}}
{{slide5_note}}
{{slide5_disclosure}}
```

Do not put multiple placeholders in the same text box unless they must share the same font size and layout.

## Weekly Automation Flow

1. Perplexity publishes the weekly trend report.
2. Codex imports the weekly CSV / prompt rows.
3. User generates Grok images and places them in Google Drive.
4. Codex reviews image quality and selects assets.
5. User duplicates the Canva panorama template.
6. User replaces image assets in Canva.
7. Codex reads the Canva design and replaces placeholders.
8. User previews and approves.
9. Codex saves the Canva design.
10. User uses Canva slicing/cutting app to export 5 images.
11. User publishes to Instagram.
12. Codex records metrics and prepares Day 6 commerce links.

## Design Rules

- Use photo-led editorial layout.
- Keep body text short.
- Use Traditional Chinese for IG and Xiaohongshu.
- Use English only for small editorial labels like `LOOK 01`, `INNER LAYER`, or `ACCESSORIES`.
- Always include `AI 虛擬穿搭示意`.
- Do not claim the AI outfit is an exact real product.
- Use wording such as `同風格單品`, `類似款`, or `替代款`.

## W21-P007 Field Values

```text
slide1_title = 沙色亞麻套裝
slide1_subtitle = 有精神，但不會太正式
slide1_disclosure = AI 虛擬穿搭示意
slide2_kicker = LOOK 01
slide2_title = 落肩西外 + 高腰寬褲
slide2_body = 比例乾淨，正式感剛好
slide3_kicker = INNER LAYER
slide3_title = 米白緞面背心
slide3_body = 比白 T 更精緻，下班約會也不突兀
slide4_kicker = ACCESSORIES
slide4_title = 巧克力棕包 + 裸色鞋
slide4_body = 棕色讓整套更穩，裸色鞋延伸腿部比例
slide5_title = 想看同風格清單？
slide5_cta = 留言「沙色套裝」
slide5_note = 我整理平價 / 質感 / 替代款
slide5_disclosure = AI 虛擬穿搭示意
```

## Common Problems

Wrong canvas size:

- `5400 x 1080` creates 5 square slides.
- `5400 x 1350` creates 5 portrait IG slides.

Placeholder typo:

- Wrong: `{{{{slide2_body}}}}`
- Correct: `{{slide2_body}}`

Text near slice boundary:

- Move it inward by at least `80 px`.
