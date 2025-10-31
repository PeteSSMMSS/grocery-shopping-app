# 🛒 Grocery Shopping App

Eine moderne, minimalistische Einkaufslisten-Web-App mit **Offline-Unterstützung** (PWA), optimiert für den täglichen Einkauf.

<div align="center">

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-web%20%7C%20mobile-lightgrey.svg)

</div>

---

## 🌟 Highlights

- ✅ **Offline-First** - Funktioniert komplett ohne Internetverbindung im Supermarkt
- ✅ **Schnell & Snappy** - Optimiert für mobile Nutzung mit sofortiger Reaktion
- ✅ **Intelligente Synchronisation** - Automatischer Sync wenn Verbindung wiederhergestellt
- ✅ **Kalender-Ansicht** - Einkaufshistorie mit Gesamtpreisen
- ✅ **Progressive Web App** - Installierbar auf Android/iOS wie eine native App

---

## ✨ Features

### 🛍️ Einkaufsliste
- **Schnelles Hinzufügen** von Produkten aus dem Katalog
- **Mengen & Preise** werden automatisch berechnet
- **Gesamtsumme** immer im Blick
- **Checkbox-System** zum Abhaken während des Einkaufs
- **Checkout-Funktion** archiviert Einkauf im Kalender

### 📦 Produktkatalog
- **Kategorisierte Produkte** (Obst, Gemüse, Milchprodukte, etc.)
- **Suchfunktion** für schnelles Finden
- **Preishistorie** für jedes Produkt
- **Einfache Verwaltung** - Produkte hinzufügen, bearbeiten, löschen

### 📅 Einkaufshistorie
- **Kalender-Ansicht** aller vergangenen Einkäufe
- **Detaillierte Übersicht** mit allen gekauften Produkten
- **Preise zum Kaufzeitpunkt** gespeichert
- **Statistiken** über Einkaufsverhalten

### 📱 Mobile-Optimiert
- **Responsive Design** für alle Bildschirmgrößen
- **Touch-Gesten** (Tap, Long-Press)
- **Bottom-Sheet** für schnelle Aktionen
- **Fixierte Navigation** am unteren Rand
- **Keine App-Store Installation nötig** - läuft direkt im Browser

---

## 🧱 Tech Stack

### Backend
- **Python 3.11** mit **FastAPI** - Modernes, schnelles REST API Framework
- **SQLAlchemy/SQLModel** - Type-safe ORM
- **Alembic** - Database Migrations
- **PostgreSQL** - Relationale Datenbank (externe Instanz)
- **Uvicorn** - ASGI Server

### Frontend
- **React 18** mit **TypeScript** - Type-safe UI Development
- **Vite** - Blazing fast Build Tool
- **Tailwind CSS** - Utility-first CSS Framework
- **TanStack Query (React Query)** - Async State Management
- **Dexie.js** - IndexedDB Wrapper für Offline-Speicherung
- **Workbox** - Service Worker & Background Sync
- **Vite PWA Plugin** - Progressive Web App Support

### Infrastructure
- **Docker** + **Docker Compose** - Containerisierung
- **Nginx** - Static File Serving & Reverse Proxy
- **Cloudflare Tunnel** - Sicherer Zugriff von extern

---

## 🚀 Quick Start

### Voraussetzungen

- Docker & Docker Compose
- PostgreSQL Datenbank (läuft extern)
- Node.js 18+ (nur für lokale Entwicklung ohne Docker)
- Python 3.11+ (nur für lokale Entwicklung ohne Docker)

### 1. Repository klonen

```bash
git clone <repo-url>
cd Einkaufen
```

### 2. Environment-Variablen konfigurieren

```bash
cp .env.example .env
# .env bearbeiten und DATABASE_URL anpassen
```

Wichtig: `DATABASE_URL` muss auf deine PostgreSQL-Instanz zeigen:

```
DATABASE_URL=postgresql+psycopg://postgres:homeassistant@192.168.178.123:5588/groceries
```

### 3. Docker Container starten

```bash
docker compose up -d
```

Die App ist dann verfügbar unter:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs

### 4. Datenbank initialisieren

Beim ersten Start werden automatisch die Migrations ausgeführt und Tabellen erstellt.

## 📁 Projektstruktur

