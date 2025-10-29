# 🚀 Deployment Workflow - Einkaufslisten App
## Windows Development → GitHub → Synology NAS Production

Diese Anleitung beschreibt den kompletten Workflow für die Einkaufslisten-App, die lokal auf Windows entwickelt und auf der Synology NAS deployed wird.

---

## 📋 Übersicht

```
┌─────────────────┐      ┌─────────────┐      ┌──────────────────┐
│  Windows Dev    │ ───► │   GitHub    │ ───► │  Synology NAS    │
│  (Development)  │ git  │  (Version)  │ pull │  (Production)    │
└─────────────────┘      └─────────────┘      └──────────────────┘
```

**Workflow:**
1. Development & Testing auf Windows
2. Git Commit & Push zu GitHub
3. Git Pull auf NAS + Container Restart
4. Verifizierung auf NAS

---

## 🖥️ System-Informationen

### Windows Development PC
- **Pfad:** `C:\Users\droms\Desktop\Einkaufen`
- **Shell:** `bash.exe` (Git Bash)
- **Docker Compose:** `docker compose` (mit Leerzeichen)
- **Compose File:** `docker-compose.yml`
- **Container Names:** `groceries-api`, `groceries-web`

### Synology NAS (Production)
- **IP-Adresse:** `192.168.178.123`
- **SSH User:** `Pierre`
- **Pfad:** `/volume1/docker/einkaufen`
- **Docker Compose:** `/usr/local/bin/docker-compose` (mit Bindestrich!)
- **Compose File:** `docker-compose.yml`

### PostgreSQL Database
- **IP-Adresse:** `192.168.178.123`
- **Port:** `5588`
- **User:** `postgres`
- **Password:** `homeassistant`
- **Database:** `groceries`
- **Connection String:** `postgresql+psycopg://postgres:homeassistant@192.168.178.123:5588/groceries`

---

## 🚀 Workflow Schritt-für-Schritt

### Phase 1: Development auf Windows

#### 1.1 Container starten
```bash
cd /c/Users/droms/Desktop/Einkaufen
docker compose up -d
```

**Services werden gestartet:**
- `groceries-api` - Backend API (Port 8080)
- `groceries-web` - Frontend (Port 5173)

#### 1.2 Logs überwachen
```bash
# Alle Logs
docker compose logs -f

# Nur API
docker compose logs -f api

# Nur Web
docker compose logs -f web

# Letzte 100 Zeilen
docker compose logs --tail=100
```

#### 1.3 App testen
- **Frontend:** http://localhost:5173
- **Backend API Docs:** http://localhost:8080/docs
- **Backend Health:** http://localhost:8080/health

**Testing Checkliste:**
- [ ] Frontend lädt ohne Fehler
- [ ] Kategorien und Produkte anzeigen
- [ ] Produkte zur Liste hinzufügen
- [ ] Menge ändern, Checkbox funktioniert
- [ ] Produkt von Liste entfernen
- [ ] Einstellungsmodal öffnen
- [ ] Neues Produkt erstellen
- [ ] Preis ändern
- [ ] Checkout funktioniert
- [ ] Keine Fehler in Browser Console
- [ ] Keine Fehler in API Logs

#### 1.4 Container neu starten (nach Code-Änderungen)
```bash
# Nur einzelnen Service
docker compose restart api
docker compose restart web

# Beide Services
docker compose restart

# Neu bauen (nach Dependency-Änderungen)
docker compose up -d --build
```

#### 1.5 Container stoppen
```bash
docker compose down
```

---

### Phase 2: Git Commit & Push

#### 2.1 Status prüfen
```bash
cd /c/Users/droms/Desktop/Einkaufen
git status
```

#### 2.2 Änderungen hinzufügen
```bash
# Einzelne Dateien
git add api/app/routers/products.py
git add web/src/components/ListPane.tsx

# Alle Backend-Änderungen
git add api/

# Alle Frontend-Änderungen
git add web/

# Alle Änderungen
git add .
```

