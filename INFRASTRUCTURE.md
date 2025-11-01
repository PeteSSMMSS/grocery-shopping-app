# Infrastructure Wissensdatenbank

Dieses Dokument dient als zentrale Wissensdatenbank für projektübergreifende Informationen.
GitHub Copilot kann diese Datei automatisch durchsuchen und relevante Informationen finden.

## NAS (Synology)

**IP-Adresse:** 192.168.178.122

**SSH-Zugang:**
- Benutzer: `admin`
- Port: `22`
- SSH-Key: `~/.ssh/nas_rsa`

**Docker:**
- Container-Pfad: `/volume1/docker`
- Alle Docker-Container liegen unter diesem Pfad
- Zugriff via SSH: `ssh admin@192.168.178.122`

**AppDaemon:**
- Config-Pfad: `\\192.168.178.122\addon_configs\a0d7b954_appdaemon`
- Apps-Ordner: `\\192.168.178.122\addon_configs\a0d7b954_appdaemon\apps`
- Grocery Sensor Script: `grocery_sensor.py`

**Synology Drive:**
- Sync-Ordner (lokal): `D:\Cooperate Design`
- Automatische Synchronisierung aktiv
- Backup-Ziel für wichtige Daten

---

## Home Assistant

**URL:** http://192.168.178.122:8123

**API:**
- API-Token gespeichert in `.env` als `HA_TOKEN`
- Integration mit AppDaemon aktiv

**Sensoren:**
- `sensor.last_grocery_purchase` - Letzter Einkauf (aktualisiert alle 60s)

---

## Grocery Shopping App

**API Base URL:** http://192.168.178.123:8082

**Haupt-Endpoints:**
- `/api/purchase/history` - Einkaufshistorie
- `/api/products` - Produktliste
- `/api/categories` - Kategorien

**Technologie-Stack:**
- Backend: FastAPI (Python)
- Frontend: React + TypeScript + Vite
- Datenbank: PostgreSQL
- Deployment: Docker Compose

**Docker-Container:**
- API: Port 8082
- Web: Port 80
- Datenbank: Port 5432 (intern)

---

## Entwicklungsumgebung

**Python:**
- Version: 3.14.0
- Virtual Environments: Im Projekt-Ordner als `.venv`

**Node.js:**
- Version: 22.19.0
- Package Manager: npm

**Docker:**
- Version: 28.5.1
- Docker Desktop installiert

**Git:**
- Repository: `grocery-shopping-app`
- Owner: PeteSSMMSS
- Branch: `main`

---

## Netzwerk-Übersicht

```
192.168.178.122  → Synology NAS (SSH, Docker, Home Assistant)
192.168.178.123  → Grocery API Server
```

---

## Wichtige Pfade

**Windows (lokal):**
- Projekte: `C:\Users\droms\Desktop\`
- Synology Drive: `D:\Cooperate Design\`
- SSH-Keys: `~/.ssh/`

**NAS (Synology):**
- Docker: `/volume1/docker/`
- AppDaemon: `/volume1/docker/appdaemon/`
- Backups: `/volume1/backups/`

---

## Code-Patterns & Best Practices

### AppDaemon Polling Pattern
```python
def initialize(self):
    self.session = requests.Session()
    self.run_in(self.start_polling, 5)  # Delayed start
    
def start_polling(self, kwargs):
    self.run_every(self.fetch_data, "now", 60)  # 60s interval
```

### Docker Compose auf NAS deployen
```bash
ssh admin@192.168.178.122
cd /volume1/docker/<service>
docker-compose up -d
```

### FastAPI + Docker Pattern
```yaml
services:
  api:
    build: ./api
    ports:
      - "8082:8000"
    environment:
      - DATABASE_URL=postgresql://...
    restart: unless-stopped
```

---

## Troubleshooting

**NAS nicht erreichbar:**
- Ping: `ping 192.168.178.122`
- SSH-Test: `ssh admin@192.168.178.122`

**Docker-Container starten nicht:**
```bash
docker ps -a  # Zeige alle Container
docker logs <container>  # Zeige Logs
docker-compose down && docker-compose up -d  # Neustart
```

**AppDaemon Sensor aktualisiert nicht:**
- Logs prüfen: AppDaemon-Log in Home Assistant
- Polling-Intervall: 60 Sekunden
- API erreichbar testen: `curl http://192.168.178.123:8082/api/purchase/history`
