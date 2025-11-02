#!/usr/bin/env python3
"""
Qdrant Helper Script - Optimiert für GitHub Copilot MCP

Einfaches Speichern von Informationen in Qdrant mit automatischer ID-Verwaltung.
"""

import json
import urllib.request
from datetime import datetime

QDRANT_URL = "http://localhost:6333"
COLLECTION = "project_knowledge"

def get_next_id(category_start=300):
    """Ermittelt die nächste freie ID"""
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll",
        data=json.dumps({
            "limit": 100,
            "with_payload": True,
            "with_vector": False
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    result = json.loads(urllib.request.urlopen(req).read())
    existing_ids = [point['id'] for point in result['result']['points']]
    
    # Finde nächste freie ID im richtigen Bereich
    next_id = category_start
    while next_id in existing_ids:
        next_id += 1
    
    return next_id

def save_to_qdrant(title, content, keywords, category, auto_id=True, custom_id=None):
    """
    Speichert Eintrag in Qdrant
    
    Args:
        title: Kurzer Titel (max 50 Zeichen)
        content: Detaillierte Information mit Commands, IPs etc.
        keywords: Liste von 5-8 Keywords
        category: infrastructure | deployment | code-pattern | troubleshooting
        auto_id: Automatische ID-Vergabe
        custom_id: Manuelle ID (wenn auto_id=False)
    """
    
    # Validierung
    if len(keywords) < 5:
        print(f"⚠️  Warnung: Nur {len(keywords)} Keywords (empfohlen: 5-8)")
    
    if len(title) > 50:
        print(f"⚠️  Warnung: Title zu lang ({len(title)} Zeichen, max 50)")
    
    # ID ermitteln
    if auto_id:
        category_map = {
            'infrastructure': 300,
            'deployment': 600,
            'code-pattern': 400,
            'troubleshooting': 500
        }
        entry_id = get_next_id(category_map.get(category, 300))
    else:
        entry_id = custom_id
    
    # Eintrag erstellen
    entry = {
        "id": entry_id,
        "vector": [0.0] * 384,
        "payload": {
            "title": title,
            "content": content,
            "keywords": keywords,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    }
    
    # Speichern
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points",
        data=json.dumps({"points": [entry]}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read())
        if result.get("status") == "ok":
            print(f"✅ Gespeichert unter ID {entry_id}")
            print(f"   Title: {title}")
            print(f"   Keywords: {', '.join(keywords)}")
            print(f"   Category: {category}")
            return entry_id
        else:
            print(f"❌ Fehler: {result}")
            return None

def search_qdrant(keywords):
    """Sucht Einträge nach Keywords"""
    req = urllib.request.Request(
        f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll",
        data=json.dumps({
            "filter": {
                "must": [
                    {"key": "keywords", "match": {"any": keywords}}
                ]
            },
            "limit": 10,
            "with_payload": True,
            "with_vector": False
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    result = json.loads(urllib.request.urlopen(req).read())
    return result['result']['points']

# Beispiele
if __name__ == "__main__":
    print("Qdrant Helper - Beispiel-Nutzung\n")
    
    # Beispiel 1: Infrastructure
    save_to_qdrant(
        title="Intel NUC Server",
        content="Intel NUC\nIP: 192.168.178.124\nSSH: ssh admin@192.168.178.124\nCPU: i7 8-Core\nRAM: 16GB",
        keywords=["nuc", "intel", "server", "hardware", "i7", "16gb", "ssh", "192.168.178.124"],
        category="infrastructure"
    )
    
    print()
    
    # Beispiel 2: Code Pattern
    save_to_qdrant(
        title="Python Async Pattern",
        content="import asyncio\n\nasync def fetch_data():\n    # Async code here\n    pass",
        keywords=["python", "async", "asyncio", "pattern", "code", "concurrent"],
        category="code-pattern"
    )
    
    print("\n" + "="*50)
    print("Suche nach 'nuc server':")
    results = search_qdrant(["nuc", "server"])
    for point in results:
        print(f"  - {point['payload']['title']}")
