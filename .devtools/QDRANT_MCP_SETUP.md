# Qdrant MCP Server - Setup & Verwendung

## 📦 Installation

Der Qdrant MCP Server ermöglicht GitHub Copilot den direkten Zugriff auf das Qdrant Langzeitgedächtnis via MCP-Protokoll.

### Voraussetzungen

- ✅ Docker Desktop installiert
- ✅ Qdrant Container läuft (`http://localhost:6333`)
- ✅ VS Code mit GitHub Copilot

### Setup

1. **Docker Image gebaut:**
   ```bash
   cd /tmp/mcp-server-qdrant
   docker build -t mcp-server-qdrant .
   ```

2. **Workspace MCP Config erstellt:**
   - Datei: `.vscode/mcp.json`
   - Server: `qdrant`
   - Format: Neues MCP-Format (nicht `github.copilot.chat.mcp.servers`)

3. **VS Code neu laden:**
   - `Ctrl+Shift+P` → `Developer: Reload Window`

---

## 🚀 Verwendung

### Verfügbare MCP Tools

Nach dem Setup stehen Copilot folgende Tools zur Verfügung:

1. **`qdrant-store`**
   - Speichert Informationen in Qdrant
   - Input: `information` (String), optional `metadata` (JSON)
   - Collection: `project_knowledge`

2. **`qdrant-find`**
   - Sucht relevante Informationen in Qdrant
   - Input: `query` (String)
   - Collection: `project_knowledge`

### Beispiel-Anfragen

**Wissen speichern:**
```
@workspace Speichere in Qdrant: Die neue Grocery API ist unter Port 9000 erreichbar
```

**Wissen abrufen:**
```
@workspace Durchsuche Qdrant nach SSH-Zugangsdaten für die NAS
```

```
@workspace Welche Docker-Ports sind dokumentiert? (Suche in Qdrant)
```

---

## 🔧 Konfiguration

### Environment Variables

- `FASTMCP_HOST=127.0.0.1` - Server hört nur auf localhost
- `QDRANT_URL=http://localhost:6333` - Lokaler Qdrant-Server
- `COLLECTION_NAME=project_knowledge` - Datenbank-Collection
- `TOOL_STORE_DESCRIPTION` - Anleitung für Copilot (Speichern)
- `TOOL_FIND_DESCRIPTION` - Anleitung für Copilot (Suchen)

### Netzwerk

- `--network host` - Container nutzt Host-Netzwerk (Zugriff auf `localhost:6333`)
- Kein API Key nötig (lokaler Qdrant ohne Auth)

---

## 🐛 Troubleshooting

### Problem: MCP Server startet nicht

**Lösung 1: Qdrant Container prüfen**
```bash
docker ps | grep qdrant
# Sollte qdrant-local zeigen
```

**Lösung 2: MCP Server Logs anzeigen**
- `Ctrl+Shift+P` → `MCP: List Servers`
- Wähle `qdrant`
- Klicke `Show Output`

**Lösung 3: Docker Image neu bauen**
```bash
cd /tmp/mcp-server-qdrant
docker build -t mcp-server-qdrant . --no-cache
```

### Problem: "Collection not found"

**Lösung:**
```bash
python .devtools/save_project_summary.py
# Erstellt Collection und befüllt mit Daten
```

### Problem: Copilot zeigt MCP Tools nicht

**Lösung:**
1. VS Code neu laden: `Ctrl+Shift+P` → `Developer: Reload Window`
2. Warten (MCP Server startet beim ersten Zugriff, nicht automatisch)
3. Test: `@workspace Welche MCP Tools sind verfügbar?`

---

## 📊 Datenbank-Status

### Qdrant prüfen

```bash
# Anzahl Einträge
python -c "
import json, urllib.request
with urllib.request.urlopen('http://localhost:6333/collections/project_knowledge') as r:
    data = json.loads(r.read())
    print(f\"Einträge: {data['result']['points_count']}\")
"
```

### Dashboard öffnen

```
http://localhost:6333/dashboard
```

---

## 🔄 Updates

### MCP Server aktualisieren

```bash
cd /tmp/mcp-server-qdrant
git pull origin main
docker build -t mcp-server-qdrant . --no-cache
```

### VS Code Settings aktualisieren

Nach Änderungen in `settings.json`:
1. Speichern (`Ctrl+S`)
2. Reload Window (`Ctrl+Shift+P` → `Developer: Reload Window`)

---

## 📝 Hinweise

- **Performance:** MCP Server startet beim ersten Tool-Aufruf (ca. 10-20s)
- **Offline:** MCP Server benötigt laufenden Qdrant-Container
- **Security:** Aktuell nur lokaler Zugriff (keine Remote-Authentifizierung)
- **Alternative:** REST API via Copilot Instructions (siehe `.github/copilot-instructions.md`)

---

## 🎯 Nächste Schritte

1. VS Code neu laden: `Ctrl+Shift+P` → `Developer: Reload Window`
2. Warten (~30 Sekunden)
3. Testen: `@workspace Welche MCP Tools sind verfügbar?`
4. Verwenden: `@workspace Durchsuche Qdrant nach NAS-Informationen`

**Dokumentation:** `.github/copilot-instructions.md` (REST API Patterns)  
**Dashboard:** http://localhost:6333/dashboard
