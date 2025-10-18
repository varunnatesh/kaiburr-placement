param(
    [string]$Base = "",
    [ValidateSet("pretty","compact","markdown")]
    [string]$Mode = "pretty",
    [int]$Limit = 0,
    [string]$SaveDir = ""
)

# Helper: pretty print objects as JSON
function To-JsonPretty($obj) {
    try {
        $obj | ConvertTo-Json -Depth 8
    } catch {
        $_ | Out-String
    }
}

function Summarize-Tasks($tasks) {
    $list = @()
    foreach ($t in $tasks) {
        $list += [PSCustomObject]@{
            id    = $t.id
            name  = $t.name
            owner = $t.owner
        }
    }
    if ($Limit -gt 0) { $list = $list | Select-Object -First $Limit }
    return ($list | Format-Table -AutoSize | Out-String)
}

function Summarize-Task($t) {
    $obj = [PSCustomObject]@{
        id      = $t.id
        name    = $t.name
        owner   = $t.owner
        command = if ($t.command.Length -gt 60) { $t.command.Substring(0,60) + '...' } else { $t.command }
    }
    return ($obj | Format-List | Out-String)
}

function Save-Output($name, $data) {
    if ([string]::IsNullOrWhiteSpace($SaveDir)) { return }
    try {
        New-Item -ItemType Directory -Path $SaveDir -Force | Out-Null
        $path = Join-Path $SaveDir ($name + '.json')
        $data | ConvertTo-Json -Depth 8 | Out-File -FilePath $path -Encoding UTF8
    } catch {}
}

function Take-FirstN($data, $n) {
    if ($null -eq $data) { return $data }
    $arr = @($data)
    if ($n -le 0 -or $arr.Count -le $n) { return $arr }
    return $arr | Select-Object -First $n
}

function Write-MarkdownReport($steps, $baseUsed) {
    $md = @()
    $md += "# Task Manager API Run Report"
    $md += ""
    $md += ("- User: Varun K N")
    $md += ("- Time: {0}" -f (Get-Date))
    $md += ("- Base: {0}" -f $baseUsed)
    $md += ""
    $md += "| Step | Action | Status | Key Info |"
    $md += "|------|--------|--------|----------|"
    foreach ($s in $steps) {
        $status = if ($s.Success) { 'OK' } else { 'FAIL' }
        $keySanitized = ($s.Key -replace "\r?\n", ' ')
        $md += ("| {0} | {1} | {2} | {3} |" -f $s.Step, $s.Action, $status, $keySanitized)
    }
    $outPath = if ($SaveDir) { Join-Path $SaveDir 'API_RUN_REPORT.md' } else { Join-Path (Split-Path -Parent $PSCommandPath) 'API_RUN_REPORT.md' }
    $md -join "`r`n" | Out-File -FilePath $outPath -Encoding UTF8
    Write-Host ("Markdown report saved to: {0}" -f $outPath) -ForegroundColor Yellow
}

# Resolve base URL
if ([string]::IsNullOrWhiteSpace($Base)) {
    $Base = "http://localhost:30080/api/tasks"
}

Write-Host "================ API SEQUENCE START ================" -ForegroundColor Cyan
Write-Host ("User: Varun K N  |  Time: {0}" -f (Get-Date)) -ForegroundColor DarkGray
Write-Host ("Base: {0}" -f $Base) -ForegroundColor DarkGray
Write-Host ("Mode: {0}  Limit: {1}" -f $Mode,$Limit) -ForegroundColor DarkGray
Write-Host "=====================================================" -ForegroundColor Cyan

# Probe base URL; if failed, try kubectl proxy fallback
$reachable = $false
try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri $Base -Method Get -TimeoutSec 5
    if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 500) { $reachable = $true }
} catch {}

if (-not $reachable) {
    $proxyBase = "http://127.0.0.1:8001/api/v1/namespaces/default/services/http:task-manager:8080/proxy/api/tasks"
    Write-Host "Primary base not reachable. Trying kubectl proxy route..." -ForegroundColor Yellow
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -Uri $proxyBase -Method Get -TimeoutSec 5
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 500) {
            $Base = $proxyBase
            $reachable = $true
            Write-Host ("Switched to Base: {0}" -f $Base) -ForegroundColor Yellow
        }
    } catch {}
}

if (-not $reachable) {
    Write-Error "Backend API is not reachable on $Base or kubectl proxy route. Ensure the service is running and try again."
    exit 1
}

# Test data
$id = "101"
$name = "Demo Task 101"
$owner = "Varun K N"
$command = "echo Hello from 101"

$steps = @()

