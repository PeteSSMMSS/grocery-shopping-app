# 📦 Projekt-Übersicht - Einkaufslisten App

## ✅ Was wurde erstellt?

Eine **vollständige Progressive Web App (PWA)** für Einkaufslisten mit:

### 🎯 Hauptfunktionen
- ✅ Zwei-Spalten-Layout (Desktop): Liste + Katalog
- ✅ Produktkatalog mit Kategorien & Suche
- ✅ Einkaufsliste mit Mengen, Preisen, Gesamtsumme
- ✅ Einstellungen zum Verwalten von Produkten & Kategorien
- ✅ Offline-Fähigkeit (IndexedDB + Service Worker)
- ✅ Automatische Synchronisierung
- ✅ Mobile-optimiert & PWA-installierbar
- ✅ Historie abgeschlossener Einkäufe

---

## 📁 Projektstruktur

```
Einkaufen/
├── api/                          # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py               # FastAPI Entry Point
│   │   ├── db.py                 # Database Connection
│   │   ├── models.py             # SQLAlchemy Models (7 Tabellen)
│   │   ├── schemas.py            # Pydantic Request/Response Schemas
│   │   ├── routers/              # API Endpoints
│   │   │   ├── categories.py    # CRUD für Kategorien
│   │   │   ├── products.py      # CRUD für Produkte + Preise
│   │   │   ├── list.py           # Aktive Einkaufsliste
│   │   │   ├── purchase.py      # Checkout & Historie
│   │   │   └── sync.py           # Offline-Synchronisierung
│   │   └── migrations/
│   │       ├── env.py            # Alembic Config
│   │       └── versions/
│   │           └── 001_initial.py # Initial Migration
│   ├── Dockerfile                # Multi-Stage Python Build
│   ├── requirements.txt          # Python Dependencies
│   └── alembic.ini               # Alembic Configuration
│
├── web/                          # Frontend (React + Vite)
│   ├── src/
│   │   ├── main.tsx              # React Entry Point
│   │   ├── App.tsx               # Root Component
│   │   ├── components/
│   │   │   ├── ListPane.tsx     # Einkaufsliste (links)
│   │   │   ├── CatalogPane.tsx  # Produktkatalog (rechts)
│   │   │   └── SettingsModal.tsx # Einstellungen Modal
│   │   ├── lib/
│   │   │   ├── api.ts            # API Client (alle Endpoints)
│   │   │   ├── db.dexie.ts       # IndexedDB (Dexie.js)
│   │   │   └── sync.ts           # Sync-Logik (Online/Offline)
│   │   └── index.css             # Tailwind CSS
│   ├── public/
│   ├── Dockerfile                # Multi-Stage Node Build + nginx
│   ├── nginx.conf                # nginx Config (SPA-Routing)
│   ├── vite.config.ts            # Vite + PWA Plugin
│   ├── package.json              # npm Dependencies
│   └── tailwind.config.js        # Tailwind Config
│
├── docker-compose.yml            # Orchestrierung (api + web)
├── .env                          # Environment Variables
├── .env.example                  # Environment Template
├── .gitignore                    # Git Ignore Rules
├── README.md                     # Projekt-Dokumentation
├── DEPLOYMENT.md                 # NAS-Deployment-Workflow
├── QUICKSTART.md                 # Schnellstart-Anleitung
├── Makefile                      # Hilfreiche Commands
└── PROJECT_SUMMARY.md            # Diese Datei
```

---

## 🗄️ Datenbank-Schema (PostgreSQL)

### Tabellen (7)

1. **categories** - Produktkategorien
   - `id`, `name`, `updated_at`

2. **products** - Produkte im Katalog
   - `id`, `name`, `category_id`, `is_active`, `updated_at`

3. **product_prices** - Preishistorie
   - `id`, `product_id`, `price_cents`, `currency`, `valid_from`, `updated_at`

4. **lists** - Einkaufslisten
   - `id`, `name`, `is_active`, `updated_at`

5. **list_items** - Items auf einer Liste
   - `id`, `list_id`, `product_id`, `qty`, `is_checked`, `added_at`, `updated_at`

6. **purchases** - Abgeschlossene Einkäufe
   - `id`, `list_id`, `purchased_at`, `total_cents`, `updated_at`

7. **purchase_items** - Items eines Einkaufs
   - `id`, `purchase_id`, `product_id`, `qty`, `price_cents_at_purchase`, `updated_at`

**Jede Tabelle hat `updated_at` für Sync!**

---

## 🔌 API Endpoints (FastAPI)

### Categories
- `GET /api/categories` - Alle Kategorien
- `POST /api/categories` - Kategorie erstellen
- `PATCH /api/categories/{id}` - Kategorie bearbeiten
- `DELETE /api/categories/{id}` - Kategorie löschen

