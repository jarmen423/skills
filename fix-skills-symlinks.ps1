$skillsDir = "C:\Users\jfrie\.claude\skills"
$agentsDir = "C:\Users\jfrie\.agents\skills"

$converted = 0
$skipped = 0
$failed = 0

Get-ChildItem -Path $skillsDir | Where-Object { $_.LinkType -eq "SymbolicLink" } | ForEach-Object {
    $name = $_.Name
    $target = Join-Path $agentsDir $name

    if (Test-Path $target) {
        Remove-Item $_.FullName -Force
        try {
            New-Item -ItemType Junction -Path (Join-Path $skillsDir $name) -Target $target -ErrorAction Stop | Out-Null
            Write-Host "OK  $name"
            $converted++
        } catch {
            Write-Host "FAIL $name - $_"
            $failed++
        }
    } else {
        Write-Host "SKIP $name (target missing)"
        $skipped++
    }
}

Write-Host ""
Write-Host "Done: $converted converted, $skipped skipped, $failed failed"
