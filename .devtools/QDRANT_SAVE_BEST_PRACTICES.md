# Qdrant Speicher-Best Practices

## 🎯 Optimiert für GitHub Copilot MCP

Diese Best Practices stellen sicher, dass Copilot deine gespeicherten Informationen **schnell und zuverlässig** findet.

---

## ✅ Checkliste für neue Einträge

### 1. **Keywords (WICHTIG!)**
- ✅ **Minimum 5-8 Keywords**
- ✅ Verschiedene Such-Varianten
- ✅ Synonyme einbeziehen
- ✅ IPs, Hostnamen, Marken

**Beispiel:**
```python
keywords = [
    "nas", "synology", "ds720+",        # Gerät & Modell
    "ssh", "server", "docker",          # Funktion
    "production", "192.168.178.123"     # Kontext & IP
]
```

❌ **Nicht:** `["nas", "server", "info"]` (zu generisch, zu wenige)

---

### 2. **Title**
- ✅ **Maximal 50 Zeichen**
- ✅ Beschreibend, nicht generisch
- ✅ Wichtigste Info zuerst

**Beispiele:**
```
✅ "Synology DS720+ NAS Production"
✅ "MacBook Pro 13-inch 2017 Specs"
✅ "Grocery App Deployment Workflow"

❌ "NAS Information"
❌ "Server"
❌ "Deployment"
```

---

### 3. **Content**
- ✅ **Erste Zeile:** Kurze Zusammenfassung
- ✅ **Weitere Zeilen:** Details mit `\n`
- ✅ Commands, IPs, Pfade explizit
- ✅ Strukturiert & lesbar

**Beispiel:**
```python
content = """Synology DS720+ NAS
IP: 192.168.178.123
SSH: ssh Pierre@192.168.178.123
Modell: DS720+
CPU: Intel Celeron J4125 4-Core
RAM: 6GB DDR4
Storage: 2x 4TB (RAID 1)
Verwendung: Production Docker Host"""
```

❌ **Nicht:** `"NAS mit 4TB und Docker"` (zu unstrukturiert)

---

### 4. **Category**
Wähle die passende Kategorie:

| Category | Verwendung | ID-Bereich |
|----------|------------|------------|
| `infrastructure` | Server, Hardware, Netzwerk, IPs | 300-399 |
| `deployment` | CI/CD, Docker, Build-Prozesse | 600-699 |
| `code-pattern` | Wiederverwendbare Code-Snippets | 400-499 |
| `troubleshooting` | Fixes, Error-Solutions | 500-599 |

---

### 5. **ID-Vergabe**
- ✅ **Automatisch:** Nächste freie ID im Bereich
- ✅ **Manuell:** Nur bei spezifischen Gründen

**ID-Schema:**
```
300-399: Infrastructure
  300: NAS
  301: MacBook
  302: iMac
  303: SSH Credentials
  304: Network Overview
  ...

400-499: Code-Patterns
  400: Python Async Pattern
  401: Docker Compose Template
  ...

500-599: Troubleshooting
  500: Docker Container Restart Fix
  501: PostgreSQL Connection Error
  ...

600-699: Deployment
  600: Grocery App Deployment
  601: Home Assistant Deployment
  ...
```

---

## 📝 Template für neuen Eintrag

```python
import json, urllib.request
from datetime import datetime

# Nächste freie ID ermitteln
req = urllib.request.Request(
    "http://localhost:6333/collections/project_knowledge/points/scroll",
    data=json.dumps({"limit": 100, "with_payload": True, "with_vector": False}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
result = json.loads(urllib.request.urlopen(req).read())
existing_ids = [point['id'] for point in result['result']['points']]
next_id = 300
while next_id in existing_ids:
    next_id += 1

# Eintrag erstellen
entry = {
    "id": next_id,
    "vector": [0.0] * 384,
    "payload": {
        "title": "Titel max. 50 Zeichen",
        "content": "Erste Zeile: Zusammenfassung\nDetails:\n- Command 1\n- IP: 192.168.x.x\n- Weitere Infos",
        "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5", "keyword6"],
        "category": "infrastructure",  # oder deployment/code-pattern/troubleshooting
        "date": datetime.now().strftime("%Y-%m-%d")
    }
}

# Speichern
req = urllib.request.Request(
    "http://localhost:6333/collections/project_knowledge/points",
    data=json.dumps({"points": [entry]}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='PUT'
)
urllib.request.urlopen(req)
print(f"✅ Gespeichert unter ID {next_id}")
```

---

## 🚀 Helper Script nutzen

**Einfacher Weg:**
```bash
python .devtools/qdrant_helper.py
```

**Im Code:**
```python
from .devtools.qdrant_helper import save_to_qdrant

save_to_qdrant(
    title="Intel NUC Server",
    content="Intel NUC\nIP: 192.168.178.124\nCPU: i7 8-Core\nRAM: 16GB",
    keywords=["nuc", "intel", "server", "i7", "16gb", "hardware"],
    category="infrastructure"
)
```

