# Windows PowerShell Setup für automatische Projekt-Initialisierung

## 🚀 Schnellstart (Empfohlen)

### 1. PowerShell Profil einrichten

```powershell
# Öffne PowerShell Profil
notepad $PROFILE

# Falls Datei nicht existiert:
New-Item -Path $PROFILE -ItemType File -Force
notepad $PROFILE
```

### 2. Funktion hinzufügen

```powershell
# VS Code Projekt Creator
function New-VSCodeProject {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Name,
        
        [Parameter(Mandatory=$false)]
        [string]$Path = "$HOME\projects"
    )
    
    $TemplatePath = "$HOME\Desktop\Einkaufen"
    $ProjectPath = Join-Path $Path $Name
    
    Write-Host "🚀 Erstelle Projekt: $Name" -ForegroundColor Green
    
    # Erstelle Verzeichnisse
    New-Item -ItemType Directory -Force -Path "$ProjectPath\.github" | Out-Null
    New-Item -ItemType Directory -Force -Path "$ProjectPath\.devtools" | Out-Null
    New-Item -ItemType Directory -Force -Path "$ProjectPath\.vscode" | Out-Null
    
    # Kopiere Copilot Instructions
    Copy-Item "$TemplatePath\.github\copilot-instructions.md" "$ProjectPath\.github\" -Force
    
    # Kopiere Dev-Tools
    $files = @(
        "QDRANT_MCP_SETUP.md",
        "QDRANT_SHORTCUTS.md", 
        "QDRANT_SAVE_BEST_PRACTICES.md",
        "qdrant_helper.py",
        "MCP_OPTIMIZATIONS.md"
    )
    
    foreach ($file in $files) {
        Copy-Item "$TemplatePath\.devtools\$file" "$ProjectPath\.devtools\" -Force
    }
    
    # Erstelle VS Code Settings
    @"
{
    "github.copilot.chat.localeOverride": "de",
    "chat.mcp.autostart": "newAndOutdated"
}
"@ | Out-File -FilePath "$ProjectPath\.vscode\settings.json" -Encoding UTF8
    
    Write-Host "✅ Projekt erstellt!" -ForegroundColor Green
    Write-Host "📁 Pfad: $ProjectPath" -ForegroundColor Cyan
    
    # Öffne in VS Code
    code $ProjectPath
}

# Alias für schnelleren Zugriff
Set-Alias -Name new-project -Value New-VSCodeProject
```

### 3. Profil neu laden

```powershell
. $PROFILE
```

### 4. Verwenden

```powershell
# Neues Projekt erstellen
new-project MeinProjekt

# Oder mit custom Pfad
new-project MeinProjekt -Path C:\dev
```

---

## 📁 Alternative: Batch Script

### Erstelle `new-project.bat`:

```batch
@echo off
setlocal EnableDelayedExpansion

set PROJECT_NAME=%1
set PROJECT_PATH=%2

if "%PROJECT_NAME%"=="" (
    echo Fehler: Projektname erforderlich
    echo Verwendung: new-project.bat ^<name^> [pfad]
    exit /b 1
)

if "%PROJECT_PATH%"=="" (
    set PROJECT_PATH=%USERPROFILE%\projects\%PROJECT_NAME%
) else (
    set PROJECT_PATH=%PROJECT_PATH%\%PROJECT_NAME%
)

echo Erstelle Projekt: %PROJECT_NAME%
echo Pfad: %PROJECT_PATH%

REM Erstelle Verzeichnisse
mkdir "%PROJECT_PATH%\.github" 2>nul
mkdir "%PROJECT_PATH%\.devtools" 2>nul
mkdir "%PROJECT_PATH%\.vscode" 2>nul

REM Kopiere Files
set TEMPLATE_PATH=%USERPROFILE%\Desktop\Einkaufen

xcopy /Y "%TEMPLATE_PATH%\.github\copilot-instructions.md" "%PROJECT_PATH%\.github\"
xcopy /Y "%TEMPLATE_PATH%\.devtools\*.md" "%PROJECT_PATH%\.devtools\"
xcopy /Y "%TEMPLATE_PATH%\.devtools\*.py" "%PROJECT_PATH%\.devtools\"

REM Erstelle Settings
(
echo {
echo     "github.copilot.chat.localeOverride": "de",
echo     "chat.mcp.autostart": "newAndOutdated"
echo }
) > "%PROJECT_PATH%\.vscode\settings.json"

echo.
echo ✅ Projekt erstellt!
echo.
echo Öffne in VS Code:
echo   code "%PROJECT_PATH%"

REM Optional: Automatisch öffnen
code "%PROJECT_PATH%"
```

