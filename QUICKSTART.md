# 🚀 Schnellstart-Anleitung - Einkaufslisten App 2025

## ⚡ Windows: Erste Schritte

### 1. PostgreSQL-Datenbank vorbereiten

Die App nutzt eine **bestehende PostgreSQL-Datenbank**. Stelle sicher, dass diese läuft:

**Verbindungsdaten:**
- Host: `192.168.178.123`
- Port: `5588`
- User: `postgres`
- Password: `homeassistant`
- Database: `groceries` (wird automatisch erstellt, falls nicht vorhanden)

**Test der Verbindung:**
```bash
# Von Windows aus testen
telnet 192.168.178.123 5588
```

Falls die Verbindung fehlschlägt:
- PostgreSQL-Server starten
- Firewall-Regel für Port 5588 hinzufügen
- `pg_hba.conf` anpassen (IP-Adresse erlauben)

---

### 2. Repository klonen (falls noch nicht geschehen)

```bash
cd /c/Users/droms/Desktop
git clone <DEINE_REPO_URL> Einkaufen
cd Einkaufen
```

---

### 3. Environment-Variablen konfigurieren

```bash
# .env.example kopieren
cp .env.example .env

# .env anpassen (falls nötig)
# Wichtig: DATABASE_URL muss korrekt sein!
```

---

### 4. Docker Container starten

```bash
cd /c/Users/droms/Desktop/Einkaufen

# Container erstmalig bauen und starten
docker compose up -d --build

# Logs anzeigen
docker compose logs -f
```

**Was passiert beim ersten Start:**
1. **Backend Build:** Python-Image wird gebaut, Dependencies installiert
2. **Frontend Build:** Node.js-Image wird gebaut, npm install, Vite build
3. **Alembic Migration:** Datenbank-Tabellen werden automatisch erstellt
4. **API startet:** FastAPI läuft auf Port 8080
5. **Web startet:** nginx serviert Frontend auf Port 5173

**Erwartete Logs:**
```
groceries-api   | INFO:     Application startup complete.
groceries-api   | INFO:     Uvicorn running on http://0.0.0.0:8080
groceries-web   | /docker-entrypoint.sh: Configuration complete; ready for start up
```

---

### 5. Erste Schritte in der App

#### 5.1 Frontend öffnen
```bash
# Im Browser:
http://localhost:5173
```

#### 5.2 API Dokumentation öffnen
```bash
# Im Browser:
http://localhost:8080/docs
```

#### 5.3 Testdaten erstellen

