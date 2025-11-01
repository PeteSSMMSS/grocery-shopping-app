# Qdrant Kurzbefehl-System

## Kurzbefehl

**`/qd` triggert Qdrant MCP Server**

Einfach `/qd` gefolgt von deiner Frage verwenden.

## Beispiele

```
/qd ssh credentials
/qd deploy workflow
/qd api endpoints
/qd docker ports
/qd database config
/qd fix error message
/qd code pattern async
```

## Vorteile

- ✅ **Kürzer:** `/qd ssh` statt langer Anfragen
- ✅ **Schneller:** Direkter Zugriff auf Qdrant MCP
- ✅ **Intuitiv:** Ein Befehl für alles
- ✅ **Projektübergreifend:** Wissen aus allen Projekten

## Wie es funktioniert

1. Copilot erkennt `/qd` als Trigger
2. Nutzt automatisch Qdrant MCP Server (`qdrant-find` Tool)
3. Sucht nach relevanten Informationen
4. Gibt kurze, direkte Antwort

## Antwort-Stil

- ✅ **Kurz & direkt:** Nur die Antwort
- ✅ **Konkret:** Commands, IPs, Configs
- ❌ **NICHT:** Lange Einleitungen

## Test-Anfragen

```
/qd ssh
/qd deploy
/qd api
/qd docker ports
/qd fix docker container startet nicht
```

## Technische Details

- **Implementierung:** Copilot Instructions (`.github/copilot-instructions.md`)
- **Backend:** Qdrant MCP Server (`.vscode/mcp.json`)
- **Collection:** `project_knowledge`
- **Server:** `http://localhost:6333`

## Erweiterung

Weitere Kurzbefehle hinzufügen:
1. Öffne `.github/copilot-instructions.md`
2. Ergänze Tabelle unter "🔥 Kurzbefehl-Trigger"
3. Speichern & VS Code neu laden

Beispiel:
```markdown
| `?db` | Datenbank-Credentials | `?db postgres` |
```
