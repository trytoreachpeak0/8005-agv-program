[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$scriptPath = $MyInvocation.MyCommand.Path
$batchDir = [System.IO.Path]::GetDirectoryName($scriptPath)
$evidenceDir = [System.IO.Directory]::GetParent($batchDir).FullName
$effortDir = [System.IO.Directory]::GetParent($evidenceDir).FullName
$issuesDir = Join-Path $effortDir 'issues'
$mapPath = Join-Path $effortDir 'map.md'
$manifestPath = Join-Path $batchDir 'v1-final-approval-batches.tsv'
$approvalEvidence = 'evidence/v1-final-approval-batches/consolidated-approval-2026-08-24.md'
$ledgerHash = '9ba7f6132a9c4599fc06f1646370de54254a94de9a1ab5e3ca7b0451162fa646'
$manifestHash = '3551d711c4a8553285d77ff8ba0b182dd664f829533b1b369db68a1159f20843'
$approvedAt = '2026-08-24T15:16:06Z'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Get-Sha256([string]$Path) {
    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $hash = [System.Security.Cryptography.SHA256]::Create().ComputeHash($stream)
        return ([System.BitConverter]::ToString($hash)).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $stream.Dispose()
    }
}

function Read-Utf8([string]$Path) {
    return [System.IO.File]::ReadAllText($Path).Replace("`r`n", "`n")
}

function Write-Utf8([string]$Path, [string]$Text) {
    [System.IO.File]::WriteAllText($Path, $Text.Replace("`r`n", "`n"), $utf8NoBom)
}

if ((Get-Sha256 $manifestPath) -ne $manifestHash) {
    throw 'Approval manifest identity drift'
}

$rows = @(Import-Csv -LiteralPath $manifestPath -Delimiter "`t" | Where-Object {
    [int]$_.issue_number -ge 93 -and [int]$_.issue_number -le 183
} | Sort-Object { [int]$_.issue_number })

if ($rows.Count -ne 91) {
    throw "Expected 91 approval tickets, found $($rows.Count)"
}

$mapEntries = [System.Collections.Generic.List[string]]::new()
$approvedReqs = [System.Collections.Generic.List[string]]::new()

