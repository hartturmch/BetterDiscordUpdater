@echo off
setlocal

set "INSTALL_DIR=%LocalAppData%\BetterDiscordUpdater"
set "PACKAGE=%~dp0BetterDiscordUpdater-v1.0.0-win64.zip"

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

%SystemRoot%\System32\tar.exe -xf "%PACKAGE%" -C "%INSTALL_DIR%"
if errorlevel 1 (
    echo Installation failed. Close this window and try again.
    pause
    exit /b 1
)

start "" "%INSTALL_DIR%\updater.exe"
exit /b 0