#### 2.3 Commit mit aussagekräftiger Message
```bash
git commit -m "feat: Add product search functionality

- Added search input in CatalogPane
- Filter products by name (case-insensitive)
- Added category filter buttons
- Improved UI responsiveness

Deployment ready for NAS"
```

**Commit Message Prefixes:**
- `feat:` - Neue Features (z.B. Offline-Sync, neue Komponente)
- `fix:` - Bugfixes (z.B. Preis-Berechnung korrigiert)
- `refactor:` - Code-Refactoring (z.B. API-Client umstrukturiert)
- `style:` - UI/UX Änderungen (z.B. Tailwind-Classes angepasst)
- `docs:` - Dokumentation (README, Kommentare)
- `chore:` - Maintenance (Dependencies updaten)

#### 2.4 Push zu GitHub
```bash
git push origin main
```

#### 2.5 Verifizierung
```bash
# Letzte 3 Commits anzeigen
git log --oneline -3

# Remote Status prüfen
git status
```

---

### Phase 3: Deployment auf Synology NAS

#### 3.1 Windows Container stoppen
```bash
cd /c/Users/droms/Desktop/Einkaufen
docker compose down
```

**⚠️ WICHTIG:** Container auf Windows stoppen, damit NAS Production läuft!

#### 3.2 SSH zur NAS & Pull
```bash
# Methode 1: Einzelne Commands
ssh Pierre@192.168.178.123
cd /volume1/docker/einkaufen
git pull
exit

# Methode 2: One-Liner
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && git pull"
```

#### 3.3 Container auf NAS neu starten
```bash
# Option 1: Restart (schnell, verwendet existierende Images)
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml restart"

# Option 2: Down + Up (empfohlen nach größeren Änderungen)
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml down && /usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml up -d"

# Option 3: Rebuild (nach Dependency-Änderungen)
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml up -d --build"
```

**⚠️ WICHTIG:** Auf NAS **MUSS** `/usr/local/bin/docker-compose` verwendet werden!

---

### Phase 4: Verifizierung auf NAS

#### 4.1 Logs von NAS abrufen
```bash
# Live Logs (mit Strg+C beenden)
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-api -f"
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-web -f"

# Letzte 200 Zeilen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-api --tail=200 2>&1"
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-web --tail=200 2>&1"
```

#### 4.2 Container Status prüfen
```bash
# Laufende Container anzeigen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker ps | grep groceries"

# Container Status
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && /usr/local/bin/docker-compose ps"
```

#### 4.3 App testen (auf NAS IP)

Ersetze `192.168.178.123` mit deiner NAS-IP:

- **Frontend:** http://192.168.178.123:5173
- **Backend API:** http://192.168.178.123:8080/docs
- **Health Check:** http://192.168.178.123:8080/health

**Production Testing Checkliste:**
- [ ] Frontend lädt von NAS
- [ ] Datenbank-Verbindung funktioniert
- [ ] Produkte werden angezeigt
- [ ] Einkaufsliste funktioniert
- [ ] Offline-Modus funktioniert (Flugmodus aktivieren)
- [ ] PWA installierbar auf Smartphone
- [ ] Keine Fehler in Logs

#### 4.4 Gesundheitschecks
```bash
# API Health Check
curl http://192.168.178.123:8080/health

# Web Health Check
curl http://192.168.178.123:5173/health
```

---

## 🔧 Troubleshooting

### Problem: "docker-compose: command not found" auf NAS

**Ursache:** Falscher Pfad verwendet

**Lösung:** Vollständigen Pfad nutzen: `/usr/local/bin/docker-compose`

### Problem: Container startet nicht auf NAS

**Debugging:**
```bash
# Container Status
ssh Pierre@192.168.178.123 "/usr/local/bin/docker ps -a | grep groceries"

# Logs prüfen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-api"
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-web"

# Docker Compose Status
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && /usr/local/bin/docker-compose ps"

# Container komplett neu starten
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml down"
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml up -d"
```

