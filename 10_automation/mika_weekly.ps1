param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("pipeline", "status", "assets", "metrics", "validate", "smoke-test")]
    [string]$Action,

    [string]$Week = "",
    [string]$PerplexitySource = "",
    [string]$RunDir = "",
    [string]$Database = "04_prompts\item_prompt_database.csv",
    [int]$Limit = 2,

    [string]$ScoreSheet = "",
    [string]$DriveInventory = "",

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
        if (-not $Week) {
            throw "Week is required for pipeline."
        }

        $resolvedRunDir = Resolve-RunDir
        $argsList = @(
            "--week", $Week,
            "--database", $Database,
            "--limit", "$Limit",
            "--output-dir", $resolvedRunDir
        )

        if ($PerplexitySource) {
            $argsList += @("--perplexity-source", $PerplexitySource)
        }
        if ($ScoreSheet) {
            $argsList += @("--score-sheet", $ScoreSheet)
        }
        if ($DriveInventory) {
            $argsList += @("--drive-inventory", $DriveInventory)
        }

        Invoke-MikaPython -ScriptPath "10_automation\run_weekly_pipeline.py" -ArgsList $argsList
    }

    "status" {
        $resolvedRunDir = Resolve-RunDir
        Invoke-MikaPython -ScriptPath "10_automation\check_weekly_status.py" -ArgsList @("--run-dir", $resolvedRunDir)
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
        Invoke-MikaPython -ScriptPath "10_automation\select_grok_assets.py" -ArgsList $argsList
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
        Invoke-MikaPython -ScriptPath "10_automation\validate_weekly_run.py" -ArgsList $argsList
    }

    "smoke-test" {
        Invoke-MikaPython -ScriptPath "10_automation\smoke_test_weekly_pipeline.py"
    }
}
