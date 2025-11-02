# VS Code Projekt-Initialisierung Script (PowerShell)
# Kopiert Copilot Instructions und Dev-Tools in neues Projekt

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath = "."
)

Write-Host "🚀 Initialisiere VS Code Projekt: $ProjectName" -ForegroundColor Green
Write-Host "📁 Pfad: $ProjectPath" -ForegroundColor Cyan
Write-Host ""

# Template-Pfad
$TemplatePath = Split-Path -Parent $PSScriptRoot

# Erstelle Verzeichnisse
New-Item -ItemType Directory -Force -Path "$ProjectPath\.github" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectPath\.vscode" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectPath\.devtools" | Out-Null

# Kopiere Copilot Instructions
Write-Host "📋 Kopiere Copilot Instructions..." -ForegroundColor Yellow
Copy-Item "$TemplatePath\.github\copilot-instructions.md" "$ProjectPath\.github\" -Force
Write-Host "   ✓ .github/copilot-instructions.md" -ForegroundColor Green

# Kopiere Dev-Tools
Write-Host "🔧 Kopiere Dev-Tools..." -ForegroundColor Yellow
$devtools = @(
    "QDRANT_MCP_SETUP.md",
    "QDRANT_SHORTCUTS.md",
    "QDRANT_SAVE_BEST_PRACTICES.md",
    "qdrant_helper.py",
    "MCP_OPTIMIZATIONS.md"
)

foreach ($file in $devtools) {
    Copy-Item "$TemplatePath\.devtools\$file" "$ProjectPath\.devtools\" -Force
}
Write-Host "   ✓ Dev-Tools kopiert" -ForegroundColor Green

# Erstelle README
@"
# Dev-Tools für dieses Projekt

## 📚 Dokumentation

- **QDRANT_MCP_SETUP.md** - Qdrant MCP Server Setup
- **QDRANT_SHORTCUTS.md** - Kurzbefehl-System (``/qd``)
- **QDRANT_SAVE_BEST_PRACTICES.md** - Best Practices für Speichern
- **MCP_OPTIMIZATIONS.md** - MCP Optimierungen

## 🔧 Tools

- **qdrant_helper.py** - Helper-Script für Qdrant

## 🎯 Copilot Instructions

Die Copilot Instructions liegen in ``.github/copilot-instructions.md``.

Diese beinhalten:
- Beast Mode 4.0 Workflow
- Qdrant Langzeitgedächtnis Integration
- MCP Server Tools
- Best Practices

## 🚀 Schnellstart

1. **Qdrant läuft bereits global** (Port 6333)
2. **MCP Server konfiguriert** (``%APPDATA%\Code\User\mcp.json``)
3. **Sofort loslegen:**
   ````
   /qd ssh
   /qd deploy
   ````

## 📝 Wissen speichern

````powershell
python .devtools/qdrant_helper.py
````

Oder im Chat:
````
"Speichere in Qdrant: [deine Infos]"
````
"@ | Out-File -FilePath "$ProjectPath\.devtools\README.md" -Encoding UTF8

Write-Host "   ✓ .devtools/README.md" -ForegroundColor Green

# Erstelle .gitignore
@"
# Lokale Notizen
notes/
*.local.*

# Temporäre Dateien
*.tmp
*.swp
"@ | Out-File -FilePath "$ProjectPath\.devtools\.gitignore" -Encoding UTF8

# Erstelle Projekt-Daten
$date = Get-Date -Format "yyyy-MM-dd"
@"
{
  "project": "$ProjectName",
  "created": "$date",
  "qdrant": {
    "collection": "project_knowledge",
    "url": "http://localhost:6333"
  }
}
"@ | Out-File -FilePath "$ProjectPath\.devtools\project_data.json" -Encoding UTF8

Write-Host "   ✓ project_data.json" -ForegroundColor Green

# Erstelle .vscode/settings.json
if (-not (Test-Path "$ProjectPath\.vscode\settings.json")) {
    @"
{
    "github.copilot.chat.localeOverride": "de",
    "chat.mcp.autostart": "newAndOutdated"
}
"@ | Out-File -FilePath "$ProjectPath\.vscode\settings.json" -Encoding UTF8
    Write-Host "   ✓ .vscode/settings.json" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Projekt initialisiert!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Erstellt:" -ForegroundColor Cyan
Write-Host "   .github/copilot-instructions.md"
Write-Host "   .devtools/ (5 Dateien)"
Write-Host "   .vscode/settings.json"
Write-Host ""
Write-Host "🎯 Nächste Schritte:" -ForegroundColor Yellow
Write-Host "   1. cd $ProjectPath"
Write-Host "   2. code ."
Write-Host "   3. Ctrl+Shift+P → Developer: Reload Window"
Write-Host "   4. /qd test"
Write-Host ""