### Problem: Git Merge Conflicts auf NAS

**Lösung:**
```bash
# Lokale Änderungen komplett verwerfen
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && git fetch origin && git reset --hard origin/main"
```

### Problem: Datenbank-Verbindung fehlgeschlagen

**Checks:**
```bash
# PostgreSQL erreichbar?
telnet 192.168.178.123 5588

# Von NAS aus testen
ssh Pierre@192.168.178.123 "telnet 192.168.178.123 5588"

# DATABASE_URL korrekt?
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && cat .env | grep DATABASE_URL"
```

**Lösung:**
- `DATABASE_URL` in `.env` überprüfen
- PostgreSQL Port 5588 in Firewall freigeben
- PostgreSQL `pg_hba.conf` prüfen (NAS IP erlauben)

### Problem: Frontend zeigt "Network Error"

**Ursache:** Frontend kann Backend nicht erreichen

**Lösung:**
```bash
# VITE_API_BASE in .env anpassen (für Production)
VITE_API_BASE=http://192.168.178.123:8080

# Container neu bauen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml up -d --build web"
```

### Problem: Alembic Migrations schlagen fehl

**Debugging:**
```bash
# Migrations manuell ausführen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker exec -it groceries-api alembic upgrade head"

# Migrations-Status prüfen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker exec -it groceries-api alembic current"

# Migrations-History
ssh Pierre@192.168.178.123 "/usr/local/bin/docker exec -it groceries-api alembic history"
```

**Lösung bei Problemen:**
```bash
# Datenbank-Tabellen manuell erstellen (nur einmalig!)
ssh Pierre@192.168.178.123 "/usr/local/bin/docker exec -it groceries-api python -c 'from app.db import Base, engine; Base.metadata.create_all(engine)'"
```

---

## 📝 Best Practices

### 1. Immer Windows zuerst testen
- Mindestens 5 erfolgreiche Tests auf Windows
- Alle Features durchgehen
- Keine Fehler in Logs

### 2. Aussagekräftige Commit Messages
```bash
# Gut ✅
git commit -m "feat: Add offline sync with background service worker

- Dexie.js IndexedDB for local storage
- Workbox background sync for API queue
- Last Write Wins conflict resolution
- Auto-sync every 5 minutes
- Visual offline indicator

All offline features tested and working"

# Schlecht ❌
git commit -m "update"
git commit -m "fix"
```

### 3. Environment-Variablen richtig setzen

**Windows (.env):**
```env
VITE_API_BASE=http://localhost:8080
```

**NAS Production (.env):**
```env
VITE_API_BASE=http://192.168.178.123:8080
```

### 4. Regelmäßig committen
- Nach jedem funktionierenden Feature
- Nicht warten bis "alles fertig" ist
- Kleinere Commits = leichter zu debuggen

### 5. Container auf Windows stoppen nach Deployment
- Verhindert Konflikte mit NAS
- NAS ist Production Environment
- Windows nur für Development

---

## 🔄 Complete Workflow Example

### Neues Feature: "Produktkatalog Suche"

