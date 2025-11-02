#!/bin/bash
# VS Code Projekt-Initialisierung Script
# Kopiert Copilot Instructions und Dev-Tools in neues Projekt

set -e

PROJECT_NAME="$1"
PROJECT_PATH="${2:-.}"

if [ -z "$PROJECT_NAME" ]; then
    echo "❌ Fehler: Projektname erforderlich"
    echo "Verwendung: ./init-vscode-project.sh <projekt-name> [pfad]"
    exit 1
fi

echo "🚀 Initialisiere VS Code Projekt: $PROJECT_NAME"
echo "📁 Pfad: $PROJECT_PATH"
echo ""

# Template-Pfad (dieses Projekt als Template)
TEMPLATE_PATH="$(dirname "$0")/.."

# Erstelle Verzeichnisse
mkdir -p "$PROJECT_PATH/.github"
mkdir -p "$PROJECT_PATH/.vscode"
mkdir -p "$PROJECT_PATH/.devtools"

# Kopiere Copilot Instructions
echo "📋 Kopiere Copilot Instructions..."
cp "$TEMPLATE_PATH/.github/copilot-instructions.md" "$PROJECT_PATH/.github/"
echo "   ✓ .github/copilot-instructions.md"

# Kopiere Dev-Tools
echo "🔧 Kopiere Dev-Tools..."
cp "$TEMPLATE_PATH/.devtools/QDRANT_MCP_SETUP.md" "$PROJECT_PATH/.devtools/"
cp "$TEMPLATE_PATH/.devtools/QDRANT_SHORTCUTS.md" "$PROJECT_PATH/.devtools/"
cp "$TEMPLATE_PATH/.devtools/QDRANT_SAVE_BEST_PRACTICES.md" "$PROJECT_PATH/.devtools/"
cp "$TEMPLATE_PATH/.devtools/qdrant_helper.py" "$PROJECT_PATH/.devtools/"
cp "$TEMPLATE_PATH/.devtools/MCP_OPTIMIZATIONS.md" "$PROJECT_PATH/.devtools/"
echo "   ✓ Dev-Tools kopiert"

# Erstelle README
cat > "$PROJECT_PATH/.devtools/README.md" << 'EOF'
# Dev-Tools für dieses Projekt

## 📚 Dokumentation

- **QDRANT_MCP_SETUP.md** - Qdrant MCP Server Setup
- **QDRANT_SHORTCUTS.md** - Kurzbefehl-System (`/qd`)
- **QDRANT_SAVE_BEST_PRACTICES.md** - Best Practices für Speichern
- **MCP_OPTIMIZATIONS.md** - MCP Optimierungen

## 🔧 Tools

- **qdrant_helper.py** - Helper-Script für Qdrant

## 🎯 Copilot Instructions

Die Copilot Instructions liegen in `.github/copilot-instructions.md`.

Diese beinhalten:
- Beast Mode 4.0 Workflow
- Qdrant Langzeitgedächtnis Integration
- MCP Server Tools
- Best Practices

## 🚀 Schnellstart

1. **Qdrant läuft bereits global** (Port 6333)
2. **MCP Server konfiguriert** (`%APPDATA%\Code\User\mcp.json`)
3. **Sofort loslegen:**
   ```
   /qd ssh
   /qd deploy
   ```

## 📝 Wissen speichern

```python
python .devtools/qdrant_helper.py
```

Oder im Chat:
```
"Speichere in Qdrant: [deine Infos]"
```
EOF

echo "   ✓ .devtools/README.md"

# Erstelle .gitignore für Dev-Tools
cat > "$PROJECT_PATH/.devtools/.gitignore" << 'EOF'
# Lokale Notizen
notes/
*.local.*

# Temporäre Dateien
*.tmp
*.swp
EOF

# Erstelle Projekt-spezifische Qdrant-Daten (optional)
cat > "$PROJECT_PATH/.devtools/project_data.json" << EOF
{
  "project": "$PROJECT_NAME",
  "created": "$(date +%Y-%m-%d)",
  "qdrant": {
    "collection": "project_knowledge",
    "url": "http://localhost:6333"
  }
}
EOF

echo "   ✓ project_data.json"

# Erstelle .vscode/settings.json wenn nicht vorhanden
if [ ! -f "$PROJECT_PATH/.vscode/settings.json" ]; then
    cat > "$PROJECT_PATH/.vscode/settings.json" << 'EOF'
{
    "github.copilot.chat.localeOverride": "de",
    "chat.mcp.autostart": "newAndOutdated"
}
EOF
    echo "   ✓ .vscode/settings.json"
fi

echo ""
echo "✅ Projekt initialisiert!"
echo ""
echo "📊 Erstellt:"
echo "   .github/copilot-instructions.md"
echo "   .devtools/ (5 Dateien)"
echo "   .vscode/settings.json"
echo ""
echo "🎯 Nächste Schritte:"
echo "   1. cd $PROJECT_PATH"
echo "   2. code ."
echo "   3. Ctrl+Shift+P → Developer: Reload Window"
echo "   4. /qd test"
echo ""
