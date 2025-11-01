# MCP Optimierungen für VS Code

Basierend auf der offiziellen VS Code MCP-Dokumentation (v1.102+)

## ✅ Implementierte Optimierungen

### 1. **Automatischer Start aktiviert** ✅
```json
"chat.mcp.autostart": "newAndOutdated"
```
- ✅ MCP Server startet automatisch bei Config-Änderungen
- ✅ Neustart bei veralteten Servern
- ✅ Kein manuelles Refresh mehr nötig

### 2. **MCP Access Control**
```json
"chat.mcp.access": "all"
```
- Erlaubt alle MCP Server (Default)
- Alternativen: `"registry"` (nur Registry), `"none"` (keine)

### 3. **Autodiscovery deaktiviert**
```json
"chat.mcp.discovery.enabled": false
```
- ✅ Keine automatische Erkennung von Claude Desktop Config
- ✅ Nur explizit konfigurierte Server werden geladen
- ✅ Bessere Kontrolle über verwendete Server

### 4. **Virtual Tools Threshold**
```json
"github.copilot.chat.virtualTools.threshold": 64
```
- ✅ Löst das "128 Tools"-Limit-Problem
- ✅ Aktiviert virtuelle Tools ab 64 Tools
- ✅ Wichtig wenn viele MCP Server installiert sind

### 5. **Qdrant Docker-Optimierung**
```json
{
  "command": "docker",
  "args": [
    "run",
    "--rm",
    "-i",
    "--network", "host",  // ← Kein -p Port-Mapping mehr nötig
    "-e", "QDRANT_URL=http://localhost:6333",
    "-e", "QDRANT_API_KEY=",
    "-e", "COLLECTION_NAME=project_knowledge",
    "mcp-server-qdrant"
  ],
  "type": "stdio"  // ← Wichtig: NICHT detached mode (-d)!
}
```
- ✅ Entfernt unnötiges `-p 8000:8000` (wegen `--network host`)
- ✅ `--rm` löscht Container nach Stop
- ✅ `-i` für interaktive stdio-Kommunikation
- ✅ **KEIN `-d`** (detached mode würde stdio blockieren!)

---

## 📊 Settings-Übersicht

### User Settings (`settings.json`)
```json
{
  // MCP Settings
  "chat.mcp.autostart": "newAndOutdated",
  "chat.mcp.access": "all",
  "chat.mcp.discovery.enabled": false,
  
  // Virtual Tools (wichtig für viele MCP Server)
  "github.copilot.chat.virtualTools.threshold": 64
}
```

### MCP Config (`mcp.json`)
```json
{
  "servers": {
    "qdrant": {
      "command": "docker",
      "args": [...],
      "type": "stdio"  // Wichtig für Docker!
    }
  },
  "inputs": []
}
```

---

## 🚀 Weitere Optimierungsideen (Optional)

### 1. **Settings Sync für MCP Server**
- Aktiviere Settings Sync in VS Code
- `Ctrl+Shift+P` → `Settings Sync: Configure`
- Stelle sicher dass "MCP Servers" aktiviert ist
- ✅ MCP Server werden über alle Geräte synchronisiert

### 2. **Tool Sets erstellen**
Gruppiere verwandte Tools für bessere Organisation:

`.vscode/tool-sets.json`:
```json
{
  "toolSets": [
    {
      "name": "Infrastructure",
      "description": "Server, Docker, Deployment",
      "tools": [
        "qdrant.qdrant-find",
        "qdrant.qdrant-store"
      ]
    }
  ]
}
```

### 3. **MCP Server mit Dev Mode**
Für Entwicklung eigener MCP Server:

```json
{
  "servers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "type": "stdio",
      "dev": {
        "watch": "src/**/*.js",  // Auto-restart bei Änderungen
        "debug": {
          "type": "node",
          "port": 9229
        }
      }
    }
  }
}
```

### 4. **Input Variables für Secrets**
Falls du später API Keys brauchst:

```json
{
  "servers": {
    "api-server": {
      "command": "node",
      "args": ["server.js"],
      "type": "stdio",
      "env": {
        "API_KEY": "${input:apiKey}"
      }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "apiKey",
      "description": "Enter your API Key",
      "password": true
    }
  ]
}
```

### 5. **Workspace-spezifische MCP Server**
Für projektspezifische Server:

`.vscode/mcp.json`:
```json
{
  "servers": {
    "project-specific": {
      "command": "uvx",
      "args": ["mcp-server-filesystem", "${workspaceFolder}"],
      "type": "stdio"
    }
  }
}
```

---

## 🔍 Troubleshooting-Befehle

### MCP Server Management
```
MCP: List Servers          → Alle Server anzeigen
MCP: Reset Cached Tools    → Tool-Cache löschen
MCP: Reset Trust           → Trust-Status zurücksetzen
MCP: Open User Configuration → User mcp.json öffnen
```

### Tool Management
```
Ctrl+Alt+I                 → Chat öffnen
# im Chat                  → Tools per Name referenzieren
Tools-Button               → Tools aktivieren/deaktivieren
```

### Logs & Debugging
```
MCP: List Servers → Show Output  → Server-Logs anzeigen
Output Panel → MCP              → Alle MCP Logs
```

---

## 📝 Best Practices

### Server Naming
- ✅ **CamelCase:** `githubIntegration`, `databaseAccess`
- ❌ **Nicht:** `github-integration`, `database access`
- ✅ **Eindeutig:** Keine Duplikate
- ✅ **Beschreibend:** Funktionalität erkennbar

### Tool Limits
- **Maximum:** 128 Tools pro Chat-Request
- **Lösung:** Virtual Tools aktivieren (`threshold: 64`)
- **Alternative:** Tool Sets verwenden

### Security
- ⚠️ Nur vertrauenswürdige MCP Server verwenden
- ⚠️ Server-Config vor Start prüfen
- ⚠️ Input Variables für Secrets verwenden
- ⚠️ Keine API Keys direkt in Config

---

## ✅ Aktueller Status

- ✅ **Auto-Start:** Aktiviert
- ✅ **Qdrant MCP:** Global konfiguriert
- ✅ **Virtual Tools:** Aktiviert (Threshold 64)
- ✅ **Autodiscovery:** Deaktiviert
- ✅ **Docker Optimiert:** Kein Port-Mapping mehr nötig

---

## 🔗 Ressourcen

- [VS Code MCP Docs](https://code.visualstudio.com/docs/copilot/copilot-mcp-servers)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Qdrant MCP Server](https://github.com/qdrant/mcp-server-qdrant)
