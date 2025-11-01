#!/usr/bin/env python3
"""
Qdrant Setup Script
Erstellt die initiale Collection für Projekt-Wissen
"""

import json
import urllib.request
import urllib.error

QDRANT_URL = "http://localhost:6333"

def create_collection():
    """Erstelle project_knowledge Collection"""
    url = f"{QDRANT_URL}/collections/project_knowledge"
    data = {
        "vectors": {
            "size": 384,  # Kompatibel mit all-MiniLM-L6-v2
            "distance": "Cosine"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✓ Collection erstellt: {json.dumps(result, indent=2)}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 400:
            print("ℹ Collection existiert bereits")
            return True
        else:
            print(f"✗ Fehler: {e.code} - {e.read().decode('utf-8')}")
            return False
    except Exception as e:
        print(f"✗ Fehler: {e}")
        return False

def test_connection():
    """Teste Verbindung zu Qdrant"""
    try:
        with urllib.request.urlopen(f"{QDRANT_URL}/collections") as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"✓ Qdrant erreichbar! Collections: {len(data.get('result', {}).get('collections', []))}")
            return True
    except Exception as e:
        print(f"✗ Qdrant nicht erreichbar: {e}")
        return False

def add_test_entry():
    """Füge Test-Eintrag hinzu (ohne Embedding, nur für Keyword-Suche)"""
    url = f"{QDRANT_URL}/collections/project_knowledge/points"
    data = {
        "points": [
            {
                "id": 1,
                "vector": [0.0] * 384,  # Dummy-Vector
                "payload": {
                    "title": "NAS Infrastructure",
                    "content": "Synology NAS IP: 192.168.178.122, SSH: admin@192.168.178.122, Docker: /volume1/docker",
                    "keywords": ["nas", "synology", "infrastructure"],
                    "date": "2025-11-01",
                    "category": "infrastructure"
                }
            }
        ]
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✓ Test-Eintrag hinzugefügt: {json.dumps(result, indent=2)}")
            return True
    except Exception as e:
        print(f"✗ Fehler beim Hinzufügen: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Qdrant Setup\n")
    
    if not test_connection():
        print("\n⚠️  Qdrant ist nicht erreichbar. Stelle sicher, dass der Container läuft:")
        print("   docker ps | grep qdrant")
        exit(1)
    
    print()
    create_collection()
    
    print()
    add_test_entry()
    
    print("\n✅ Setup abgeschlossen!")
    print(f"\n📊 Qdrant Dashboard: http://localhost:6333/dashboard")
    print(f"📡 REST API: http://localhost:6333")
