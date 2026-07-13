param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("pipeline", "status", "dashboard", "queue", "today", "brief", "cockpit", "visibility-test", "assets", "image-job", "sync-canva-map", "generate-images", "metrics", "validate", "smoke-test")]
    [string]$Action,

    [string]$Week = "",
    [string]$PerplexitySource = "",
    [string]$PerplexityIndex = "",
    [switch]$UsePerplexityIndex,
    [string]$RunDir = "",
    [string]$RunsDir = "10_automation\runs",
    [string]$TodayOutput = "10_automation\TODAY.md",
    [string]$TodayJson = "10_automation\TODAY.json",
    [string]$TodayDate = "",
    [string]$QueueOutput = "10_automation\PUBLISH_QUEUE.md",
    [string]$QueueJson = "10_automation\PUBLISH_QUEUE.json",
    [string]$QueueCsv = "10_automation\PUBLISH_QUEUE.csv",
    [string]$CockpitHtml = "10_automation\DAILY_COCKPIT.html",
    [string]$CockpitMd = "10_automation\DAILY_COCKPIT.md",
    [string]$VisibilityOutput = "",
    [string]$VisibilityJson = "",
    [string]$Database = "04_prompts\item_prompt_database.csv",
    [int]$Limit = 5,

    [string]$ScoreSheet = "",
    [string]$DriveInventory = "",
    [string]$AssetProvider = "Codex",
    [switch]$SkipImageJobs,
    [string]$DailyId = "",
    [string]$OpenAIModel = "",
    [string]$ImageSize = "1024x1536",
    [string]$ImageQuality = "medium",
    [int]$ImageVariants = 2,
    [switch]$DryRunImages,

    [string]$CarouselId = "",
    [string]$Platform = "Instagram",
    [string]$Format = "Carousel",
    [string]$PostUrl = "",
    [string]$PublishedAt = "",
    [string]$MeasuredAt = "",
    [int]$HoursAfterPublish = 24,
    [int]$Reach = 0,
    [int]$Likes = 0,
    [int]$Saves = 0,
    [int]$Comments = 0,
    [int]$Shares = 0,
    [int]$ProfileVisits = 0,
    [int]$NewFollowers = 0,
    [int]$CtaComments = 0,
    [int]$LinkClicks = 0,
    [string]$GlobalDir = "07_metrics",
    [switch]$RecordMetrics,
    [switch]$RequireAssets
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $ProjectRoot

function Resolve-PythonExe {
    $bundled = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path $bundled) {
        return $bundled
    }
    return "python"
}

function Resolve-RunDir {
    if ($RunDir) {
        return $RunDir
    }
    if ($Week) {
        return "10_automation\runs\$Week"
    }
    throw "RunDir or Week is required for action '$Action'."
}

function Invoke-MikaPython {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptPath,
        [string[]]$ArgsList = @()
    )

    $python = Resolve-PythonExe
    & $python $ScriptPath @ArgsList
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