# 1) GET ALL
Write-Host "\n[1/8] GET ALL TASKS" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=1; Action='GET ALL'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri $Base -Method Get
    Save-Output '01_get_all' $data
    $s.Success = $true
    $s.Key = "count=" + ($data | Measure-Object | Select-Object -ExpandProperty Count)
    if ($Mode -eq 'pretty') {
        $out = if ($Limit -gt 0) { Take-FirstN $data $Limit } else { $data }
        To-JsonPretty $out
    } elseif ($Mode -eq 'compact' -or $Mode -eq 'markdown') {
        ($data | ForEach-Object { $_ }) | ForEach-Object { } > $null # no-op to realize
        Write-Host (Summarize-Tasks $data)
    }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 2) CREATE/UPDATE (PUT) id=101
Write-Host "\n[2/8] CREATE OR UPDATE TASK (PUT) id=$id" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=2; Action='PUT create/update'; Success=$false; Key='' }
$body = @{ id=$id; name=$name; owner=$owner; command=$command } | ConvertTo-Json
try {
    $data = Invoke-RestMethod -Uri $Base -Method Put -ContentType 'application/json' -Body $body
    Save-Output '02_put_create_update' $data
    $s.Success = $true
    $s.Key = ("id={0}, name={1}" -f $data.id, $data.name)
    if ($Mode -eq 'pretty') { To-JsonPretty $data } else { Write-Host (Summarize-Task $data) }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 3) GET BY ID
Write-Host "\n[3/8] GET TASK BY ID id=$id" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=3; Action='GET by id'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri ("{0}?id={1}" -f $Base,$id) -Method Get
    Save-Output '03_get_by_id' $data
    $s.Success = $true
    $s.Key = ("id={0}, name={1}" -f $data.id, $data.name)
    if ($Mode -eq 'pretty') { To-JsonPretty $data } else { Write-Host (Summarize-Task $data) }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 4) SEARCH BY NAME (substring of name)
Write-Host "\n[4/8] SEARCH TASKS BY NAME contains 'Demo'" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=4; Action='SEARCH by name'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri ("{0}/search?name=Demo" -f $Base) -Method Get
    Save-Output '04_search_by_name' $data
    $s.Success = $true
    $s.Key = "count=" + ($data | Measure-Object | Select-Object -ExpandProperty Count)
    if ($Mode -eq 'pretty') {
        $out = if ($Limit -gt 0) { Take-FirstN $data $Limit } else { $data }
        To-JsonPretty $out
    } else { Write-Host (Summarize-Tasks $data) }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 5) SEARCH BY OWNER
Write-Host "\n[5/8] SEARCH TASKS BY OWNER contains 'Varun'" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=5; Action='SEARCH by owner'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri ("{0}/search?owner=Varun" -f $Base) -Method Get
    Save-Output '05_search_by_owner' $data
    $s.Success = $true
    $s.Key = "count=" + ($data | Measure-Object | Select-Object -ExpandProperty Count)
    if ($Mode -eq 'pretty') {
        $out = if ($Limit -gt 0) { Take-FirstN $data $Limit } else { $data }
        To-JsonPretty $out
    } else { Write-Host (Summarize-Tasks $data) }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 6) EXECUTE TASK
Write-Host "\n[6/8] EXECUTE TASK id=$id" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=6; Action='PUT execute'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri ("{0}/{1}/execute" -f $Base,$id) -Method Put
    Save-Output '06_execute' $data
    $s.Success = $true
    $s.Key = ("output='{0}'" -f ($data.output -replace "\r?\n"," "))
    if ($Mode -eq 'pretty') { To-JsonPretty $data } else { Write-Host ($data | Format-List | Out-String) }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 7) DELETE TASK
Write-Host "\n[7/8] DELETE TASK id=$id" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=7; Action='DELETE'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri ("{0}/{1}" -f $Base,$id) -Method Delete
    Save-Output '07_delete' $data
    $s.Success = $true
    $s.Key = "deleted id=101"
    if ($Mode -eq 'pretty') { To-JsonPretty $data } else { Write-Host ($data | ConvertTo-Json -Depth 4) }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

# 8) GET ALL (final)
Write-Host "\n[8/8] GET ALL TASKS (final)" -ForegroundColor Green
$s = [PSCustomObject]@{ Step=8; Action='GET ALL (final)'; Success=$false; Key='' }
try {
    $data = Invoke-RestMethod -Uri $Base -Method Get
    Save-Output '08_get_all_final' $data
    $s.Success = $true
    $s.Key = "count=" + ($data | Measure-Object | Select-Object -ExpandProperty Count)
    if ($Mode -eq 'pretty') {
        $out = if ($Limit -gt 0) { Take-FirstN $data $Limit } else { $data }
        To-JsonPretty $out
    } elseif ($Mode -eq 'compact' -or $Mode -eq 'markdown') {
        Write-Host (Summarize-Tasks $data)
    }
} catch { Write-Host $_.Exception.Message -ForegroundColor Red }
$steps += $s

if ($Mode -eq 'markdown') { Write-MarkdownReport -steps $steps -baseUsed $Base }

Write-Host "\n================  API SEQUENCE END  =================" -ForegroundColor Cyan
