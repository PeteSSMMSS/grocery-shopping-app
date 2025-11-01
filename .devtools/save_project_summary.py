#!/usr/bin/env python3
"""
Grocery Shopping App - Projekt-Zusammenfassung für Qdrant
Speichert detaillierte Informationen über Infrastructure, Credentials, Workflows
"""

import json
import urllib.request
from datetime import datetime

QDRANT_URL = "http://localhost:6333"
COLLECTION = "project_knowledge"

def create_vector():
    return [0.0] * 384

def get_project_summary_entries():
    """Detaillierte Projekt-Dokumentation"""
    v = create_vector()
    date = datetime.now().strftime("%Y-%m-%d")
    
    return [
        # === PROJEKT OVERVIEW ===
        {
            "id": 200,
            "vector": v,
            "payload": {
                "slug": "project-overview",
                "title": "Grocery Shopping App - Projekt-Übersicht",
                "content": """
Projekt: Grocery Shopping App (Einkaufs-Tracking & Verwaltung)
Repository: https://github.com/PeteSSMMSS/grocery-shopping-app
Branch: main
Owner: PeteSSMMSS

Zweck:
- Einkäufe tracken und verwalten
- Integration mit Home Assistant via AppDaemon
- API für Einkaufsdaten
- Web-Frontend für Verwaltung

Komponenten:
1. FastAPI Backend (Python) - Port 8082
2. React Frontend (TypeScript + Vite) - Port 80
3. PostgreSQL Datenbank - Port 5432 (intern)
4. Home Assistant AppDaemon Sensor
                """,
                "keywords": ["projekt", "overview", "grocery-app", "einkaufen", "tracking"],
                "category": "documentation",
                "project": "grocery-shopping-app",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === NAS INFRASTRUCTURE ===
        {
            "id": 201,
            "vector": v,
            "payload": {
                "slug": "nas-infrastructure-detailed",
                "title": "Synology NAS - Vollständige Infrastructure",
                "content": """
Synology NAS Details:

IP-Adresse: 192.168.178.122
Hostname: (nicht dokumentiert)

SSH-Zugang:
- Benutzer: admin
- Port: 22 (Standard)
- SSH-Key: ~/.ssh/nas_rsa
- Verbindung: ssh admin@192.168.178.122
- Key-Permissions: chmod 600 ~/.ssh/nas_rsa
- Alternative (ohne Key): ssh admin@192.168.178.122 -o PubkeyAuthentication=no

Docker auf NAS:
- Container-Basis-Pfad: /volume1/docker
- Alle Services unter diesem Pfad organisiert
- Docker Compose: /usr/local/bin/docker-compose
- Deployment: Via SSH + git pull + docker-compose

Wichtige Dienste auf NAS:
1. Home Assistant (Port 8123)
2. AppDaemon (Add-on in HA)
3. Docker Container (verschiedene Services)

Netzwerk-Shares:
- AppDaemon Config: \\\\192.168.178.122\\addon_configs\\a0d7b954_appdaemon
- Apps-Ordner: \\\\192.168.178.122\\addon_configs\\a0d7b954_appdaemon\\apps
- Grocery Sensor: grocery_sensor.py (in apps/)

Synology Drive:
- Windows Sync-Ordner: D:\\Cooperate Design
- Automatische Synchronisierung aktiv
- Backup-Ziel für wichtige Projekt-Daten
                """,
                "keywords": ["nas", "synology", "ssh", "docker", "infrastructure", "192.168.178.122", "admin", "credentials"],
                "category": "infrastructure",
                "project": "general",
                "date": date,
                "author": "project-summary",
                "sensitive": True
            }
        },
        
        # === HOME ASSISTANT ===
        {
            "id": 202,
            "vector": v,
            "payload": {
                "slug": "home-assistant-detailed",
                "title": "Home Assistant - Konfiguration & Integration",
                "content": """
Home Assistant Setup:

URL: http://192.168.178.122:8123
Installation: Auf Synology NAS (Docker/Add-on)

API-Zugang:
- API-Token: Gespeichert in .env als HA_TOKEN
- API-Endpoint: http://192.168.178.122:8123/api/
- Authentifizierung: Bearer Token

AppDaemon Integration:
- Version: Add-on in Home Assistant
- Config-Pfad: \\\\192.168.178.122\\addon_configs\\a0d7b954_appdaemon
- Apps-Ordner: apps/
- Logs: Über Home Assistant UI abrufbar

Grocery Sensor (grocery_sensor.py):
- Name: sensor.last_grocery_purchase
- Update-Intervall: 60 Sekunden
- Datenquelle: Grocery API (http://192.168.178.123:8082/api/purchase/history)
- Implementierung: Polling mit requests.Session()
- Pattern: Delayed start (5s) + run_every (60s)

Sensor-Attribute:
- state: Letzter Einkauf (Datum/Zeit)
- product_name: Name des Produkts
- category: Kategorie
- supermarket: Supermarkt
- price: Preis
- quantity: Menge
                """,
                "keywords": ["home-assistant", "appdaemon", "sensor", "api", "automation", "grocery", "token"],
                "category": "infrastructure",
                "project": "home-assistant",
                "date": date,
                "author": "project-summary",
                "sensitive": True
            }
        },
        
        # === GROCERY API ===
        {
            "id": 203,
            "vector": v,
            "payload": {
                "slug": "grocery-api-detailed",
                "title": "Grocery Shopping App API - Vollständige Dokumentation",
                "content": """
Grocery API Details:

Base URL: http://192.168.178.123:8082
Framework: FastAPI (Python 3.14)
Server-IP: 192.168.178.123

Haupt-Endpoints:
1. GET /api/purchase/history
   - Einkaufshistorie abrufen
   - Neueste Käufe zuerst
   - Genutzt von: Home Assistant Sensor

2. GET /api/products
   - Liste aller Produkte
   - Filter: Kategorie, Supermarkt
   
3. GET /api/categories
   - Alle verfügbaren Kategorien
   
4. POST /api/purchase
   - Neuen Einkauf registrieren
   
5. GET /api/supermarkets
   - Liste aller Supermärkte

Backend-Tech-Stack:
- Framework: FastAPI
- Python: 3.14.0
- Datenbank: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- Validation: Pydantic

Datenbank:
- Typ: PostgreSQL
- Host: db (Docker-internes Netzwerk)
- Port: 5432
- Name: grocery_db (vermutlich)
- Connection String: In docker-compose.yml als DATABASE_URL

Docker:
- Container-Name: grocery-api
- Port: 8082 (extern) → 8000 (intern)
- Dockerfile: api/Dockerfile
- Requirements: api/requirements.txt
                """,
                "keywords": ["grocery-api", "fastapi", "api", "endpoints", "backend", "192.168.178.123", "8082", "postgresql"],
                "category": "infrastructure",
                "project": "grocery-shopping-app",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === FRONTEND ===
        {
            "id": 204,
            "vector": v,
            "payload": {
                "slug": "grocery-frontend-detailed",
                "title": "Grocery App Frontend - Architektur",
                "content": """
Web Frontend:

URL: http://192.168.178.123:80 (vermutlich)
Framework: React 18
Language: TypeScript
Build Tool: Vite

Tech Stack:
- React + TypeScript
- Vite (Build & Dev Server)
- TailwindCSS (Styling)
- Dexie.js (IndexedDB für Offline-Support)
- React Router (Navigation)

Komponenten-Struktur:
- App.tsx: Haupt-App-Komponente
- CatalogPane.tsx: Produktkatalog
- ListPane.tsx: Einkaufsliste
- MealsModal.tsx: Mahlzeiten-Planung
- CalendarModal.tsx: Kalender-Ansicht
- SettingsModal.tsx: Einstellungen
- Toast.tsx: Benachrichtigungen

Services:
- api.ts: API-Client für Backend
- db.dexie.ts: IndexedDB-Schema
- sync.ts: Offline-Sync-Logik
- supermarkets.ts: Supermarkt-Verwaltung

Features:
- Offline-First (IndexedDB + Sync)
- Responsive Design (TailwindCSS)
- Kategorien-Management
- Mahlzeiten-Planung
- Einkaufsliste-Verwaltung
- Supermarkt-Auswahl

Build:
- Dev: npm run dev
- Build: npm run build
- Preview: npm run preview

Docker:
- Container: grocery-web
- Port: 80
- Nginx-Config: web/nginx.conf
- Dockerfile: web/Dockerfile
                """,
                "keywords": ["frontend", "react", "typescript", "vite", "web", "ui", "offline", "pwa"],
                "category": "infrastructure",
                "project": "grocery-shopping-app",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === DEPLOYMENT ===
        {
            "id": 205,
            "vector": v,
            "payload": {
                "slug": "deployment-workflow-complete",
                "title": "Deployment-Workflow - Schritt-für-Schritt",
                "content": """
Deployment auf Synology NAS:

Voraussetzungen:
- SSH-Zugang zur NAS (admin@192.168.178.122)
- SSH-Key (~/.ssh/nas_rsa) konfiguriert
- Git auf NAS installiert
- Docker & Docker Compose installiert

Deployment-Schritte:

1. SSH-Verbindung herstellen:
   ssh admin@192.168.178.122

2. Zum Projekt navigieren:
   cd /volume1/docker/grocery-app

3. Code aktualisieren:
   git pull origin main

4. Container stoppen:
   docker-compose down

5. Neu bauen und starten:
   docker-compose up -d --build

6. Logs prüfen:
   docker-compose logs -f

7. Status überprüfen:
   docker-compose ps
   docker logs grocery-api
   docker logs grocery-web

Wichtige Docker-Commands:
- docker ps -a: Alle Container
- docker logs <container>: Container-Logs
- docker exec -it <container> bash: Shell in Container
- docker-compose restart: Neustart ohne Rebuild

Troubleshooting:
- Port belegt: docker ps | grep <port>
- Container-Fehler: docker logs <container>
- Disk Space: docker system df
- Cleanup: docker system prune -a

Rollback:
git reset --hard HEAD~1
docker-compose up -d --build

Environment Variables:
- Gespeichert in: /volume1/docker/grocery-app/.env
- Wichtig: DATABASE_URL, HA_TOKEN

Produktions-Files:
- docker-compose.prod.yml: Produktions-Konfiguration
- .env: Environment Variables (nicht in Git!)
                """,
                "keywords": ["deployment", "docker-compose", "nas", "ssh", "workflow", "git", "ci-cd"],
                "category": "deployment",
                "project": "grocery-shopping-app",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === NETZWERK ===
        {
            "id": 206,
            "vector": v,
            "payload": {
                "slug": "network-topology",
                "title": "Netzwerk-Topologie & IP-Adressen",
                "content": """
Netzwerk-Übersicht:

IP-Adressen:
- 192.168.178.122: Synology NAS
  → Home Assistant (Port 8123)
  → AppDaemon (Teil von HA)
  → SSH-Server (Port 22)
  → Docker-Host
  
- 192.168.178.123: Grocery API Server
  → API (Port 8082)
  → Web Frontend (Port 80)
  → PostgreSQL (Port 5432, intern)

- 192.168.178.1: Router (vermutlich)

Lokale Entwicklung:
- Laptop/PC: Windows 10/11
- Projekte: C:\\Users\\droms\\Desktop\\
- Synology Drive: D:\\Cooperate Design\\
- SSH-Keys: C:\\Users\\droms\\.ssh\\

Port-Mapping:

NAS (192.168.178.122):
- 22: SSH
- 8123: Home Assistant
- 6333: Qdrant (lokal auf Entwickler-PC)

API Server (192.168.178.123):
- 80: Web Frontend
- 8082: API Backend
- 5432: PostgreSQL (nur Docker-intern)

Firewall/Router:
- Keine Port-Forwarding dokumentiert
- Lokales Netzwerk (192.168.178.0/24)

DNS:
- Keine Custom-DNS dokumentiert
- Zugriff via IP-Adresse
                """,
                "keywords": ["netzwerk", "ip-adressen", "ports", "topology", "infrastructure", "192.168.178.122", "192.168.178.123"],
                "category": "infrastructure",
                "project": "general",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === DEVELOPMENT ENVIRONMENT ===
        {
            "id": 207,
            "vector": v,
            "payload": {
                "slug": "dev-environment-complete",
                "title": "Entwicklungsumgebung - Vollständige Konfiguration",
                "content": """
Entwickler-Setup:

Betriebssystem: Windows 10/11
User: droms
Home: C:\\Users\\droms\\

Installierte Tools:

Python:
- Version: 3.14.0
- Installiert via: Python.org / winget
- Virtual Environments: .venv (in Projekten)
- pip: Aktuell
- Wichtige Packages: fastapi, uvicorn, sqlalchemy, alembic, requests

Node.js:
- Version: 22.19.0
- Package Manager: npm (Standard)
- Global Packages: (nicht dokumentiert)

Docker:
- Version: 28.5.1
- Docker Desktop installiert
- WSL2 Backend (vermutlich)
- Compose: Integriert in Docker Desktop

Git:
- Version: (nicht dokumentiert)
- Default Editor: VS Code (vermutlich)
- SSH-Keys: ~/.ssh/nas_rsa

VS Code:
- Extensions: GitHub Copilot, Python, Docker, Remote-SSH
- Settings: Beast Mode 4.0 Copilot Instructions
- Terminal: Bash (Git Bash)

Qdrant:
- Lokal via Docker: http://localhost:6333
- Container: qdrant-local
- Storage: .devtools/qdrant-storage/
- Collection: project_knowledge

UV (Python Package Manager):
- Version: 0.9.7
- Installiert: ~/.local/bin/
- Aktivierung: source ~/.local/bin/env

Projekt-Struktur:
grocery-shopping-app/
├── api/              # FastAPI Backend
├── web/              # React Frontend
├── homeassistant/    # AppDaemon Scripts
├── .devtools/        # Docker Compose, Scripts
├── .github/          # Copilot Instructions
└── docs/             # Markdown-Dokumentation

Git Repository:
- Remote: https://github.com/PeteSSMMSS/grocery-shopping-app
- Branch: main
- Clone: C:\\Users\\droms\\Desktop\\Einkaufen\\
                """,
                "keywords": ["development", "dev-environment", "tools", "python", "nodejs", "docker", "git", "vscode"],
                "category": "infrastructure",
                "project": "general",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === CODE PATTERNS ===
        {
            "id": 208,
            "vector": v,
            "payload": {
                "slug": "code-patterns-all",
                "title": "Code-Patterns & Best Practices",
                "content": """
Wichtige Code-Patterns im Projekt:

1. AppDaemon Polling Pattern (File Descriptor Safe):
```python
def initialize(self):
    self.session = requests.Session()  # Session wiederverwenden!
    self.run_in(self.start_polling, 5)  # Delayed start
    
def start_polling(self, kwargs):
    self.run_every(self.fetch_data, \"now\", 60)  # 60s Intervall
    
def fetch_data(self, kwargs):
    try:
        response = self.session.get(API_URL)
        # ... Verarbeitung ...
    except Exception as e:
        self.log(f\"Error: {e}\")
```
Vorteile: Vermeidet FD-Leaks, bessere Performance

2. FastAPI + Docker Pattern:
```yaml
services:
  api:
    build: ./api
    ports:
      - \"8082:8000\"
    environment:
      - DATABASE_URL=postgresql://...
    restart: unless-stopped
    depends_on:
      - db
```

3. React Offline-First Pattern:
```typescript
// Dexie.js für IndexedDB
const db = new Dexie('GroceryDB');
db.version(1).stores({
  products: '++id, name, category',
  purchases: '++id, date, product_id'
});

// Sync-Logik
async function syncWithServer() {
  const offline = await db.purchases.where('synced').equals(0).toArray();
  // ... Upload zu Server ...
}
```

4. FastAPI Error Handling:
```python
from fastapi import HTTPException

@app.get(\"/api/purchase/history\")
async def get_history():
    try:
        # ... DB Query ...
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Best Practices:
- Environment Variables für Config
- Docker restart: unless-stopped für Prod
- Session-Wiederverwendung bei HTTP-Requests
- Offline-First für PWAs
- Type Safety mit TypeScript/Pydantic
                """,
                "keywords": ["code-patterns", "best-practices", "appdaemon", "fastapi", "react", "docker", "offline-first"],
                "category": "code-pattern",
                "project": "grocery-shopping-app",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === TROUBLESHOOTING ===
        {
            "id": 209,
            "vector": v,
            "payload": {
                "slug": "troubleshooting-complete",
                "title": "Troubleshooting-Guide - Häufige Probleme",
                "content": """
Troubleshooting-Leitfaden:

Problem: NAS nicht erreichbar
Lösung:
1. ping 192.168.178.122
2. Router/Switch prüfen
3. NAS neu starten (Synology Web UI)
4. Firewall-Regeln prüfen

Problem: SSH-Verbindung fehlschlägt
Lösung:
1. SSH-Key-Permissions: chmod 600 ~/.ssh/nas_rsa
2. SSH-Agent: eval $(ssh-agent); ssh-add ~/.ssh/nas_rsa
3. Alternative: ssh admin@192.168.178.122 -o PubkeyAuthentication=no
4. SSH-Logs auf NAS: /var/log/secure

Problem: Docker Container startet nicht
Lösung:
1. docker ps -a (Status)
2. docker logs <container> (Fehler)
3. docker-compose down && docker-compose up -d
4. Port-Konflikte: docker ps | grep <port>
5. Disk Space: docker system df

Problem: Grocery API gibt 500-Fehler
Lösung:
1. docker logs grocery-api
2. Database Connection prüfen (DATABASE_URL in .env)
3. Migrations: docker exec grocery-api alembic upgrade head
4. PostgreSQL prüfen: docker exec -it grocery-db psql -U <user>

Problem: Frontend lädt nicht
Lösung:
1. Browser-Console (F12) auf Fehler prüfen
2. API erreichbar? curl http://192.168.178.123:8082/api/purchase/history
3. CORS-Fehler? CORS-Header in FastAPI prüfen
4. Nginx-Logs: docker logs grocery-web

Problem: Home Assistant Sensor aktualisiert nicht
Lösung:
1. AppDaemon-Logs in HA UI prüfen
2. API erreichbar? curl http://192.168.178.123:8082/api/purchase/history
3. grocery_sensor.py Syntax prüfen
4. AppDaemon neu starten (HA UI → Add-ons → AppDaemon → Restart)

Problem: Git Pull schlägt fehl
Lösung:
1. git status (Lokale Änderungen?)
2. git stash (Änderungen temporär speichern)
3. git pull origin main
4. git stash pop (Änderungen zurück)

Problem: Docker Disk Space voll
Lösung:
1. docker system df
2. docker system prune -a (Alle ungenutzten Daten löschen)
3. docker volume prune (Ungenutzte Volumes)

Problem: Qdrant nicht erreichbar
Lösung:
1. docker ps | grep qdrant
2. docker logs qdrant-local
3. cd .devtools && docker-compose restart
                """,
                "keywords": ["troubleshooting", "debugging", "errors", "fixes", "problems", "solutions"],
                "category": "troubleshooting",
                "project": "grocery-shopping-app",
                "date": date,
                "author": "project-summary"
            }
        },
        
        # === CREDENTIALS SUMMARY ===
        {
            "id": 210,
            "vector": v,
            "payload": {
                "slug": "credentials-summary",
                "title": "Credentials & Zugangsdaten - Übersicht",
                "content": """
⚠️ SENSITIVE: Zugangsdaten-Übersicht

Synology NAS:
- IP: 192.168.178.122
- SSH-User: admin
- SSH-Key: ~/.ssh/nas_rsa
- Web UI: http://192.168.178.122:5000 (Standard)

Home Assistant:
- URL: http://192.168.178.122:8123
- API-Token: In .env als HA_TOKEN (nicht hier gespeichert!)
- Login: (nicht dokumentiert)

Grocery API:
- URL: http://192.168.178.123:8082
- Auth: (keine Authentifizierung dokumentiert)

PostgreSQL:
- Host: db (Docker-intern)
- Port: 5432
- User: (in docker-compose.yml)
- Password: (in docker-compose.yml)
- Database: grocery_db (vermutlich)

Git:
- Repository: https://github.com/PeteSSMMSS/grocery-shopping-app
- Auth: SSH-Key oder Personal Access Token

Qdrant:
- URL: http://localhost:6333
- Auth: Keine (lokal)

WICHTIG:
- Passwörter nie in Git committen
- .env-Datei in .gitignore
- SSH-Keys mit chmod 600 schützen
- API-Token in Environment Variables
                """,
                "keywords": ["credentials", "passwords", "logins", "security", "sensitive", "zugangsdaten", "admin"],
                "category": "infrastructure",
                "project": "general",
                "date": date,
                "author": "project-summary",
                "sensitive": True
            }
        }
    ]

def save_to_qdrant(entries):
    """Speichert Einträge in Qdrant"""
    print(f"💾 Speichere {len(entries)} Einträge in Qdrant...\n")
    
    try:
        req = urllib.request.Request(
            f"{QDRANT_URL}/collections/{COLLECTION}/points",
            data=json.dumps({"points": entries}).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            if result.get("status") == "ok":
                print(f"✅ {len(entries)} Einträge erfolgreich gespeichert!")
                return True
            else:
                print(f"⚠️ Fehler: {result}")
                return False
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")
        return False

def main():
    print("=" * 60)
    print("  Grocery Shopping App - Projekt-Zusammenfassung")
    print("  Detaillierte Dokumentation für Qdrant")
    print("=" * 60)
    print()
    
    # Test Qdrant connection
    try:
        with urllib.request.urlopen(f"{QDRANT_URL}/collections") as r:
            print("✓ Qdrant erreichbar\n")
    except:
        print("❌ Qdrant nicht erreichbar!")
        print("   Starte: cd .devtools && docker-compose up -d")
        return 1
    
    # Get entries
    entries = get_project_summary_entries()
    print(f"📊 {len(entries)} detaillierte Einträge vorbereitet:")
    print("   - Projekt-Übersicht")
    print("   - NAS Infrastructure")
    print("   - Home Assistant Setup")
    print("   - Grocery API")
    print("   - Frontend-Architektur")
    print("   - Deployment-Workflow")
    print("   - Netzwerk-Topologie")
    print("   - Dev-Environment")
    print("   - Code-Patterns")
    print("   - Troubleshooting")
    print("   - Credentials (⚠️ Sensitive)")
    print()
    
    # Save
    if save_to_qdrant(entries):
        print()
        print("🎯 Nächste Schritte:")
        print("   1. Dashboard: http://localhost:6333/dashboard")
        print("   2. Test: '@workspace Durchsuche Qdrant nach NAS SSH-Zugangsdaten'")
        print("   3. Test: '@workspace Welche IP hat die Grocery API?'")
        print("   4. Test: '@workspace Zeige mir den Deployment-Workflow'")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())
