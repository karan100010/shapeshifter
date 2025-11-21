# Install GitHub CLI and create issues

# Install GitHub CLI
Write-Host "Installing GitHub CLI..." -ForegroundColor Green
winget install --id GitHub.cli

Write-Host "`nPlease restart PowerShell and run create_issues.ps1 to create the issues." -ForegroundColor Yellow
Write-Host "After restarting, you'll need to authenticate with: gh auth login" -ForegroundColor Yellow
