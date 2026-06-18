# Automation Hub

Purpose: make the weekly Mika Lin workflow repeatable with less discussion and fewer manual decisions.

The current priority is not monetization. The priority is:

```text
stable character + weekly fashion trend + Grok image prompts + polished Instagram carousel + basic reach test
```

Only after Instagram or another channel gets non-zero reach should affiliate links and product lists become the main work.

## Weekly Inputs

Each week needs these inputs:

1. Perplexity weekly trend URL or CSV.
2. One selected trend / outfit direction.
3. 3-5 Grok output images in Google Drive.
4. One Canva panorama template copy.
5. A final Instagram post URL and metrics after publishing.

## Weekly Outputs

Each week should produce:

1. `weekly_content_packet.csv`
2. 3-5 Grok prompts
3. Canva placeholder values
4. IG carousel caption and hashtags
5. Drive asset inventory
6. Publish record
7. Metrics record

## Files In This Folder

- `weekly_carousel_pipeline.md`: the fixed weekly production workflow.
- `weekly_content_packet_template.csv`: one-row template for a weekly carousel packet.
- `canva_placeholder_values_template.csv`: field values that Codex can paste into Canva.
- `weekly_handoff_checklist.md`: what the user should provide each week.
- `generate_canva_placeholders.py`: converts a weekly content packet CSV into Canva placeholder values.
- `build_weekly_packet.py`: converts rows from `04_prompts/item_prompt_database.csv` into a weekly run folder.

## Placeholder Generator

Example:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\generate_canva_placeholders.py `
  --input 10_automation\examples\weekly_content_packet_example.csv `
  --output tmp\generated_canva_placeholder_test.csv
```

Expected result:

```text
Wrote 1 row(s) to tmp\generated_canva_placeholder_test.csv
```

## Weekly Packet Builder

Use this when the weekly Perplexity prompts have already been imported into `04_prompts/item_prompt_database.csv`.

Example:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\build_weekly_packet.py `
  --week 2026-W21-test `
  --limit 2 `
  --output-dir 10_automation\runs\2026-W21-test
```

Expected result:

```text
Wrote 2 carousel packet(s) to 10_automation\runs\2026-W21-test
```

Generated files:

- `weekly_content_packet.csv`
- `grok_prompts.md`
- `canva_placeholder_values.csv`
- `README.md`

## Operating Rule

Do not rebuild the workflow every week.

Every week should follow:

```text
Perplexity -> prompt packet -> Grok images -> Canva carousel -> IG post -> metrics -> decide next test
```
