# push-amr.ps1 v2
# Usage: .\push-amr.ps1 "description du changement"

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
)

$ErrorActionPreference = "Continue"

function Test-LastCommand {
    param([string]$Step)
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[X] Echec etape: $Step" -ForegroundColor Red
        Write-Host "Code retour: $LASTEXITCODE" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "=== PUSH AMR ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".git")) {
    Write-Host "[X] Pas dans un repo Git. Place ce script dans C:\dev\amr-site\" -ForegroundColor Red
    exit 1
}

$null = gh --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] GitHub CLI non installe. https://cli.github.com" -ForegroundColor Red
    exit 1
}

$null = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] GitHub CLI non authentifie. Tape: gh auth login" -ForegroundColor Red
    exit 1
}

Write-Host "[1/6] Sync main..." -ForegroundColor Yellow
git checkout main --quiet 2>&1 | Out-String | Out-Null
Test-LastCommand "git checkout main"
git pull origin main --quiet 2>&1 | Out-String | Out-Null
Test-LastCommand "git pull"

$changes = git status --porcelain 2>&1
if (-not $changes) {
    Write-Host "[!] Aucun changement detecte. Rien a pousser." -ForegroundColor Yellow
    exit 0
}

Write-Host "[2/6] Changements detectes:" -ForegroundColor Yellow
git status --short

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$branchName = "claude/auto-$timestamp"
Write-Host ""
Write-Host "[3/6] Creation branche: $branchName" -ForegroundColor Yellow
git checkout -b $branchName --quiet 2>&1 | Out-String | Out-Null
Test-LastCommand "git checkout -b"

Write-Host "[4/6] Commit et push..." -ForegroundColor Yellow
git add -A 2>&1 | Out-String | Out-Null
Test-LastCommand "git add"

git commit -m "$Message" --quiet 2>&1 | Out-String | Out-Null
Test-LastCommand "git commit"

git push -u origin $branchName --quiet 2>&1 | Out-String | Out-Null
Test-LastCommand "git push"

Write-Host "[5/6] Creation Pull Request..." -ForegroundColor Yellow
$prBody = @"
Auto-push depuis session Claude.

Branche: $branchName
Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

Validator passera automatiquement a 8h matin.
"@

$prUrl = gh pr create --title "$Message" --body "$prBody" --base main --head $branchName 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[X] Erreur creation PR:" -ForegroundColor Red
    Write-Host $prUrl -ForegroundColor Red
    exit 1
}
Write-Host "[OK] PR creee: $prUrl" -ForegroundColor Green

Write-Host ""
Write-Host "[6/6] Tentative auto-merge..." -ForegroundColor Yellow
$prNumber = ($prUrl -split '/')[-1]
$autoMergeOutput = gh pr merge $prNumber --auto --squash --delete-branch 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Auto-merge active. Sera merge des que checks OK (Validator 8h)." -ForegroundColor Green
} else {
    Write-Host "[!] Auto-merge non active. Merge manuel via web." -ForegroundColor Yellow
}

git checkout main --quiet 2>&1 | Out-String | Out-Null

Write-Host ""
Write-Host "=== TERMINE ===" -ForegroundColor Cyan
Write-Host "URL: $prUrl" -ForegroundColor Cyan
Write-Host ""

$open = Read-Host "Ouvrir la PR dans le navigateur ? (O/N)"
if ($open -eq "O" -or $open -eq "o") {
    Start-Process $prUrl
}