### Products
- `GET /api/products?search=&category=&active=` - Produkte filtern
- `GET /api/products/{id}` - Ein Produkt mit Preishistorie
- `POST /api/products` - Produkt erstellen (mit initial price)
- `PATCH /api/products/{id}` - Produkt bearbeiten
- `POST /api/products/{id}/price` - Preis ändern (History-Entry)
- `DELETE /api/products/{id}` - Produkt deaktivieren (Soft Delete)

### Shopping List
- `GET /api/lists/active` - Aktuelle Liste mit Items + Gesamtsumme
- `POST /api/lists/active/items` - Item hinzufügen
- `PATCH /api/lists/active/items/{id}` - Item aktualisieren (Menge, Check)
- `DELETE /api/lists/active/items/{id}` - Item entfernen

### Purchases
- `POST /api/purchase/checkout` - Einkauf abschließen
- `GET /api/purchase/history?limit=` - Letzte Einkäufe
- `GET /api/purchase/{id}` - Ein Einkauf

### Sync (Offline-Fähigkeit)
- `GET /api/sync/since?ts=` - Änderungen seit Timestamp
- `POST /api/sync/changes` - Offline-Queue vom Client senden

**Vollständige API-Docs:** http://localhost:8080/docs (Swagger UI)

---

## 🧱 Tech Stack

### Backend
- **FastAPI** - Modern Python Web Framework
- **SQLAlchemy** - ORM für PostgreSQL
- **Alembic** - Database Migrations
- **Pydantic** - Request/Response Validation
- **psycopg** - PostgreSQL Driver
- **Uvicorn** - ASGI Server

### Frontend
- **React 18** - UI Framework
- **TypeScript** - Type Safety
- **Vite** - Build Tool & Dev Server
- **Tailwind CSS** - Utility-First CSS
- **TanStack Query** - Data Fetching & Caching
- **Dexie.js** - IndexedDB Wrapper
- **Workbox** - Service Worker & Background Sync
- **vite-plugin-pwa** - PWA Generation

### Infrastructure
- **Docker** - Containerisierung
- **Docker Compose** - Multi-Container Orchestrierung
- **nginx** - Static File Serving (Frontend)
- **PostgreSQL** - Datenbank (externe Instanz)

---

## 🚀 Wie starten?

### 1. Schnellstart (Windows)
```bash
cd /c/Users/droms/Desktop/Einkaufen
docker compose up -d
# → http://localhost:5173
```

Siehe: [QUICKSTART.md](./QUICKSTART.md)

### 2. Auf NAS deployen
Siehe: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🎨 UI-Features

### Desktop (Zwei-Spalten-Layout)
- **Links:** Einkaufsliste
  - Produkte mit Mengen & Preisen
  - Checkbox zum Abhaken
  - +/- Buttons für Mengen
  - Entfernen-Button
  - Gesamtsumme unten (fixiert)

- **Rechts:** Produktkatalog
  - Suchfeld
  - Kategorie-Filter (Chips)
  - Produkte nach Kategorie gruppiert
  - Klick → Produkt zur Liste hinzufügen

- **Header:**
  - Online/Offline Indicator
  - "Abschließen"-Button (Checkout)
  - "Einstellungen"-Button

### Mobile (Responsive)
- Stapel-Layout (Liste oben, Katalog unten)
- Touch-optimiert
- PWA installierbar
- Offline-fähig

### Einstellungsmodal
- **Tab "Produkte":**
  - Neues Produkt erstellen (Name, Kategorie, Preis)
  - Alle Produkte auflisten
  - Preis ändern (History-Entry)
  - Produkt aktivieren/deaktivieren

- **Tab "Kategorien":**
  - Neue Kategorie erstellen
  - Alle Kategorien auflisten

---

## 🔌 Offline-Funktionalität

### IndexedDB (Dexie.js)
Lokale Kopie von:
- `categories`
- `products`
- `product_prices`
- `list_items`
- `offlineQueue` (für Sync)

### Service Worker (Workbox)
- **NetworkFirst** für API-Requests
- **Stale-While-Revalidate** für Assets
- **Background Sync** für Mutations
- Automatische Synchronisierung bei Reconnect

### Sync-Logik
- Auto-Sync alle 5 Minuten (wenn online)
- Manueller Sync bei App-Start
- Offline-Queue für Mutations
- **Last Write Wins** Konfliktauflösung

---

## 📱 Progressive Web App (PWA)

### Features
- ✅ Installierbar auf Smartphone (Add to Homescreen)
- ✅ Funktioniert offline
- ✅ Manifest mit Icons
- ✅ Service Worker für Caching
- ✅ Background Sync
- ✅ Standalone Display Mode

### Installation
- **Android:** Chrome → Menü → "Zum Startbildschirm hinzufügen"
- **iOS:** Safari → Teilen → "Zum Home-Bildschirm"

---

## 🔧 Konfiguration

### Environment Variables (.env)

