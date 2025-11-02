# 💾 Backup & Synchronisation Workflow

Regelmäßige Backups sind essentiell für Datensicherheit und Projektkontinuität.

---

## 🎯 Ziel

**Zwei-Stufen-Backup:**
1. **Git/GitHub** - Code & Files (Versionskontrolle)
2. **Qdrant DB** - Wissen & Metadaten (Langzeitgedächtnis)

---

## ⏰ Wann Backup erstellen?

### Automatisch triggern nach:

- ✅ **Feature-Implementierung**
- ✅ **Bugfixes** (wichtige)
- ✅ **Deployment-Änderungen**
- ✅ **Neue Konfigurationen** (Docker, CI/CD)
- ✅ **Architektur-Entscheidungen**
- ✅ **Refactorings**

### Oder auf Anfrage:

- "Sichere das Projekt"
- "Backup erstellen"
- "Push zu GitHub"
- "Speichere in Qdrant"

### Mindestens:

- **Täglich** bei aktiver Entwicklung
- **Vor größeren Änderungen**
- **Nach Deployment** zu Production

---

## 1️⃣ Git/GitHub Backup

### Workflow

```bash
# 1. Status prüfen
git status

# 2. Änderungen stagen
git add .

# 3. Commit mit detailliertem Kommentar
git commit -m "feat: Feature-Name - Kurzbeschreibung

Detaillierte Beschreibung:
- Was wurde implementiert
- Welche Files geändert
- Warum diese Änderung
- Test-Status

Breaking Changes: [falls vorhanden]
Issues: #123, #456
"

# 4. Push zu GitHub
git push origin main
```

---

### Commit-Message Format

**Schema:**
```
<type>: <Zusammenfassung in max. 50 Zeichen>

<Detaillierte Beschreibung>
- Bullet-Point 1
- Bullet-Point 2

<Optional: Breaking Changes, Issues>
```

**Types:**

| Type | Verwendung | Beispiel |
|------|------------|----------|
| `feat` | Neues Feature | `feat: Add meal planning` |
| `fix` | Bugfix | `fix: Resolve login timeout` |
| `refactor` | Code-Umstrukturierung | `refactor: Extract auth logic` |
| `docs` | Dokumentation | `docs: Update API guide` |
| `chore` | Wartung, Dependencies | `chore: Update dependencies` |
| `test` | Tests | `test: Add unit tests` |
| `perf` | Performance | `perf: Optimize DB queries` |
| `ci` | CI/CD | `ci: Add GitHub Actions` |

---

### Beispiel: Guter Commit

```
feat: Add Qdrant MCP Server Integration

Integriert Qdrant als Langzeitgedächtnis für Copilot:
- MCP Server global konfiguriert in mcp.json
- `/qd` Kurzbefehl für schnelle Abfragen
- Automatisches Speichern von Projekt-Infos
- Helper-Scripts für Datenmanagement

Files:
- .devtools/qdrant_helper.py (neu)
- .devtools/QDRANT_MCP_SETUP.md (neu)
- .github/copilot-instructions.md (aktualisiert)
- README.md (Qdrant-Sektion hinzugefügt)

Testing:
✅ Lokal getestet
✅ /qd Befehle funktionieren
✅ MCP Server connected

Breaking Changes: Keine
```

---

### Beispiel: Schlechter Commit ❌