```bash
# === WINDOWS: DEVELOPMENT ===

cd /c/Users/droms/Desktop/Einkaufen

# 1. Container starten
docker compose up -d

# 2. Code schreiben
# - web/src/components/CatalogPane.tsx anpassen
# - Suchfunktion implementieren

# 3. Testen
# → http://localhost:5173 öffnen
# → Suche testen, verschiedene Queries ausprobieren

# 4. Logs prüfen
docker compose logs -f

# 5. Container stoppen
docker compose down

# === GIT: COMMIT & PUSH ===

# 6. Status prüfen
git status

# 7. Änderungen hinzufügen
git add web/src/components/CatalogPane.tsx

# 8. Commit
git commit -m "feat: Add product search in catalog

- Search input filters products by name
- Case-insensitive search
- Real-time filtering
- Improved UX

Tested successfully on Windows, ready for NAS deployment"

# 9. Push
git push origin main

# === NAS: DEPLOYMENT ===

# 10. Pull auf NAS
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && git pull"

# 11. Container restart auf NAS
ssh Pierre@192.168.178.123 "/usr/local/bin/docker-compose -f /volume1/docker/einkaufen/docker-compose.yml restart web"

# 12. Logs prüfen
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-web --tail=100 2>&1"

# === VERIFIZIERUNG ===

# 13. App auf NAS testen
# → http://192.168.178.123:5173 öffnen
# → Suche testen

# 14. Smartphone testen (PWA)
# → App auf Smartphone öffnen
# → Suche testen
# → Offline-Modus testen
```

---

## 🎯 Checkliste für neues Feature

- [ ] **Development**
  - [ ] Code geschrieben & getestet auf Windows
  - [ ] Container läuft ohne Fehler
  - [ ] Alle Features funktionieren
  - [ ] Keine Console-Errors im Browser
  - [ ] API-Responses korrekt
  - [ ] Offline-Modus funktioniert

- [ ] **Git**
  - [ ] `git status` geprüft
  - [ ] Nur relevante Dateien hinzugefügt
  - [ ] Aussagekräftige Commit Message
  - [ ] `git push` erfolgreich
  - [ ] GitHub Repo aktualisiert

- [ ] **Deployment**
  - [ ] Windows Container gestoppt
  - [ ] `git pull` auf NAS erfolgreich
  - [ ] Container auf NAS restarted
  - [ ] Logs auf NAS geprüft
  - [ ] Keine Fehler in Logs

- [ ] **Verifizierung**
  - [ ] App läuft auf NAS-IP
  - [ ] Alle Features funktionieren
  - [ ] Datenbank-Verbindung OK
  - [ ] PWA auf Smartphone funktioniert
  - [ ] Offline-Sync funktioniert
  - [ ] 24h Monitoring (keine Crashes)

---

## 📞 Wichtige URLs & Zugänge

### Windows Development
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs

### NAS Production
- **Frontend:** http://192.168.178.123:5173
- **Backend:** http://192.168.178.123:8080
- **API Docs:** http://192.168.178.123:8080/docs

### PostgreSQL
- **Host:** 192.168.178.123
- **Port:** 5588
- **Database:** groceries
- **User:** postgres

---

## 🆘 Nützliche Commands

### Docker auf Windows
```bash
# Alle Container
docker ps -a

# Container stoppen
docker stop groceries-api groceries-web

# Container entfernen
docker rm groceries-api groceries-web

# Images entfernen
docker rmi einkaufen-api einkaufen-web

# Volumes anzeigen
docker volume ls

# Logs
docker logs groceries-api -f
```

### Docker auf NAS
```bash
# Container Status
ssh Pierre@192.168.178.123 "/usr/local/bin/docker ps"

# Logs
ssh Pierre@192.168.178.123 "/usr/local/bin/docker logs groceries-api --tail=200"

# Container restart
ssh Pierre@192.168.178.123 "/usr/local/bin/docker restart groceries-api"

# Shell in Container
ssh Pierre@192.168.178.123 "/usr/local/bin/docker exec -it groceries-api /bin/sh"
```

### Git Nützliches
```bash
# Letzten Commit rückgängig (Files bleiben)
git reset --soft HEAD~1

# Letzten Commit komplett löschen
git reset --hard HEAD~1

# Änderungen verwerfen
git checkout -- <file>

# Commit Message ändern
git commit --amend -m "Neue Message"

# Remote Status
git fetch && git status

# Branches
git branch -a
```

---

**Erstellt:** 29. Oktober 2025  
**Letzte Aktualisierung:** 29. Oktober 2025  
**Version:** 1.0
