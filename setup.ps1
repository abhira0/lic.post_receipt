# Post LIC Receipt Setup Script
Write-Host "Setting up Post LIC Receipt shortcut..." -ForegroundColor Cyan

# Get the current directory
$currentDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Get the user's desktop path
$desktopPath = [Environment]::GetFolderPath("Desktop")

# Define paths
$targetPath = Join-Path -Path $currentDir -ChildPath "postit.cmd"
$iconPath = Join-Path -Path $currentDir -ChildPath "mail.ico"
$shortcutPath = Join-Path -Path $desktopPath -ChildPath "Post LIC Receipt.lnk"

# Check if the target file exists
if (-not (Test-Path -Path $targetPath)) {
    Write-Host "Error: $targetPath does not exist!" -ForegroundColor Red
    Write-Host "Make sure postit.cmd is in the same directory as this setup script." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if the icon file exists
if (-not (Test-Path -Path $iconPath)) {
    Write-Host "Warning: Icon file (mail.ico) not found. The shortcut will use the default icon." -ForegroundColor Yellow
    $iconPath = $targetPath
}

# Create the shortcut
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $targetPath
    $Shortcut.WorkingDirectory = $currentDir
    $Shortcut.IconLocation = $iconPath
    $Shortcut.Save()
    
    Write-Host "Successfully created 'Post LIC Receipt' shortcut on your desktop." -ForegroundColor Green
} catch {
    Write-Host "Error creating shortcut: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "`nSetup complete!" -ForegroundColor Cyan
Read-Host "Press Enter to exit"