```
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

**Problem:**
- Keine Details
- Nicht nachvollziehbar
- Nicht hilfreich bei Code-Review
- Schwer zu revertn

---

## 2️⃣ Qdrant DB Backup

### Was speichern?

**Projekt-Metadaten:**
- ✅ Projekt-Name & Zweck
- ✅ Tech-Stack
- ✅ Deployment-Workflows
- ✅ API-Endpoints & Ports
- ✅ Wichtige Entscheidungen
- ✅ Code-Patterns
- ✅ Troubleshooting-Lösungen

---

### Template für Projekt-Info

```python
{
    "id": 600,  # Deployment-Kategorie
    "vector": [0.0] * 384,
    "payload": {
        "title": "Grocery App - Deployment Workflow",
        "content": """Grocery Shopping App

Tech-Stack:
- Backend: FastAPI + Python
- Frontend: React + TypeScript + Vite
- Database: PostgreSQL
- Deployment: Docker Compose auf Synology NAS

Deployment auf NAS:
1. ssh Pierre@192.168.178.123
2. cd /volume1/docker/einkaufen
3. git pull origin main
4. /usr/local/bin/docker-compose down
5. /usr/local/bin/docker-compose up -d --build
6. /usr/local/bin/docker-compose logs -f

Ports:
- API: 8080
- Web: 5173  
- PostgreSQL: 5588

URLs:
- Production: http://192.168.178.123:5173
- API: http://192.168.178.123:8080/docs

Letzte Änderung: 2025-11-01
Status: ✅ Production
""",
        "keywords": [
            "grocery", "app", "deployment", "docker",
            "fastapi", "react", "typescript", "postgresql",
            "nas", "synology", "production", "workflow"
        ],
        "category": "deployment",
        "project": "grocery-shopping-app",
        "date": "2025-11-01"
    }
}
```

---

### Speichern via Helper-Script

```python
# .devtools/qdrant_helper.py
from qdrant_helper import save_to_qdrant

save_to_qdrant(
    title="Grocery App - Deployment",
    content="...",  # Siehe Template oben
    keywords=["grocery", "app", "deployment", ...],
    category="deployment"
)
```

---

### Speichern via REST API

```python
import json, urllib.request

entry = {
    "id": 600,
    "vector": [0.0] * 384,
    "payload": {
        "title": "Projekt-Name - Beschreibung",
        "content": "Detaillierte Infos...",
        "keywords": ["keyword1", "keyword2", ...],
        "category": "deployment",
        "project": "projekt-name",
        "date": "2025-11-01"
    }
}

