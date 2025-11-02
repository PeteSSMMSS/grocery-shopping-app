# 🚀 Schnellstart - Neues Projekt erstellen

## ✅ 3 einfache Methoden

### Methode 1: Doppelklick (Einfachste) ⭐

1. **Navigiere zu:**
   ```
   Desktop\Einkaufen\.devtools\
   ```

2. **Doppelklick auf:**
   ```
   new-project.bat
   ```

3. **Projektname eingeben**

4. **VS Code öffnen? → `j`**

**Fertig! ✅**

---

### Methode 2: PowerShell direkt

```powershell
# Öffne PowerShell in beliebigem Ordner
cd ~\Desktop\Einkaufen\.devtools

# Führe aus
.\new-project-standalone.ps1

# Oder mit Projektname:
.\new-project-standalone.ps1 -ProjectName MeinProjekt
```

---

### Methode 3: Von überall (nach Setup)

#### Einmalig einrichten:

```powershell
# Öffne PowerShell
notepad $PROFILE
```

**Füge ein:**
```powershell
function new-project {
    param([string]$Name)
    & "$HOME\Desktop\Einkaufen\.devtools\new-project-standalone.ps1" -ProjectName $Name
}
```

**Speichern & Reload:**
```powershell
. $PROFILE
```

#### Dann überall verwenden:

```powershell
new-project MeinProjekt
```

---

## 📋 Was passiert automatisch

```
MeinProjekt/
├── .github/
│   └── copilot-instructions.md    ✓ Beast Mode 4.0
├── .devtools/
│   ├── QDRANT_MCP_SETUP.md       ✓ Qdrant Setup
│   ├── QDRANT_SHORTCUTS.md       ✓ /qd Befehle
│   ├── QDRANT_SAVE_BEST_PRACTICES.md ✓ Guidelines
│   ├── qdrant_helper.py          ✓ Helper
│   ├── MCP_OPTIMIZATIONS.md      ✓ VS Code MCP
│   └── README.md                 ✓ Übersicht
└── .vscode/
    └── settings.json             ✓ Copilot Settings
```

---

## ✨ Sofort nach Projekt-Erstellung

1. **VS Code öffnet automatisch**
2. **Copilot Instructions aktiv**
3. **`/qd` Befehle funktionieren**
4. **Qdrant Langzeitgedächtnis verfügbar**

### Testen:

```
Ctrl+Alt+I (Chat öffnen)
/qd ssh
```

→ Sollte SSH-Zugangsdaten aus Qdrant zeigen!

---

## 🔧 Troubleshooting

### "Ausführungsrichtlinie"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Template nicht gefunden"

Prüfe ob Pfad stimmt:
```powershell
Test-Path "$HOME\Desktop\Einkaufen\.github\copilot-instructions.md"
```

Falls False, passe Pfad in `new-project-standalone.ps1` an:
```powershell
$TemplatePath = "C:\dein\pfad\zu\Einkaufen"
```

### "PowerShell Profil nicht gefunden"

```powershell
# Erstelle Profil
New-Item -Path $PROFILE -ItemType File -Force
notepad $PROFILE
```

---

## 🎯 Empfehlung

**Für schnellen Start: Methode 1 (Doppelklick)**

Später kannst du auf Methode 3 (PowerShell Profil) upgraden für noch mehr Komfort.

---

## 📝 Beispiel-Session

```powershell
# Start
C:\> cd Desktop\Einkaufen\.devtools
C:\Desktop\Einkaufen\.devtools> .\new-project.bat

========================================
  VS Code Projekt Creator
========================================

Projektname: awesome-api

🚀 Erstelle Projekt: awesome-api
📁 Pfad: C:\Users\...\projects\awesome-api

📁 Erstelle Verzeichnisse...
   ✓ Verzeichnisse erstellt
📋 Kopiere Copilot Instructions...
   ✓ copilot-instructions.md
🔧 Kopiere Dev-Tools...
   ✓ 6 Dev-Tool Dateien kopiert
   ✓ README.md
   ✓ settings.json

✅ Projekt erfolgreich erstellt!

📊 Erstellt:
   • .github/copilot-instructions.md
   • .devtools/ (6 Dateien)
   • .vscode/settings.json

📁 Projekt-Pfad:
   C:\Users\...\projects\awesome-api

VS Code jetzt öffnen? (j/n): j
🚀 Öffne VS Code...

# VS Code öffnet → Fertig! ✅
```

---

**💡 Tipp:** Erstelle Verknüpfung auf Desktop zu `new-project.bat` für noch schnelleren Zugriff!

```
Rechtsklick auf new-project.bat
→ Verknüpfung erstellen
→ Auf Desktop ziehen
→ Umbenennen zu "Neues VS Code Projekt"
```
