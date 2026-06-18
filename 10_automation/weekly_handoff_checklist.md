# Weekly Handoff Checklist

When restarting work in Codex, paste this information:

```text
Week ID:
Perplexity weekly URL / CSV / markdown export:
Chosen trend / outfit:
Google Drive folder with Grok images:
Canva design URL:
Instagram account status:
Last post reach:
Anything stuck:
```

## Minimum Required To Continue

Codex can continue with only:

```text
Week ID
Perplexity weekly URL / CSV / markdown export
```

If the Perplexity export is ready, Codex should run:

```text
10_automation/run_weekly_pipeline.py
```

and produce the weekly Grok prompts, Canva placeholders, platform drafts, and publish checklist.

Before image production, confirm:

```text
quality_report.md status = pass
```

## If Grok Images Are Not Ready

Codex should output:

- `grok_prompts.md`
- one recommended cover concept
- `canva_placeholder_values.csv`
- `post_drafts.md`
- `publish_checklist.md`

## If Canva Is Not Ready

Codex should output:

- 5-slide placeholder values
- layout notes for `5400 x 1350`
- short IG caption

## If IG Reach Is Still Zero

Do not start affiliate links.

Run:

```text
09_sops/instagram_zero_reach_recovery.md
```
