@echo off
REM VS Code Projekt Creator - Einfacher Starter
REM Doppelklick oder aus CMD ausfuehren

setlocal EnableDelayedExpansion

echo.
echo ========================================
echo   VS Code Projekt Creator
echo ========================================
echo.

REM Projektname abfragen wenn nicht uebergeben
set "PROJECT_NAME=%~1"
if "%PROJECT_NAME%"=="" (
    set /p "PROJECT_NAME=Projektname: "
)

REM PowerShell Script ausfuehren
powershell -ExecutionPolicy Bypass -File "%~dp0new-project-standalone.ps1" -ProjectName "%PROJECT_NAME%"

pause
