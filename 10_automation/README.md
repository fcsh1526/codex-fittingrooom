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
- `import_perplexity_export.py`: imports a Perplexity CSV or markdown CSV block into `04_prompts/item_prompt_database.csv`.
- `generate_canva_placeholders.py`: converts a weekly content packet CSV into Canva placeholder values.
- `build_weekly_packet.py`: converts rows from `04_prompts/item_prompt_database.csv` into a weekly run folder.
- `validate_weekly_run.py`: validates required files, missing fields, disclosure, prompt safety terms, hashtag count, and Canva text length.
- `run_weekly_pipeline.py`: optional one-command importer + weekly packet builder.

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
- `post_drafts.md`
- `publish_checklist.md`
- `README.md`

## Perplexity Importer

Use this when Perplexity provides a direct CSV export, a downloaded CSV, or a markdown report that contains a fenced CSV block.

Dry run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\import_perplexity_export.py `
  --source 10_automation\examples\perplexity_export_example.md `
  --week 2026-W25 `
  --dry-run
```

Import:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\import_perplexity_export.py `
  --source path_or_url_to_perplexity_export `
  --week 2026-W25
```

The importer upserts rows by `(week, id)` so re-running the same week replaces that week's matching prompt rows instead of duplicating them.

## One-Command Weekly Pipeline

Use this when a Perplexity export is ready and you want the full weekly packet in one run:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\run_weekly_pipeline.py `
  --week 2026-W25 `
  --perplexity-source path_or_url_to_perplexity_export `
  --limit 2
```

Output:

```text
10_automation/runs/2026-W25/
```

The one-command pipeline runs quality validation by default and writes:

```text
quality_report.md
quality_report.json
```

To validate an existing run folder:

```powershell
& 'C:\Users\Brandon_ChangChien\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  10_automation\validate_weekly_run.py `
  --run-dir 10_automation\runs\2026-W21-test `
  --min-rows 2
```

## Operating Rule

Do not rebuild the workflow every week.

Every week should follow:

```text
Perplexity -> prompt packet -> Grok images -> Canva carousel -> IG post -> metrics -> decide next test
```
