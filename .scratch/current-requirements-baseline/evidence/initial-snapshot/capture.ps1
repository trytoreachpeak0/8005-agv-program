param(
    [string]$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')).Path
)

$ErrorActionPreference = 'Stop'
$captureStartedLocal = Get-Date
$captureStartedUtc = $captureStartedLocal.ToUniversalTime()
$outputDirectory = $PSScriptRoot
$effortRelativePrefix = '.scratch/current-requirements-baseline/'

function Normalize-RepositoryPath {
    param([string]$Path)
    $normalized = $Path -replace '\\', '/'
    if ($normalized.StartsWith('./', [StringComparison]::Ordinal)) {
        return $normalized.Substring(2)
    }
    return $normalized
}

function New-PathSet {
    param([string[]]$Paths)
    $set = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($path in $Paths) {
        if (-not [string]::IsNullOrWhiteSpace($path)) {
            [void]$set.Add((Normalize-RepositoryPath $path))
        }
    }
    return ,$set
}

Push-Location -LiteralPath $RepositoryRoot
try {
    $branch = (git branch --show-current).Trim()
    $head = (git rev-parse HEAD).Trim()
    $upstream = (git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>$null)
    if ($LASTEXITCODE -ne 0) {
        $upstream = '(none)'
    }
    else {
        $upstream = $upstream.Trim()
    }

    $tracked = New-PathSet @(git ls-files)
    $staged = New-PathSet @(git diff --cached --name-only 2>$null)
    $modified = New-PathSet @(git diff --name-only 2>$null)
    $worktreeStatusPath = Join-Path $outputDirectory 'worktree-status.txt'
    $worktreeStatus = @(git status --porcelain=v1 --branch --untracked-files=all)
    [IO.File]::WriteAllLines($worktreeStatusPath, $worktreeStatus, [Text.UTF8Encoding]::new($false))

    $excludedGlobs = @(
        '!.git/**',
        '!**/bin/**',
        '!**/obj/**',
        '!**/node_modules/**',
        '!**/packages/**',
        '!**/dist/**',
        '!**/.dist/**',
        '!**/build/**',
        '!**/coverage/**',
        '!**/TestResults/**',
        '!**/.vs/**',
        '!**/.idea/**',
        '!**/.vscode/**',
        '!**/.cache/**',
        '!**/.cache',
        '!**/.pytest_cache/**',
        '!**/.pytest_cache',
        '!rcs/riot-sdk/python/.pytest_cache/**',
        '!rcs/riot-sdk/python/.pytest_cache',
        '!**/artifacts/**',
        '!**/artifact/**'
    )
    $rgArguments = @('--files', '--hidden', '--no-ignore')
    foreach ($glob in $excludedGlobs) {
        $rgArguments += @('-g', $glob)
    }

    $discoveryErrorsPath = Join-Path $outputDirectory 'discovery-errors.txt'
    $discoveryErrorsTemporaryPath = Join-Path $env:TEMP ("agv-snapshot-rg-{0}.txt" -f [guid]::NewGuid().ToString('N'))
    $allPaths = @(& rg @rgArguments 2> $discoveryErrorsTemporaryPath)
    $rgExitCode = $LASTEXITCODE
    $discoveryErrors = if (Test-Path -LiteralPath $discoveryErrorsTemporaryPath) {
        @(Get-Content -LiteralPath $discoveryErrorsTemporaryPath)
    }
    else {
        @()
    }
    if (Test-Path -LiteralPath $discoveryErrorsTemporaryPath) {
        Remove-Item -LiteralPath $discoveryErrorsTemporaryPath
    }
    if ($discoveryErrors.Count -eq 0) {
        [IO.File]::WriteAllText($discoveryErrorsPath, '', [Text.UTF8Encoding]::new($false))
    }
    else {
        [IO.File]::WriteAllLines($discoveryErrorsPath, $discoveryErrors, [Text.UTF8Encoding]::new($false))
    }
    if ($rgExitCode -notin @(0, 1)) {
        throw "rg candidate discovery failed with exit code $rgExitCode. See discovery-errors.txt."
    }

    $candidateExtensions = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    @(
        '.md', '.markdown', '.adoc', '.rst', '.txt', '.rtf',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.csv', '.tsv', '.html', '.htm', '.xml', '.json', '.yaml', '.yml',
        '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.svg', '.drawio'
    ) | ForEach-Object { [void]$candidateExtensions.Add($_) }

    $candidatePaths = @(
        $allPaths |
            ForEach-Object { Normalize-RepositoryPath $_ } |
            Where-Object {
                -not $_.StartsWith($effortRelativePrefix, [StringComparison]::OrdinalIgnoreCase) -and
                $candidateExtensions.Contains([IO.Path]::GetExtension($_))
            } |
            Sort-Object -Unique
    )

    $nonTrackedCandidatePaths = @($candidatePaths | Where-Object { -not $tracked.Contains($_) })
    $ignoredPaths = if ($nonTrackedCandidatePaths.Count -gt 0) {
        @($nonTrackedCandidatePaths | git check-ignore --stdin)
    }
    else {
        @()
    }
    if ($LASTEXITCODE -notin @(0, 1)) {
        throw "git check-ignore failed with exit code $LASTEXITCODE."
    }
    $ignored = New-PathSet $ignoredPaths

    $rows = foreach ($relativePath in $candidatePaths) {
        $absolutePath = Join-Path $RepositoryRoot ($relativePath -replace '/', [IO.Path]::DirectorySeparatorChar)
        $item = Get-Item -LiteralPath $absolutePath
        $gitStatus = if ($tracked.Contains($relativePath)) {
            $parts = [System.Collections.Generic.List[string]]::new()
            if ($staged.Contains($relativePath)) { $parts.Add('staged') }
            if ($modified.Contains($relativePath)) { $parts.Add('modified') }
            if ($parts.Count -eq 0) { 'tracked-clean' } else { 'tracked-' + ($parts -join '+') }
        }
        elseif ($ignored.Contains($relativePath)) {
            'ignored-untracked'
        }
        else {
            'untracked'
        }

        [PSCustomObject]@{
            path = $relativePath
            git_status = $gitStatus
            sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $absolutePath).Hash.ToLowerInvariant()
            bytes = $item.Length
            last_write_utc = $item.LastWriteTimeUtc.ToString('o')
        }
    }

    $manifestPath = Join-Path $outputDirectory 'candidate-documents.tsv'
    $manifestLines = @($rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation)
    [IO.File]::WriteAllLines($manifestPath, $manifestLines, [Text.UTF8Encoding]::new($false))

    $captureCompletedLocal = Get-Date
    $captureCompletedUtc = $captureCompletedLocal.ToUniversalTime()
    $statusCounts = @($rows | Group-Object git_status | Sort-Object Name)
    $statusSummary = @($statusCounts | ForEach-Object { "- $($_.Name): $($_.Count)" })
    if ($statusSummary.Count -eq 0) {
        $statusSummary = @('- (none): 0')
    }
    $discoveryErrorSummary = if ($discoveryErrors.Count -eq 0) {
        'None.'
    }
    else {
        "$($discoveryErrors.Count) line(s); see `discovery-errors.txt`."
    }

    $metadata = @(
        '# Initial requirement-evidence snapshot',
        '',
        'This is an evidence capture, not an authority or approval classification. It does not modify source requirement materials.',
        '',
        '## Capture identity',
        '',
        "- Started (local): $($captureStartedLocal.ToString('o'))",
        "- Started (UTC): $($captureStartedUtc.ToString('o'))",
        "- Completed (local): $($captureCompletedLocal.ToString('o'))",
        "- Completed (UTC): $($captureCompletedUtc.ToString('o'))",
        "- Repository root: $RepositoryRoot",
        "- Branch: $branch",
        "- HEAD: $head",
        "- Upstream: $upstream",
        "- Candidate files: $($rows.Count)",
        '- Content hash: SHA-256 of the actual working-directory bytes',
        "- Discovery errors: $discoveryErrorSummary",
        '',
        '## Candidate policy',
        '',
        'The manifest takes a deliberately broad document-shaped candidate set from the actual working directory, including tracked, untracked, and ignored files. It includes Markdown/text, structured data, PDF/Office, image, HTML/XML, and diagram formats. Inclusion does not imply that a file is a requirement or authoritative.',
        '',
        'Dependency, build-output, test-output, IDE, and cache directory names are excluded by the capture script. This map and its evidence directory (`.scratch/current-requirements-baseline/`) are also excluded from the candidate set because they are newly-created governance records, not recovered source requirements; they remain visible in the raw worktree status. If later inventory discovers requirement evidence outside this candidate policy, it must be recorded in a new snapshot rather than silently added to this one.',
        '',
        '## Git status counts',
        ''
    ) + $statusSummary + @(
        '',
        '## Files',
        '',
        '- `candidate-documents.tsv`: candidate path, Git state, SHA-256, byte size, and last-write UTC.',
        '- `worktree-status.txt`: raw `git status --porcelain=v1 --branch --untracked-files=all` output captured during this run.',
        '- `discovery-errors.txt`: stderr from file discovery; empty means no discovery errors.',
        '- `capture.ps1`: the exact repeatable capture method. Re-running it overwrites this evidence directory and therefore creates a new observation, not the original observation.',
        '',
        '## Verification boundary',
        '',
        'The manifest fixes the observed bytes and Git state at capture time. Later file changes must not overwrite the meaning of this capture; compare current hashes to the manifest or create a separately timestamped snapshot.'
    )
    [IO.File]::WriteAllLines((Join-Path $outputDirectory 'snapshot.md'), $metadata, [Text.UTF8Encoding]::new($false))
}
finally {
    Pop-Location
}