req = urllib.request.Request(
    "http://localhost:6333/collections/project_knowledge/points",
    data=json.dumps({"points": [entry]}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='PUT'
)
urllib.request.urlopen(req)
```

---

## 🤖 Copilot Workflow

### Nach Feature-Implementierung

**Copilot fragt automatisch:**

```
✅ Feature "Meal Planning" erfolgreich implementiert!

📊 Änderungen:
- api/app/routers/meals.py (neu)
- api/app/models.py (erweitert)
- web/src/components/MealsModal.tsx (aktualisiert)
- 8 neue API-Endpoints
- Tests: 12/12 passed

💾 Soll ich Backup erstellen?

1️⃣ Git Commit & Push:
   "feat: Add meal planning feature
   
   - Implementiert Meal-Management API
   - React Modal für Meal-Planung
   - Integration mit Shopping-Liste
   - Tests: 12/12 passed"

2️⃣ Qdrant Speichern:
   - API-Endpoints dokumentieren
   - React-Pattern speichern
   - Deployment-Notes aktualisieren

Durchführen? [1/2/beide/skip]
```

**User wählt:** `beide`

**Copilot führt aus:**

```bash
# 1. Git Backup
git add .
git commit -m "feat: Add meal planning feature..."
git push origin main
✅ Pushed to GitHub

# 2. Qdrant Backup
python .devtools/qdrant_helper.py save \
  --title "Grocery App - Meal Planning API" \
  --content "..." \
  --keywords "meals,api,fastapi,grocery" \
  --category "code-pattern"
✅ Gespeichert unter ID 402
```

---

### Proaktive Erinnerungen

**Bei vielen ungesicherten Änderungen:**

```
⚠️  Hinweis: 15 geänderte Dateien ohne Commit seit 2 Stunden.
💾 Backup empfohlen!

Soll ich jetzt ein Backup erstellen?
[Ja/Nein/Später]
```

**Bei wichtigen Entscheidungen:**

```
✅ Architektur-Entscheidung: Migration zu PostgreSQL

💾 Diese Entscheidung sollte dokumentiert werden:
1. Git Commit (Architektur-Änderung)
2. Qdrant (Entscheidungs-Rationale speichern)

Durchführen?
[Ja/Nein]
```

---

## 📅 Backup-Frequenz

### Empfohlen:

| Aktion | Git | Qdrant |
|--------|-----|--------|
| Feature fertig | ✅ Sofort | ✅ Ja |
| Bugfix (wichtig) | ✅ Sofort | Optional |
| Deployment-Änderung | ✅ Sofort | ✅ Wichtig! |
| Refactoring | ✅ Ja | Optional |
| Neue Pattern/Lösung | Optional | ✅ Ja |
| Config-Änderung | ✅ Ja | Optional |

### Mindestens:

- **Git:** Nach jedem abgeschlossenen Task
- **Qdrant:** Nach wichtigen Meilensteinen
- **Beide:** Täglich bei aktiver Entwicklung

---

## 🔄 Backup-Status prüfen

### Git Status

```bash
# Letzte Commits
git log --oneline -5

# Ungesicherte Änderungen
git status

# Differenzen
git diff

# Letzter Push
git log origin/main..HEAD
```

### Qdrant Status

```python
# Letzte gespeicherte Einträge
import urllib.request, json

req = urllib.request.Request(
    "http://localhost:6333/collections/project_knowledge/points/scroll",
    data=json.dumps({"limit": 5, "with_payload": True}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
result = json.loads(urllib.request.urlopen(req).read())

for point in result['result']['points']:
    print(f"ID {point['id']}: {point['payload']['title']} ({point['payload']['date']})")
```

---

## ✅ Backup-Checkliste

**Nach jeder größeren Änderung:**

- [ ] Git Status geprüft (`git status`)
- [ ] Alle Files gestaged (`git add .`)
- [ ] Detaillierter Commit-Kommentar
- [ ] Gepusht zu GitHub (`git push`)
- [ ] Projekt-Metadaten aktualisiert
- [ ] Wichtige Infos in Qdrant gespeichert
- [ ] Deployment-Workflow dokumentiert
- [ ] Neue Patterns/Lösungen archiviert

---

## 🆘 Recovery

### Git Rollback

```bash
# Letzten Commit rückgängig (lokal)
git reset --soft HEAD~1

# Letzten Commit rückgängig (remote - VORSICHT!)
git push --force

# Zu bestimmtem Commit zurück
git reset --hard <commit-hash>
```

### Qdrant Restore

```python
# Backup exportieren
import json, urllib.request

req = urllib.request.Request(
    "http://localhost:6333/collections/project_knowledge/points/scroll",
    data=json.dumps({"limit": 1000, "with_payload": True, "with_vector": True}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
result = json.loads(urllib.request.urlopen(req).read())

# Speichern
with open('qdrant_backup.json', 'w') as f:
    json.dump(result, f, indent=2)

# Restore
with open('qdrant_backup.json', 'r') as f:
    data = json.load(f)
    
req = urllib.request.Request(
    "http://localhost:6333/collections/project_knowledge/points",
    data=json.dumps({"points": data['result']['points']}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='PUT'
)
urllib.request.urlopen(req)
```

---

## 💡 Best Practices

1. **Commit early, commit often**
   - Kleine, atomare Commits
   - Jeder Commit = lauffähiger Zustand

2. **Beschreibende Messages**
   - Was & Warum dokumentieren
   - Kontext für später bereitstellen

3. **Branching nutzen**
   - Feature-Branches für große Changes
   - Main-Branch immer stabil

4. **Qdrant als zweite Ebene**
   - Git = Code & Files
   - Qdrant = Wissen & Entscheidungen

5. **Regelmäßig testen**
   - Nach Backup: Build & Tests laufen lassen
   - Sicherstellen dass alles funktioniert

---

**💾 Backup ist Pflicht, nicht optional!**
