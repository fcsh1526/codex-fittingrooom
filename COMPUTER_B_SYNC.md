# Computer B Sync And Handoff

Updated: 2026-07-17

Computer A and computer B use the same GitHub `main` branch and production workflow.

Canonical instructions: `10_automation/CANONICAL_WORKFLOW.md`.

## Start On Computer B

```powershell
git pull origin main
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action dashboard
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action queue
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action cockpit
```

Open:

```text
10_automation/CANONICAL_WORKFLOW.md
10_automation/DAILY_COCKPIT.html
10_automation/PUBLISH_QUEUE.md
CURRENT_STATUS.md
```

Do not follow an older W27/W29 chat message when repository files disagree.

## Local Skill Check

Repository copy: `11_skills/mira-image-daily/`.

Local installation: `%USERPROFILE%\.codex\skills\mira-image-daily\`.

If computer B does not have the skill, install/copy the repository skill before image generation. Both copies must remain equivalent.

## Current Contract

```text
Image provider: Codex built-in image generation
Grok: inactive
Drive: optional archive only
Canva: draft transaction -> preview -> user approval -> commit
Manual boundary: Canva three-slice export and Instagram posting
Current verified week: W29
W29: all five carousels ready_for_manual_export
```

## Continue Work

1. Read `PUBLISH_QUEUE.md` and use its top item.
2. `needs_image_asset_selection`: follow Phases 2-4 of the canonical workflow.
3. `needs_canva_frame_review`: create a Canva draft but never save without preview approval.
4. `ready_for_manual_export`: do not regenerate or refill; only slice, export, and publish.
5. Record every accepted state and Canva URL in the weekly run files.

## End Work On Computer B

```powershell
git status --short
git diff --check
git add <only intended files>
git commit -m "Describe the completed checkpoint"
git push origin main
```

Do not stage unrelated drafts or historical experiments.

Must reach GitHub:

- accepted A/B/C and review status;
- exact Canva-ready files and manifest;
- Canva design URL and committed transaction status;
- weekly packet, daily queue, asset slots, and asset inventory;
- publish URL/time if posted;
- any workflow change.

## Quick Validation

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action validate -Week 2026-WXX -RequireAssets
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\10_automation\mika_weekly.ps1 -Action smoke-test
```

Required weekly result: `Validation pass: 0 error(s), 0 warning(s).`
