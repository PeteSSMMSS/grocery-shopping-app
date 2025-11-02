# VS Code Projekt Creator - Standalone Version
# Einfach per Doppelklick oder aus PowerShell ausführen

param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectName
)

# Falls kein Name übergeben, frage danach
if (-not $ProjectName) {
    $ProjectName = Read-Host "Projektname"
}

$ProjectPath = "$HOME\projects\$ProjectName"
$TemplatePath = "$HOME\Desktop\Einkaufen"

Write-Host ""
Write-Host "🚀 Erstelle Projekt: $ProjectName" -ForegroundColor Green
Write-Host "📁 Pfad: $ProjectPath" -ForegroundColor Cyan
Write-Host ""

# Prüfe ob Template existiert
if (-not (Test-Path "$TemplatePath\.github\copilot-instructions.md")) {
    Write-Host "❌ Fehler: Template nicht gefunden!" -ForegroundColor Red
    Write-Host "   Erwartet: $TemplatePath\.github\copilot-instructions.md" -ForegroundColor Yellow
    Read-Host "Enter zum Beenden"
    exit 1
}

# Erstelle Verzeichnisse
Write-Host "📁 Erstelle Verzeichnisse..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "$ProjectPath\.github" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectPath\.devtools" | Out-Null
New-Item -ItemType Directory -Force -Path "$ProjectPath\.vscode" | Out-Null
Write-Host "   ✓ Verzeichnisse erstellt" -ForegroundColor Green

# Kopiere Copilot Instructions
Write-Host "📋 Kopiere Copilot Instructions..." -ForegroundColor Yellow
Copy-Item "$TemplatePath\.github\copilot-instructions.md" "$ProjectPath\.github\" -Force
Write-Host "   ✓ copilot-instructions.md" -ForegroundColor Green

# Kopiere Dev-Tools
Write-Host "🔧 Kopiere Dev-Tools..." -ForegroundColor Yellow
$devtools = @(
    "QDRANT_MCP_SETUP.md",
    "QDRANT_SHORTCUTS.md",
    "QDRANT_SAVE_BEST_PRACTICES.md",
    "qdrant_helper.py",
    "MCP_OPTIMIZATIONS.md",
    "COPILOT_INSTRUCTIONS_TEMPLATE.md"
)

$copied = 0
foreach ($file in $devtools) {
    if (Test-Path "$TemplatePath\.devtools\$file") {
        Copy-Item "$TemplatePath\.devtools\$file" "$ProjectPath\.devtools\" -Force
        $copied++
    }
}
Write-Host "   ✓ $copied Dev-Tool Dateien kopiert" -ForegroundColor Green

# Erstelle README
@"
# Dev-Tools für $ProjectName

Erstellt am: $(Get-Date -Format "dd.MM.yyyy")

## 📚 Dokumentation
- **QDRANT_MCP_SETUP.md** - Qdrant Setup
- **QDRANT_SHORTCUTS.md** - `/qd` Befehle
- **QDRANT_SAVE_BEST_PRACTICES.md** - Speicher-Guidelines
- **MCP_OPTIMIZATIONS.md** - VS Code MCP Optimierungen

## 🔧 Tools
- **qdrant_helper.py** - Helper-Script

## 🎯 Copilot Instructions
Liegen in `.github/copilot-instructions.md`

## 🚀 Schnellstart
``````
/qd ssh
/qd deploy
``````
"@ | Out-File -FilePath "$ProjectPath\.devtools\README.md" -Encoding UTF8
Write-Host "   ✓ README.md" -ForegroundColor Green

# Erstelle VS Code Settings
@"
{
    "github.copilot.chat.localeOverride": "de",
    "chat.mcp.autostart": "newAndOutdated"
}
"@ | Out-File -FilePath "$ProjectPath\.vscode\settings.json" -Encoding UTF8
Write-Host "   ✓ settings.json" -ForegroundColor Green

# Erstelle .gitignore
@"
# Dev-Tools lokale Dateien
.devtools/notes/
.devtools/*.local.*
*.tmp
"@ | Out-File -FilePath "$ProjectPath\.devtools\.gitignore" -Encoding UTF8

Write-Host ""
Write-Host "✅ Projekt erfolgreich erstellt!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Erstellt:" -ForegroundColor Cyan
Write-Host "   • .github/copilot-instructions.md"
Write-Host "   • .devtools/ ($copied Dateien)"
Write-Host "   • .vscode/settings.json"
Write-Host ""
Write-Host "📁 Projekt-Pfad:" -ForegroundColor Yellow
Write-Host "   $ProjectPath" -ForegroundColor White
Write-Host ""

# Frage ob VS Code öffnen
$open = Read-Host "VS Code jetzt öffnen? (j/n)"
if ($open -eq "j" -or $open -eq "J" -or $open -eq "y" -or $open -eq "Y") {
    Write-Host "🚀 Öffne VS Code..." -ForegroundColor Green
    code "$ProjectPath"
} else {
    Write-Host ""
    Write-Host "Öffne später mit:" -ForegroundColor Cyan
    Write-Host "   code `"$ProjectPath`"" -ForegroundColor White
}

Write-Host ""
Read-Host "Enter zum Beenden"