---

## 🧪 Nach dem Speichern testen

```
1. MCP Cache löschen:
   Ctrl+Shift+P → MCP: Reset Cached Tools

2. VS Code neu laden:
   Ctrl+Shift+P → Developer: Reload Window

3. Testen:
   /qd [deine keywords]
```

---

## ❌ Häufige Fehler

### 1. Zu wenige Keywords
```python
❌ keywords = ["nas", "server", "info"]
✅ keywords = ["nas", "synology", "ds720+", "ssh", "server", "docker", "production", "192.168.178.123"]
```

### 2. Generischer Title
```python
❌ title = "Server"
✅ title = "Synology DS720+ Production NAS"
```

### 3. Unstrukturierter Content
```python
❌ content = "NAS mit 4TB und Docker"
✅ content = """Synology DS720+ NAS
IP: 192.168.178.123
SSH: ssh Pierre@192.168.178.123
Storage: 2x 4TB RAID 1
Docker: Ja"""
```

### 4. Falsche Category
```python
❌ category = "server"  # Existiert nicht!
✅ category = "infrastructure"
```

### 5. ID-Kollision
```python
❌ id = 300  # Könnte schon existieren
✅ id = get_next_id()  # Automatisch nächste freie ID
```

---

## 📊 Qualitäts-Check

**Vor dem Speichern fragen:**
- [ ] Habe ich **5-8 Keywords**?
- [ ] Ist der **Title < 50 Zeichen**?
- [ ] Ist der **Content strukturiert** (mit `\n`)?
- [ ] Habe ich die **richtige Category**?
- [ ] Ist die **ID eindeutig** im richtigen Bereich?
- [ ] Sind **IPs, Commands, Pfade** explizit angegeben?
- [ ] Habe ich **Synonyme** in Keywords?

---

## 🎯 Beispiele für perfekte Einträge

### Infrastructure
```python
{
    "id": 307,
    "payload": {
        "title": "Intel NUC i7 Development Server",
        "content": "Intel NUC\nIP: 192.168.178.124\nSSH: ssh admin@192.168.178.124\nCPU: Intel i7-1165G7 4-Core (8-Thread)\nRAM: 32GB DDR4 3200MHz\nStorage: 1TB NVMe SSD\nNetwork: 2x 1GbE\nOS: Ubuntu 22.04 LTS\nVerwendung: Development, CI/CD",
        "keywords": ["nuc", "intel", "i7", "server", "dev", "hardware", "ubuntu", "32gb", "192.168.178.124"],
        "category": "infrastructure"
    }
}
```

### Deployment
```python
{
    "id": 601,
    "payload": {
        "title": "Home Assistant Deployment NAS",
        "content": "Home Assistant auf NAS deployen:\n\n1. SSH: ssh Pierre@192.168.178.123\n2. cd /volume1/docker/homeassistant\n3. git pull origin main\n4. /usr/local/bin/docker-compose down\n5. /usr/local/bin/docker-compose up -d --build\n6. /usr/local/bin/docker-compose logs -f\n\nURL: http://192.168.178.123:8123\nConfig: /volume1/docker/homeassistant/config",
        "keywords": ["homeassistant", "deployment", "deploy", "nas", "docker", "compose", "automation"],
        "category": "deployment"
    }
}
```

### Code Pattern
```python
{
    "id": 401,
    "payload": {
        "title": "Python FastAPI Async Pattern",
        "content": "FastAPI Async Pattern mit Dependency Injection:\n\n```python\nfrom fastapi import FastAPI, Depends\nfrom typing import AsyncGenerator\n\nasync def get_db() -> AsyncGenerator:\n    db = await create_connection()\n    try:\n        yield db\n    finally:\n        await db.close()\n\n@app.get(\"/items\")\nasync def read_items(db = Depends(get_db)):\n    return await db.fetch_all(\"SELECT * FROM items\")\n```\n\nVorteile: Connection Pooling, Auto-Cleanup, Type-Safe",
        "keywords": ["python", "fastapi", "async", "pattern", "dependency", "injection", "database", "code"],
        "category": "code-pattern"
    }
}
```

---

## 🔄 Einträge aktualisieren

**Gleiche ID verwenden, nur payload ändern:**
```python
# Bestehenden Eintrag laden
entry_id = 307

# Payload aktualisieren
updated_entry = {
    "id": entry_id,
    "vector": [0.0] * 384,
    "payload": {
        "title": "Intel NUC i7 Dev Server (Updated)",
        "content": "... aktualisierte Infos ...",
        "keywords": [...],
        "category": "infrastructure",
        "date": "2025-11-02"  # Neues Datum!
    }
}

# PUT Request wie beim Speichern
```

---

**💡 Tipp:** Nutze das Helper-Script (`.devtools/qdrant_helper.py`) für automatische ID-Verwaltung und Validierung!