```
Einkaufen/
├── api/                      # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py           # FastAPI Entry Point
│   │   ├── db.py             # Database Connection
│   │   ├── models.py         # SQLAlchemy Models
│   │   ├── schemas.py        # Pydantic Schemas
│   │   ├── routers/          # API Endpoints
│   │   │   ├── products.py
│   │   │   ├── categories.py
│   │   │   ├── list.py
│   │   │   ├── prices.py
│   │   │   ├── sync.py
│   │   │   └── purchase.py
│   │   └── migrations/       # Alembic Migrations
│   ├── Dockerfile
│   └── requirements.txt
│
├── web/                      # Frontend (React + Vite)
│   ├── src/
│   │   ├── main.tsx          # React Entry Point
│   │   ├── App.tsx           # Root Component
│   │   ├── components/       # React Components
│   │   │   ├── ListPane.tsx
│   │   │   ├── CatalogPane.tsx
│   │   │   ├── SettingsModal.tsx
│   │   │   └── TotalBar.tsx
│   │   └── lib/              # Utilities
│   │       ├── api.ts        # API Client
│   │       ├── db.dexie.ts   # IndexedDB (Dexie)
│   │       ├── sync.ts       # Offline Sync Logic
│   │       └── pwa.ts        # PWA Utilities
│   ├── public/
│   │   └── manifest.webmanifest
│   ├── service-worker.ts     # Workbox Service Worker
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

## 💾 Datenmodell

### Tabellen

- **`categories`** - Produktkategorien (z.B. Obst, Gemüse, Milchprodukte)
- **`products`** - Alle Produkte mit Namen und Kategorie
- **`product_prices`** - Preishistorie pro Produkt
- **`lists`** - Einkaufslisten (Standard: "Einkauf")
- **`list_items`** - Items auf einer Liste mit Menge
- **`purchases`** - Abgeschlossene Einkäufe (Historie)
- **`purchase_items`** - Items eines abgeschlossenen Einkaufs

Jede Tabelle hat ein `updated_at` Feld für Synchronisierung.

## 🔌 API Endpoints

### Products
- `GET /api/products?search=&category=&active=1` - Produkte suchen/filtern
- `POST /api/products` - Neues Produkt anlegen
- `PATCH /api/products/{id}` - Produkt bearbeiten
- `POST /api/products/{id}/price` - Preis ändern

### Categories
- `GET /api/categories` - Alle Kategorien

### List (aktuelle Einkaufsliste)
- `GET /api/lists/active` - Aktuelle Liste mit Items
- `POST /api/lists/active/items` - Item zur Liste hinzufügen
- `PATCH /api/lists/active/items/{id}` - Item aktualisieren (Menge, Check)
- `DELETE /api/lists/active/items/{id}` - Item von Liste entfernen

### Purchases
- `POST /api/purchase/checkout` - Einkauf abschließen (speichert Historie)

### Sync (für Offline-Fähigkeit)
- `GET /api/sync/since?ts=<iso8601>` - Änderungen seit Zeitpunkt X
- `POST /api/sync/changes` - Offline-Queue vom Client senden

Vollständige API-Dokumentation: http://localhost:8080/docs (Swagger UI)

## 🛠️ Entwicklung

### Lokale Entwicklung (ohne Docker)

#### Backend

```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Migrations ausführen
alembic upgrade head

# Server starten
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

#### Frontend

```bash
cd web
npm install
npm run dev  # Startet auf http://localhost:5173
```

### Datenbank Migrations

Neue Migration erstellen:

```bash
cd api
alembic revision --autogenerate -m "Beschreibung"
alembic upgrade head
```

### Testing

```bash
# Backend Tests (wenn implementiert)
cd api
pytest

# Frontend Tests (wenn implementiert)
cd web
npm test
```

## 📱 PWA Installation

Die App kann auf dem Smartphone als PWA installiert werden:

1. Im Browser öffnen (Chrome/Edge/Safari)
2. "Zum Startbildschirm hinzufügen" wählen
3. App funktioniert dann auch offline!

## 🔄 Deployment

Siehe [DEPLOYMENT.md](./DEPLOYMENT.md) für vollständige Anleitung zum Deployment auf Synology NAS.

**Quick Deployment:**

```bash
# 1. Auf Windows: Code committen
git add .
git commit -m "feat: Feature-Beschreibung"
git push origin main

# 2. Auf NAS: Pull & Restart
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && git pull"
ssh Pierre@192.168.178.123 "cd /volume1/docker/einkaufen && docker compose down && docker compose up -d"
```

## 🐛 Troubleshooting

### Container startet nicht

```bash
# Logs prüfen
docker compose logs api
docker compose logs web

# Container neu starten
docker compose restart
```

### Datenbank-Verbindung fehlgeschlagen

- `DATABASE_URL` in `.env` überprüfen
- PostgreSQL Server erreichbar? `telnet 192.168.178.123 5588`
- Firewall-Regeln prüfen

### Frontend zeigt "Network Error"

- Backend läuft? → http://localhost:8080/health
- `VITE_API_BASE` in `.env` korrekt?
- CORS-Einstellungen in Backend prüfen

### Offline-Sync funktioniert nicht

- Service Worker registriert? → Chrome DevTools → Application → Service Workers
- IndexedDB vorhanden? → Chrome DevTools → Application → Storage → IndexedDB
- Background Sync aktiviert? → Chrome DevTools → Application → Background Services

## 📄 Lizenz

MIT

## 🙋 Support

Bei Fragen oder Problemen bitte ein GitHub Issue erstellen.
