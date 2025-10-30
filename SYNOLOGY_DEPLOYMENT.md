# 🚀 Deployment auf Synology NAS

## 📋 Voraussetzungen

- ✅ Synology NAS mit Docker installiert
- ✅ PostgreSQL Datenbank läuft bereits (192.168.178.123:5588)
- ✅ SSH-Zugriff auf die NAS
- ✅ Git auf der NAS installiert

---

## 🔧 Installation

### **1. Repository auf NAS klonen**

```bash
# SSH zur NAS verbinden
ssh dein-user@192.168.178.XXX

# Ins Docker-Verzeichnis wechseln (oder dein bevorzugter Ort)
cd /volume1/docker

# Repository klonen
git clone https://github.com/PeteSSMMSS/grocery-shopping-app.git
cd grocery-shopping-app
```

### **2. Environment-Variablen konfigurieren**

```bash
# .env Datei erstellen
cp .env.example .env

# .env bearbeiten (mit vim oder nano)
nano .env
```

**Wichtig! Anpassen:**
- `VITE_API_BASE` → Deine NAS IP (z.B. `http://192.168.178.123:8080`)
- `CORS_ORIGINS` → Deine NAS IP + Port (z.B. `http://192.168.178.123:5173`)

### **3. Docker Container starten**

```bash
# Production Build starten
docker compose -f docker-compose.prod.yml up -d --build

# Logs verfolgen
docker compose -f docker-compose.prod.yml logs -f
```

### **4. Zugriff testen**

Öffne im Browser:
```
http://192.168.178.123:5173
```

---

## 🔄 Updates deployen

### **Automatisch mit Git:**

```bash
# SSH zur NAS
ssh dein-user@192.168.178.XXX
cd /volume1/docker/grocery-shopping-app

# Neueste Version ziehen
git pull

# Container neu bauen und starten
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 📊 Container verwalten

### **Status prüfen:**
```bash
docker compose -f docker-compose.prod.yml ps
```

### **Logs ansehen:**
```bash
# Alle Logs
docker compose -f docker-compose.prod.yml logs -f

# Nur API
docker compose -f docker-compose.prod.yml logs -f api

# Nur Frontend
docker compose -f docker-compose.prod.yml logs -f web
```

### **Container stoppen:**
```bash
docker compose -f docker-compose.prod.yml down
```

### **Container neu starten:**
```bash
docker compose -f docker-compose.prod.yml restart
```

---

## 🌐 Reverse Proxy Setup (Optional)

Falls du einen Reverse Proxy wie Nginx oder Traefik nutzt:

### **Nginx Config Beispiel:**

```nginx
server {
    listen 80;
    server_name einkaufen.local;

    location / {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 🔒 Sicherheit

### **Empfohlene Maßnahmen:**

1. **Firewall-Regeln:**
   - Port 8080 (API) nur intern erreichbar
   - Port 5173 (Web) nur intern oder über VPN

2. **HTTPS (falls extern erreichbar):**
   - Let's Encrypt Zertifikat
   - Reverse Proxy mit SSL

3. **Backup:**
   - Datenbank regelmäßig sichern
   - Git Repository als Backup

---

## 🐛 Troubleshooting

### **Container starten nicht:**
```bash
# Logs prüfen
docker compose -f docker-compose.prod.yml logs

# Ports prüfen (ob schon belegt)
netstat -tulpn | grep -E '8080|5173'
```

### **API nicht erreichbar:**
```bash
# Health-Check
curl http://localhost:8080/health

# Container-Status
docker compose -f docker-compose.prod.yml ps
```

### **Frontend zeigt API-Fehler:**
- Prüfe `VITE_API_BASE` in `.env`
- Prüfe `CORS_ORIGINS` in `.env`
- Prüfe ob API-Container läuft

### **Datenbank-Verbindung fehlschlägt:**
- Prüfe `DATABASE_URL` in `.env`
- Prüfe ob PostgreSQL auf 192.168.178.123:5588 erreichbar ist
- Teste Verbindung: `psql "postgresql://postgres:homeassistant@192.168.178.123:5588/groceries"`

---

## 📱 Mobile Zugriff

Die App ist automatisch responsive und funktioniert auf dem Handy!

**Zugriff im lokalen Netzwerk:**
```
http://192.168.178.123:5173
```

**Tipp:** Als Lesezeichen auf dem Homescreen speichern für schnellen Zugriff!

---

## ✅ Checkliste

- [ ] Repository auf NAS geklont
- [ ] `.env` Datei erstellt und angepasst
- [ ] Docker Container gestartet
- [ ] API Health-Check erfolgreich (`/health`)
- [ ] Frontend im Browser erreichbar
- [ ] Login funktioniert
- [ ] Datenbank-Verbindung OK

---

## 📞 Support

Bei Problemen kannst du:
1. Logs prüfen: `docker compose -f docker-compose.prod.yml logs -f`
2. Container Status: `docker compose -f docker-compose.prod.yml ps`
3. Health Check: `curl http://localhost:8080/health`
