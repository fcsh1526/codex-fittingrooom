# Mira AI Fashion Carousel Automation

This repository is the shared production workspace for computer A, computer B, and Codex.

## Start Here

1. Pull GitHub:

```powershell
git pull origin main
```

2. Read the canonical workflow:

```text
10_automation/CANONICAL_WORKFLOW.md
```

3. Refresh the current operating view:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action dashboard
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action queue
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action cockpit
```

4. Open:

```text
10_automation/DAILY_COCKPIT.html
10_automation/PUBLISH_QUEUE.md
CURRENT_STATUS.md
```

Computer B instructions: `COMPUTER_B_SYNC.md`.

## Active Workflow

```text
Perplexity weekly trends
-> five ISO-week carousel packets
-> M01-M05 rotation
-> Codex exact-frame A/B/C images
-> approved Canva v3 duplicate
-> manual three-slice export
-> Instagram Carousel
```

Production rules:

- Codex is the active image generator; Grok is inactive.
- Google Drive is optional archive storage.
- GitHub is the cross-computer source of truth.
- Canva is saved only after the user sees and approves the draft.
- Canvas is `3240x1350`, exported as three `1080x1350` slides.
- Zero reach never blocks the next carousel.

## Current Verified Reference

W29 is the first fully verified exact-frame week. All five carousels are `ready_for_manual_export`, with weekly validation at zero errors and zero warnings.

Use W29 folders as workflow examples only. Do not reuse their images for future weeks.