**Via API Docs (http://localhost:8080/docs):**

1. **Kategorien erstellen:**
   - `POST /api/categories`
   - Body: `{"name": "Obst & Gemüse"}`
   - Weitere: Milchprodukte, Fleisch & Wurst, Getränke, Backwaren

2. **Produkte erstellen:**
   - `POST /api/products`
   - Body: `{"name": "Bananen", "category_id": 1, "price_cents": 189}`
   - Weitere Produkte hinzufügen

**Via Frontend (http://localhost:5173):**

1. Auf **⚙️ Einstellungen** klicken
2. Tab **Kategorien** → Neue Kategorien erstellen
3. Tab **Produkte** → Neue Produkte mit Preisen erstellen
4. Modal schließen
5. Rechts im Katalog: Produkte anklicken zum Hinzufügen
6. Links: Einkaufsliste mit Mengen verwalten

---

### 6. App testen

**Desktop-Features testen:**
- [x] Produkte aus Katalog anklicken
- [x] Mengen mit +/- ändern
- [x] Produkte abhaken (Checkbox)
- [x] Produkte von Liste entfernen (🗑️)
- [x] Gesamtsumme unten sehen
- [x] Suche im Katalog nutzen
- [x] Kategorien filtern
- [x] Einstellungen öffnen
- [x] Neues Produkt erstellen
- [x] Preis ändern
- [x] Einkauf abschließen (Checkout)

**Mobile-Features testen:**
- [x] Browser-Fenster auf Smartphone-Größe verkleinern
- [x] Responsive Layout prüfen
- [x] Touch-Gesten testen

**Offline-Features testen:**
- [x] Browser DevTools → Network → Offline
- [x] "Offline"-Badge erscheint
- [x] Produkte hinzufügen funktioniert
- [x] Online gehen → Sync läuft automatisch

---

## 🚨 Troubleshooting beim ersten Start

### Problem: Container starten nicht

```bash
# Container Status prüfen
docker compose ps

# Logs prüfen
docker compose logs api
docker compose logs web

# Container neu starten
docker compose down
docker compose up -d --build
```

### Problem: API zeigt Datenbank-Fehler

**Symptom in Logs:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Lösung:**
1. PostgreSQL-Server läuft?
2. Port 5588 erreichbar? → `telnet 192.168.178.123 5588`
3. `DATABASE_URL` in `.env` korrekt?
4. PostgreSQL-Firewall-Regeln prüfen
5. `pg_hba.conf`: Verbindung von deiner IP erlauben

### Problem: Frontend zeigt "Network Error"

**Ursache:** Frontend kann Backend nicht erreichen

**Lösung:**
```bash
# 1. Backend erreichbar prüfen
curl http://localhost:8080/health

# 2. Sollte zurückgeben:
# {"status": "healthy"}

# 3. Falls nicht → API Logs prüfen
docker compose logs api

# 4. CORS-Einstellungen prüfen (.env)
CORS_ORIGINS=http://localhost:5173
```

### Problem: Alembic Migration schlägt fehl

**Symptom:**
```
alembic.util.exc.CommandError: Can't locate revision identified by 'xyz'
```

**Lösung:**
```bash
# Manuell Tabellen erstellen
docker compose exec api python -c "from app.db import Base, engine; Base.metadata.create_all(engine)"

# Container neu starten
docker compose restart api
```

### Problem: Frontend-Build schlägt fehl

**Symptom:**
```
ERROR: failed to solve: process "/bin/sh -c npm run build" did not complete successfully
```

**Lösung:**
```bash
# Node-Cache löschen und neu bauen
docker compose down
docker volume prune -f
docker compose build --no-cache web
docker compose up -d
```

---

## 📱 PWA auf Smartphone installieren

### Android (Chrome)
1. http://192.168.178.123:5173 im Chrome öffnen
2. Menü (⋮) → "Zum Startbildschirm hinzufügen"
3. App-Name bestätigen → "Hinzufügen"
4. Icon auf Startbildschirm erscheint

### iOS (Safari)
1. http://192.168.178.123:5173 im Safari öffnen
2. Teilen-Button (📤) → "Zum Home-Bildschirm"
3. App-Name bestätigen → "Hinzufügen"
4. Icon auf Home-Bildschirm erscheint

**PWA-Features testen:**
- [x] App öffnen (sieht aus wie native App)
- [x] Offline-Modus: Flugmodus aktivieren
- [x] Produkte zur Liste hinzufügen (funktioniert offline!)
- [x] Flugmodus deaktivieren → Auto-Sync läuft

---

## 🎯 Nächste Schritte

### 1. Testdaten anlegen
- Mindestens 3-5 Kategorien erstellen
- Pro Kategorie 5-10 Produkte mit Preisen
- Einkaufsliste testen

### 2. Smartphone testen
- PWA installieren (siehe oben)
- Touch-Gesten testen
- Offline-Modus testen

### 3. Auf NAS deployen
- Siehe [DEPLOYMENT.md](./DEPLOYMENT.md)
- Windows Container stoppen
- Code zu GitHub pushen
- Auf NAS pullen und starten

### 4. Optional: Datenbank mit echten Preisen füllen
- Supermarkt-Bon durchgehen
- Produkte mit aktuellen Preisen anlegen
- Kategorien nach eigenen Bedürfnissen anpassen

---

## 📊 Monitoring & Debugging

### Logs in Echtzeit anzeigen
```bash
# Alle Services
docker compose logs -f

# Nur Backend
docker compose logs -f api

# Nur Frontend
docker compose logs -f web

# Letzte 100 Zeilen
docker compose logs --tail=100
```

### Container Status
```bash
# Laufende Container
docker compose ps

# Resource Usage
docker stats groceries-api groceries-web
```

### Datenbank direkt abfragen
```bash
# PostgreSQL Shell
psql -h 192.168.178.123 -p 5588 -U postgres -d groceries

# SQL Queries
SELECT * FROM categories;
SELECT * FROM products;
SELECT * FROM list_items;
```

### Browser DevTools
- **Console:** Fehler und Logs
- **Network:** API-Requests prüfen
- **Application → Storage → IndexedDB:** Offline-Daten
- **Application → Service Workers:** SW Status
- **Application → Manifest:** PWA-Config

---

## 🎉 Fertig!

Die App läuft jetzt lokal auf Windows:

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs

**Viel Spaß beim Einkaufen! 🛒**

Bei Fragen oder Problemen: siehe [DEPLOYMENT.md](./DEPLOYMENT.md) oder [README.md](./README.md)
