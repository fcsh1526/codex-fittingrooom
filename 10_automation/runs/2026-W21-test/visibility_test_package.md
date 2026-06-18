# Visibility Test Package

Created: `2026-06-18`
Run folder: `10_automation\runs\2026-W21-test`
Source carousel: `2026-W21-test-002`
Prompt ID: `W21-P002`

## Purpose

Use one simple post to test whether Instagram can distribute this account at all. Do not use a panorama carousel for this test.

## Image

- Recommended file: `IMG_1455.JPG`
- Drive URL: https://drive.google.com/file/d/1N_hpdxNvz1DebbwNf--ISkuKLxBp3zMT/view?usp=drivesdk

## Instagram Caption

```text
上班不想太正式，奶油白西裝套裝可以嗎？

這套是 AI 虛擬穿搭示意，我想測試「輕正式通勤」方向：有整理過，但不會像面試套裝。

你會穿這種奶油白西裝套裝出門嗎？
留言 1 = 會
留言 2 = 不會

AI 虛擬穿搭示意，非真人試穿。
```

## Hashtags

```text
#通勤穿搭 #上班穿搭 #女生穿搭 #西裝外套 #寬褲穿搭 #小資穿搭 #AI穿搭 #虛擬穿搭 #穿搭靈感 #每日穿搭
```

## First Comment

```text
想看同風格清單可以留言「通勤套裝」，我會整理平價 / 質感 / 替代款。
AI 虛擬穿搭示意，非真人試穿。
```

## Threads Backup

```text
上班不想太正式，奶油白西裝套裝可以嗎？

我在測 AI 虛擬穿搭帳號的通勤風格方向。你會穿這種搭配出門嗎？留言 1=會，2=不會。

AI 虛擬穿搭示意，非真人試穿。
```

## Publish Checklist

1. Confirm Instagram account is public and Account Status has no restriction.
2. Publish this as one single-image post.
3. Add the first comment immediately.
4. Share once to Story.
5. Send to 3-5 trusted people for a clean visibility check.
6. Record metrics after 6 hours and 24 hours.

## Metrics Command Template

Replace `POST_URL`, `YYYY/MM/DD HH:mm`, `YYYY-MM-DD`, and metric numbers.

```powershell
powershell -ExecutionPolicy Bypass -File 10_automation\mika_weekly.ps1 `
  -Action metrics `
  -RunDir 10_automation\runs\2026-W21-test `
  -Week 2026-W21-test `
  -CarouselId 2026-W21-test-002-visibility-01 `
  -PostUrl "POST_URL" `
  -PublishedAt "YYYY/MM/DD HH:mm" `
  -RecordMetrics `
  -MeasuredAt YYYY-MM-DD `
  -HoursAfterPublish 24 `
  -Reach 0 `
  -Likes 0 `
  -Saves 0 `
  -Comments 0 `
  -Shares 0
```

## Pass / Fail

- Pass: `reach >= 20`
- Strong pass: `reach >= 100`, `saves >= 1`, or `comments >= 1`
- Fail: `reach = 0` after account audit, Story share, and trusted-person seed traffic
