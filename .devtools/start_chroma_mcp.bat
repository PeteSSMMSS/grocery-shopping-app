@echo off
REM Chroma MCP Launcher für VS Code
REM Nutzt Python 3.11 in Virtual Environment

SET SCRIPT_DIR=%~dp0
SET VENV_DIR=%SCRIPT_DIR%chroma_venv
SET DATA_DIR=D:\Cooperate Design\Chroma

REM Prüfe ob Virtual Environment existiert
IF NOT EXIST "%VENV_DIR%\Scripts\python.exe" (
    echo [CHROMA MCP] Virtual Environment wird erstellt...
    python -m venv "%VENV_DIR%"
    
    echo [CHROMA MCP] Installiere chroma-mcp...
    "%VENV_DIR%\Scripts\pip.exe" install chroma-mcp --no-warn-script-location
)

REM Starte Chroma MCP Server
"%VENV_DIR%\Scripts\python.exe" -m chroma_mcp --client-type persistent --data-dir "%DATA_DIR%"