foreach ($row in $rows) {
    $issuePath = Join-Path $effortDir $row.issue_file
    if (-not (Test-Path -LiteralPath $issuePath)) {
        throw "Missing issue: $($row.issue_file)"
    }

    $text = Read-Utf8 $issuePath
    $statusMatch = [regex]::Match($text, '(?m)^Status:\s*(open|claimed|resolved)\s*$')
    if (-not $statusMatch.Success) {
        throw "Missing tracker status: $($row.issue_file)"
    }
    if ($statusMatch.Groups[1].Value -eq 'resolved') {
        if ($text -notmatch [regex]::Escape($approvalEvidence)) {
            throw "Resolved ticket lacks consolidated evidence: $($row.issue_file)"
        }
        continue
    }
    if ($statusMatch.Groups[1].Value -ne 'open') {
        throw "Ticket is not open: $($row.issue_file)"
    }

    $payload = [regex]::Match($text, '(?m)^Approval payload SHA-256:\s*([0-9a-f]{64})\s*$').Groups[1].Value
    $ticketLedger = [regex]::Match($text, '(?m)^Candidate ledger SHA-256:\s*([0-9a-f]{64})\s*$').Groups[1].Value
    if ($payload -ne $row.approval_payload_sha256) {
        throw "Payload mismatch: $($row.issue_file)"
    }
    if ($ticketLedger -ne $ledgerHash) {
        throw "Candidate ledger mismatch: $($row.issue_file)"
    }
    if ([regex]::IsMatch($text, '(?m)^## Answer\s*$')) {
        throw "Current Answer already exists: $($row.issue_file)"
    }

    $reqIds = @($row.candidate_ids -split ',')
    if ($reqIds.Count -ne [int]$row.candidate_count) {
        throw "Candidate count mismatch: $($row.issue_file)"
    }
    foreach ($reqId in $reqIds) {
        if ($text -notmatch "(?m)^### $([regex]::Escape($reqId)) —") {
            throw "Missing candidate $reqId in $($row.issue_file)"
        }
        $checkPattern = "(?m)^- \[ \] `$([regex]::Escape($reqId))`：批准／拒绝／修订（写明精确选择）$"
        $checkedLine = "- [x] ``$reqId``：批准／拒绝／修订（写明精确选择）"
        $text = [regex]::Replace($text, $checkPattern, $checkedLine, 1)
        $approvedReqs.Add($reqId)
    }

    $text = [regex]::Replace($text, '(?m)^Status:\s*open\s*$', 'Status: resolved', 1)
    $itemLines = ($reqIds | ForEach-Object {
        "- ``$_``：批准本票所列精确规范文本、适用范围与验证方法进入 ``v1.0.0``。"
    }) -join "`n"
    $special = if ([int]$row.issue_number -eq 127) {
        "`n机械修复说明：``REQ-0149`` 已按候选总账恢复字面量 ``serviceId=enable|disable``；规范文本语义、文本 SHA-256 与 Approval payload 均未改变，修正后的初始票据 SHA-256 为 ``ed2ca2bb5cf19464f11e0fbe8e92d884817eac1bbfa02c2f2b44f953b9d9c2a6``。`n"
    }
    else { '' }
    $answer = @"
## Answer

用户本人作为本地图默认且唯一最终批准人，于 `$approvedAt` 在本次 Codex 任务中审阅三路并行只读核对的汇总结论后明确回复“同意”，并授权采用集中审批、单一协调者串行落盘。该回复按票面规则解释为逐项采用本票全部推荐值：

$itemLines
$special
本批准绑定批次 ``$($row.batch_id)``、Approval payload SHA-256 ``$($row.approval_payload_sha256)``、候选总账 SHA-256 ``$ledgerHash``、当前 95 批 manifest SHA-256 ``$manifestHash``，以及本票逐项列出的规范文本 SHA-256。任一绑定字段变化均使本批准失效并要求重新生成、重新批准。

集中批准证据：[$approvalEvidence](../$approvalEvidence)。三路核对确认本批的 REQ 成员、规范文本、范围、验证方法、来源身份、冲突处置和 payload 与当前总账及 manifest 一致；没有未解决业务判断、外部权限、破坏性操作或路线图范围扩张。本批准不把 ``Superseded Answer`` 恢复为当前批准，也不扩大票据明确保留的现场或投运前验证边界。
"@.Trim()

    $insertMatch = [regex]::Match($text, '(?m)^## (?:Superseded Answer|Comments)')
    if ($insertMatch.Success) {
        $text = $text.Insert($insertMatch.Index, $answer + "`n`n")
    }
    else {
        $text = $text.TrimEnd() + "`n`n" + $answer + "`n"
    }
    Write-Utf8 $issuePath $text

    $gist = "用户逐项批准 $($row.first_req)–$($row.last_req) 的当前精确文本、范围与验证方法，绑定 $($row.batch_id)、payload ``$($row.approval_payload_sha256)``、当前候选总账及 manifest。"
    $mapEntries.Add("- [$($row.title)]($($row.issue_file)) — $gist")
}

$uniqueApprovedReqs = @($approvedReqs | Sort-Object -Unique)
if ($approvedReqs.Count -ne 332 -or $uniqueApprovedReqs.Count -ne 332) {
    throw "Expected 332 unique approved REQs, found $($uniqueApprovedReqs.Count)"
}
if ($approvedReqs[0] -ne 'REQ-0017' -or $approvedReqs[$approvedReqs.Count - 1] -ne 'REQ-0348') {
    throw 'Approved REQ range drift'
}

$mapText = Read-Utf8 $mapPath
$marker = "## Not yet specified"
$markerIndex = $mapText.IndexOf($marker, [System.StringComparison]::Ordinal)
if ($markerIndex -lt 0) {
    throw 'Map is missing Not yet specified section'
}
$newEntries = @($mapEntries | Where-Object { $mapText -notmatch [regex]::Escape($_.Split(']')[0] + ']') })
if ($newEntries.Count -gt 0) {
    $block = ($newEntries -join "`n") + "`n`n"
    $mapText = $mapText.Insert($markerIndex, $block)
    Write-Utf8 $mapPath $mapText
}

[pscustomobject]@{
    resolved_tickets = $rows.Count
    approved_requirements = $approvedReqs.Count
    candidate_ledger_sha256 = $ledgerHash
    approval_manifest_sha256 = $manifestHash
    map_entries_added = $newEntries.Count
} | ConvertTo-Json
