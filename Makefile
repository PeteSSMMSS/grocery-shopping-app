# Makefile für die Einkaufslisten App
# Vereinfacht häufig genutzte Docker-Commands

.PHONY: help up down restart logs build clean test

help:
	@echo "🛒 Einkaufslisten App - Verfügbare Commands:"
	@echo ""
	@echo "  make up          - Container starten"
	@echo "  make down        - Container stoppen"
	@echo "  make restart     - Container neu starten"
	@echo "  make build       - Container neu bauen"
	@echo "  make logs        - Logs anzeigen"
	@echo "  make logs-api    - API Logs anzeigen"
	@echo "  make logs-web    - Web Logs anzeigen"
	@echo "  make clean       - Alles aufräumen (Container, Volumes, Images)"
	@echo "  make test        - Health Checks ausführen"
	@echo "  make shell-api   - Shell in API-Container"
	@echo ""

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

build:
	docker compose up -d --build

logs:
	docker compose logs -f

logs-api:
	docker compose logs -f api

logs-web:
	docker compose logs -f web

clean:
	docker compose down -v
	docker system prune -af

test:
	@echo "Testing API health..."
	@curl -f http://localhost:8080/health || echo "❌ API nicht erreichbar"
	@echo "\nTesting Web health..."
	@curl -f http://localhost:5173/health || echo "❌ Web nicht erreichbar"

shell-api:
	docker compose exec api /bin/sh

shell-web:
	docker compose exec web /bin/sh
