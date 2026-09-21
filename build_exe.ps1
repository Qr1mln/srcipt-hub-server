# Build zjm_server into a single-file exe via PyInstaller.
# Usage: run in repo root ->  .\build_exe.ps1
#
# NOTE: stop any running zjm_server.exe before rebuilding, otherwise PyInstaller
# fails to overwrite dist\zjm_server.exe (OSError / safe-delete failure).
# This script stops it automatically.

$ErrorActionPreference = 'Stop'

$pyinstaller = "C:\Users\111\.conda\envs\zjm-server\Scripts\pyinstaller.exe"
$spec        = "zjm_server.spec"

if (-not (Test-Path $pyinstaller)) {
    Write-Error "pyinstaller not found: $pyinstaller. Please install PyInstaller in the zjm-server conda env."
    exit 1
}
if (-not (Test-Path $spec)) {
    Write-Error "spec not found: $spec"
    exit 1
}

# Stop any process holding dist\zjm_server.exe to avoid overwrite failure.
$proc = Get-Process -Name zjm_server -ErrorAction SilentlyContinue
if ($proc) {
    Write-Host "Stopping running zjm_server.exe ..."
    Stop-Process -Name zjm_server -Force
    Start-Sleep -Seconds 1
}

Write-Host "Building (pyinstaller --noconfirm --clean $spec) ..."
& $pyinstaller --noconfirm --clean $spec

if (Test-Path "dist\zjm_server.exe") {
    Write-Host "Done: dist\zjm_server.exe"
} else {
    Write-Error "Build seems incomplete: dist\zjm_server.exe was not generated."
    exit 1
}
