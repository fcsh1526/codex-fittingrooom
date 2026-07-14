# Perplexity Weekly Auto-Publish Schedule

Status: pending user confirmation in Perplexity.

## Purpose

The weekly research task can finish inside the Perplexity workspace without deploying the public site. Codex only consumes the public bridge at:

```text
https://mika-lin-weekly.pplx.app/data/index.json
```

The report is not complete until the current ISO week is present in the public index and its HTML and CSV URLs return successfully.

## Recommended Perplexity Schedule

- Run every Monday after the research task, currently proposed at 08:20 Asia/Taipei.
- Use the Perplexity execution mode that can call `deploy_website` and `publish_website`.
- Deploy all content from `fashion-weekly/dist/public` to site id `3978c987-c0cd-4d05-8d30-afabf1cf2af6`.
- Keep all previous week files.

## Required Safety Checks

Before deploy:

1. Calculate the current ISO 8601 week.
2. Confirm `data/YYYY-WXX.csv` and `weeks/YYYY-WXX.html` exist.
3. Confirm the CSV has at least 20 data rows and the fixed schema.
4. If the files are not ready, wait 20 minutes and retry once instead of republishing the previous week as current.

After publish:

1. Verify the weekly HTML URL returns 200.
2. Verify the weekly CSV URL returns 200.
3. Verify `data/index.json` resolves the current ISO week as the latest item.
4. Send an in-app success or failure notification with the three public URLs.

The task must be idempotent: if the current week is already live and valid, verify it and exit without creating duplicate index entries.