### Verwendung:

```cmd
new-project.bat MeinProjekt
```

---

## 🎯 Zu PATH hinzufügen

### Option A: User PATH (Empfohlen)

1. **Script erstellen:**
   ```powershell
   # Speichere Script
   $ScriptPath = "$HOME\bin"
   New-Item -ItemType Directory -Force -Path $ScriptPath
   
   # Kopiere PowerShell Script
   Copy-Item .devtools\init-vscode-project.ps1 $ScriptPath\
   ```

2. **Zu PATH hinzufügen:**
   ```powershell
   # Öffne Systemsteuerung
   SystemPropertiesAdvanced
   
   # Oder mit PowerShell:
   $CurrentPath = [Environment]::GetEnvironmentVariable("Path", "User")
   $NewPath = "$CurrentPath;$HOME\bin"
   [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
   ```

3. **Verwenden:**
   ```powershell
   init-vscode-project.ps1 MeinProjekt
   ```

---

## 🔄 Windows Terminal Integration

### `settings.json` ergänzen:

```json
{
  "profiles": {
    "list": [
      {
        "name": "New Project",
        "commandline": "powershell.exe -NoExit -Command \"New-VSCodeProject\"",
        "icon": "📁"
      }
    ]
  }
}
```

---

## 🎨 VS Code Task (Windows)

### `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Create New Project",
      "type": "shell",
      "command": "powershell",
      "args": [
        "-ExecutionPolicy", "Bypass",
        "-File", "${workspaceFolder}\\.devtools\\init-vscode-project.ps1",
        "-ProjectName", "${input:projectName}",
        "-ProjectPath", "${input:projectPath}"
      ],
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "projectName",
      "type": "promptString",
      "description": "Projektname"
    },
    {
      "id": "projectPath",
      "type": "promptString",
      "description": "Projekt-Pfad (oder leer für Standard)",
      "default": ""
    }
  ]
}
```

### Verwendung:
```
Ctrl+Shift+P → Tasks: Run Task → Create New Project
```

---

## ⚡ Schnellzugriff via Startmenü

### Erstelle Shortcut:

1. **Rechtsklick auf Desktop → Neu → Verknüpfung**

2. **Ziel:**
   ```
   powershell.exe -NoExit -Command "& {param($name) New-VSCodeProject $name}" -args
   ```

3. **Name:** "New VS Code Project"

4. **Icon:** VS Code Icon wählen

5. **Verwendung:**
   - Doppelklick
   - Projektname eingeben

---

## 🎯 Empfehlung für Windows

**Beste Lösung: PowerShell Profil + Alias**

1. **Einmalig Setup:**
   ```powershell
   # Führe .devtools/init-vscode-project.ps1 aus
   . $HOME\Desktop\Einkaufen\.devtools\init-vscode-project.ps1
   
   # Füge zu Profil hinzu
   Add-Content $PROFILE @"
   
   # VS Code Project Template
   function New-VSCodeProject {
       param([string]`$Name, [string]`$Path = "`$HOME\projects")
       & "`$HOME\Desktop\Einkaufen\.devtools\init-vscode-project.ps1" -ProjectName `$Name -ProjectPath `$Path
   }
   Set-Alias new-project New-VSCodeProject
   "@
   
   . $PROFILE
   ```

2. **Verwenden:**
   ```powershell
   new-project MeinProjekt
   ```

3. **Überall verfügbar:**
   - ✅ PowerShell
   - ✅ Windows Terminal
   - ✅ VS Code Terminal
   - ✅ Git Bash (mit Wrapper)

---

## 🔍 Troubleshooting

### "Skriptausführung deaktiviert"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Pfad nicht gefunden"

```powershell
# Prüfe Template-Pfad
Test-Path "$HOME\Desktop\Einkaufen\.github\copilot-instructions.md"

# Falls Pfad anders, update in Funktion:
$TemplatePath = "C:\dein\pfad\zur\grocery-app"
```

### Script erscheint nicht in PATH

```powershell
# Reload Environment
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

---

## ✅ Test

```powershell
# Test-Projekt erstellen
new-project TestProjekt

# Prüfe Dateien
Test-Path TestProjekt\.github\copilot-instructions.md  # Sollte True sein
Test-Path TestProjekt\.devtools\*.md  # Sollte Files finden

# Öffne in VS Code
cd TestProjekt
code .

# Teste Qdrant MCP
# Im VS Code Chat: /qd test
```

---

**💡 Tipp:** Speichere das PowerShell-Profil in Git für Backup!

```powershell
Copy-Item $PROFILE $HOME\Desktop\Einkaufen\.devtools\powershell-profile.ps1
```