switch ($Action) {
    "pipeline" {
        if (-not $Week -and -not $UsePerplexityIndex) {
            throw "Week is required for pipeline unless UsePerplexityIndex is set."
        }

        $argsList = @(
            "--database", $Database,
            "--limit", "$Limit"
        )

        if ($Week) {
            $argsList += @("--week", $Week)
        }
        if ($RunDir -or $Week) {
            $resolvedRunDir = Resolve-RunDir
            $argsList += @("--output-dir", $resolvedRunDir)
        }

        if ($PerplexitySource) {
            $argsList += @("--perplexity-source", $PerplexitySource)
        }
        if ($UsePerplexityIndex) {
            $argsList += "--use-perplexity-index"
        }
        if ($PerplexityIndex) {
            $argsList += @("--perplexity-index", $PerplexityIndex)
        }
        if ($ScoreSheet) {
            $argsList += @("--score-sheet", $ScoreSheet)
        }
        if ($DriveInventory) {
            $argsList += @("--drive-inventory", $DriveInventory)
        }
        if ($AssetProvider) {
            $argsList += @("--asset-provider", $AssetProvider)
        }
        if ($SkipImageJobs) {
            $argsList += "--skip-image-jobs"
        }

        Invoke-MikaPython -ScriptPath "10_automation\run_weekly_pipeline.py" -ArgsList $argsList
    }

    "status" {
        $resolvedRunDir = Resolve-RunDir
        Invoke-MikaPython -ScriptPath "10_automation\check_weekly_status.py" -ArgsList @("--run-dir", $resolvedRunDir)
    }

    "dashboard" {
        Invoke-MikaPython -ScriptPath "10_automation\weekly_dashboard.py" -ArgsList @("--runs-dir", $RunsDir)
    }

    "queue" {
        Invoke-MikaPython -ScriptPath "10_automation\publish_queue.py" -ArgsList @("--runs-dir", $RunsDir, "--output-md", $QueueOutput, "--output-json", $QueueJson, "--output-csv", $QueueCsv)
    }

    "today" {
        $argsList = @("--runs-dir", $RunsDir, "--date", $TodayDate, "--today-md", $TodayOutput, "--today-json", $TodayJson, "--queue-md", $QueueOutput, "--queue-json", $QueueJson, "--queue-csv", $QueueCsv, "--output-html", $CockpitHtml, "--output-md", $CockpitMd)
        if (-not $TodayDate) {
            $argsList = @("--runs-dir", $RunsDir, "--today-md", $TodayOutput, "--today-json", $TodayJson, "--queue-md", $QueueOutput, "--queue-json", $QueueJson, "--queue-csv", $QueueCsv, "--output-html", $CockpitHtml, "--output-md", $CockpitMd)
        }
        Invoke-MikaPython -ScriptPath "10_automation\daily_cockpit.py" -ArgsList $argsList
    }

    "cockpit" {
        $argsList = @("--runs-dir", $RunsDir, "--date", $TodayDate, "--today-md", $TodayOutput, "--today-json", $TodayJson, "--queue-md", $QueueOutput, "--queue-json", $QueueJson, "--queue-csv", $QueueCsv, "--output-html", $CockpitHtml, "--output-md", $CockpitMd)
        if (-not $TodayDate) {
            $argsList = @("--runs-dir", $RunsDir, "--today-md", $TodayOutput, "--today-json", $TodayJson, "--queue-md", $QueueOutput, "--queue-json", $QueueJson, "--queue-csv", $QueueCsv, "--output-html", $CockpitHtml, "--output-md", $CockpitMd)
        }
        Invoke-MikaPython -ScriptPath "10_automation\daily_cockpit.py" -ArgsList $argsList
    }

    "brief" {
        $argsList = @("--runs-dir", $RunsDir, "--output-md", $TodayOutput, "--output-json", $TodayJson, "--queue-md", $QueueOutput, "--queue-json", $QueueJson, "--queue-csv", $QueueCsv)
        if ($TodayDate) {
            $argsList += @("--date", $TodayDate)
        }
        Invoke-MikaPython -ScriptPath "10_automation\daily_brief.py" -ArgsList $argsList
    }

    "visibility-test" {
        $resolvedRunDir = Resolve-RunDir
        $argsList = @("--run-dir", $resolvedRunDir)
        if ($CarouselId) {
            $argsList += @("--carousel-id", $CarouselId)
        }
        if ($VisibilityOutput) {
            $argsList += @("--output-md", $VisibilityOutput)
        }
        if ($VisibilityJson) {
            $argsList += @("--output-json", $VisibilityJson)
        }
        Invoke-MikaPython -ScriptPath "10_automation\prepare_visibility_test.py" -ArgsList $argsList
    }

    "assets" {
        $resolvedRunDir = Resolve-RunDir
        $argsList = @("--run-dir", $resolvedRunDir)
        if ($ScoreSheet) {
            $argsList += @("--score-sheet", $ScoreSheet)
        }
        if ($DriveInventory) {
            $argsList += @("--drive-inventory", $DriveInventory)
        }
        if ($AssetProvider) {
            $argsList += @("--provider", $AssetProvider)
        }
        Invoke-MikaPython -ScriptPath "10_automation\select_codex_assets.py" -ArgsList $argsList
    }

    "image-job" {
        $resolvedRunDir = Resolve-RunDir
        $argsList = @(
            "--project-root", ".",
            "--run-dir", $resolvedRunDir,
            "--tool", $AssetProvider
        )
        if ($CarouselId) {
            $argsList += @("--carousel-id", $CarouselId)
        }
        if ($DailyId) {
            $argsList += @("--daily-id", $DailyId)
        }
        Invoke-MikaPython -ScriptPath "11_skills\mira-image-daily\scripts\prepare_daily_image_job.py" -ArgsList $argsList
    }

    "sync-canva-map" {
        $resolvedRunDir = Resolve-RunDir
        Invoke-MikaPython -ScriptPath "10_automation\sync_canva_placeholder_map.py" -ArgsList @("--run-dir", $resolvedRunDir)
    }

    "generate-images" {
        $resolvedRunDir = Resolve-RunDir
        $argsList = @(
            "--run-dir", $resolvedRunDir,
            "--size", $ImageSize,
            "--quality", $ImageQuality,
            "--variants", "$ImageVariants"
        )
        if ($OpenAIModel) {
            $argsList += @("--model", $OpenAIModel)
        }
        if ($DryRunImages) {
            $argsList += "--dry-run"
        }
        Invoke-MikaPython -ScriptPath "10_automation\generate_openai_images.py" -ArgsList $argsList
    }

    "metrics" {
        $resolvedRunDir = Resolve-RunDir
        if (-not $PostUrl) {
            throw "PostUrl is required for metrics."
        }

        $argsList = @(
            "--run-dir", $resolvedRunDir,
            "--platform", $Platform,
            "--format", $Format,
            "--post-url", $PostUrl,
            "--global-dir", $GlobalDir
        )
        if ($Week) {
            $argsList += @("--week", $Week)
        }
        if ($CarouselId) {
            $argsList += @("--carousel-id", $CarouselId)
        }
        if ($PublishedAt) {
            $argsList += @("--published-at", $PublishedAt)
        }
        if ($RecordMetrics) {
            $argsList += @(
                "--record-metrics",
                "--hours-after-publish", "$HoursAfterPublish",
                "--reach", "$Reach",
                "--likes", "$Likes",
                "--saves", "$Saves",
                "--comments", "$Comments",
                "--shares", "$Shares",
                "--profile-visits", "$ProfileVisits",
                "--new-followers", "$NewFollowers",
                "--cta-comments", "$CtaComments",
                "--link-clicks", "$LinkClicks"
            )
            if ($MeasuredAt) {
                $argsList += @("--measured-at", $MeasuredAt)
            }
        }

        Invoke-MikaPython -ScriptPath "10_automation\record_post_metrics.py" -ArgsList $argsList
    }

    "validate" {
        $resolvedRunDir = Resolve-RunDir
        $argsList = @(
            "--run-dir", $resolvedRunDir,
            "--min-rows", "$Limit"
        )
        if ($RequireAssets) {
            $argsList += "--require-assets"
        }
        if ($CarouselId) {
            $argsList += @("--carousel-id", $CarouselId)
        }
        Invoke-MikaPython -ScriptPath "10_automation\validate_weekly_run.py" -ArgsList $argsList
    }

    "smoke-test" {
        Invoke-MikaPython -ScriptPath "10_automation\smoke_test_weekly_pipeline.py"
    }
}