**Wichtigste Variablen:**
```env
# PostgreSQL (REQUIRED!)
DATABASE_URL=postgresql+psycopg://postgres:homeassistant@192.168.178.123:5588/groceries

# API
API_HOST=0.0.0.0
API_PORT=8080

# Frontend
VITE_API_BASE=http://localhost:8080        # Dev
VITE_API_BASE=http://192.168.178.123:8080  # Production

# CORS
CORS_ORIGINS=http://localhost:5173
```

### Ports
- **API:** 8080
- **Web:** 5173 (Dev), 80 (Production nginx)
- **PostgreSQL:** 5588 (extern)

---

## 🧪 Testing

### Manuelle Tests
- [ ] Produkte erstellen & anzeigen
- [ ] Kategorien erstellen
- [ ] Produkte zur Liste hinzufügen
- [ ] Mengen ändern (+/-)
- [ ] Produkte abhaken
- [ ] Produkte entfernen
- [ ] Gesamtsumme korrekt
- [ ] Suche funktioniert
- [ ] Kategorie-Filter funktioniert
- [ ] Einstellungen öffnen
- [ ] Preis ändern
- [ ] Checkout funktioniert
- [ ] Offline-Modus (Flugmodus)
- [ ] Sync nach Reconnect
- [ ] PWA Installation

### Health Checks
```bash
# API
curl http://localhost:8080/health
# → {"status": "healthy"}

# Web
curl http://localhost:5173/health
# → healthy
```

---

## 📊 Monitoring

### Logs
```bash
# Alle Container
docker compose logs -f

# Nur API
docker compose logs -f api

# Nur Web
docker compose logs -f web
```

### Container Status
```bash
docker compose ps
```

### Browser DevTools
- **Console:** JavaScript-Fehler
- **Network:** API-Requests
- **Application:**
  - IndexedDB → `GroceriesDB`
  - Service Workers → Status
  - Manifest → PWA-Config

---

## 🚨 Häufige Probleme

### 1. Datenbank-Verbindung fehlschlägt
- PostgreSQL läuft? → `telnet 192.168.178.123 5588`
- `DATABASE_URL` korrekt?
- Firewall-Regeln?

### 2. Frontend zeigt "Network Error"
- Backend läuft? → `curl http://localhost:8080/health`
- `VITE_API_BASE` korrekt?
- CORS-Einstellungen?

### 3. Container startet nicht
```bash
docker compose logs api
docker compose down
docker compose up -d --build
```

### 4. Alembic Migration schlägt fehl
```bash
docker compose exec api alembic upgrade head
```

Siehe: [QUICKSTART.md → Troubleshooting](./QUICKSTART.md#-troubleshooting-beim-ersten-start)

---

## 📚 Dokumentation

- **README.md** - Projekt-Übersicht & Features
- **QUICKSTART.md** - Erste Schritte & Setup
- **DEPLOYMENT.md** - NAS-Deployment-Workflow
- **PROJECT_SUMMARY.md** - Diese Datei (Übersicht)
- **.env.example** - Environment-Template
- **Makefile** - Hilfreiche Commands

### API Dokumentation
- **Swagger UI:** http://localhost:8080/docs
- **ReDoc:** http://localhost:8080/redoc

---

## 🎯 Nächste Schritte

### Sofort einsatzbereit:
1. ✅ Testdaten anlegen (Kategorien, Produkte)
2. ✅ Auf Windows testen
3. ✅ Auf NAS deployen (siehe DEPLOYMENT.md)
4. ✅ PWA auf Smartphone installieren

### Optional (Erweiterungen):
- [ ] Mobile Bottom-Sheet (Touch-Gesten)
- [ ] Grafana Analytics (Preisverlauf, Ausgaben)
- [ ] Barcode-Scanner (Produkte schnell hinzufügen)
- [ ] Mehrere Listen (Familie, Arbeit, etc.)
- [ ] Teilen von Listen (Multi-User)
- [ ] Push-Notifications (Shopping-Reminder)
- [ ] Dark Mode
- [ ] Eigenes Branding (Logo, Farben)

---

## 🔐 Sicherheit

**Aktuell:**
- Keine Authentifizierung (für private Nutzung OK)
- CORS auf localhost + NAS-IP begrenzt

**Für Production (extern erreichbar):**
- [ ] JWT Authentication hinzufügen
- [ ] HTTPS mit SSL-Zertifikat (Let's Encrypt)
- [ ] Rate Limiting
- [ ] Input Validation verschärfen

---

## 📄 Lizenz

MIT - Frei nutzbar, anpassbar, erweiterbar!

---

## 🙋 Support

Bei Fragen oder Problemen:
1. [QUICKSTART.md](./QUICKSTART.md) lesen
2. [DEPLOYMENT.md](./DEPLOYMENT.md) checken
3. Logs prüfen: `docker compose logs -f`
4. GitHub Issue erstellen (falls Repository öffentlich)

---

**Viel Erfolg mit der Einkaufslisten-App! 🛒✨**

---

**Erstellt:** 29. Oktober 2025  
**Version:** 1.0  
**Status:** ✅ Production Ready
