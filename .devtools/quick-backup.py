#!/usr/bin/env python3
"""
Quick Backup Script - Git + Qdrant

Erstellt automatisch Git Commit und speichert Projekt-Info in Qdrant.
"""

import subprocess
import json
import urllib.request
import sys
from datetime import datetime

def git_backup(message_type="feat", description="Update"):
    """Erstellt Git Commit und pusht zu GitHub"""
    
    print("📊 Git Status...")
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("✓ Keine Änderungen zum Committen")
        return False
    
    print(f"Änderungen:\n{result.stdout}")
    
    # Stage all
    print("\n📁 Stage Files...")
    subprocess.run(["git", "add", "."])
    
    # Commit
    print("\n💾 Erstelle Commit...")
    commit_msg = f"{message_type}: {description}\n\nAutomatischer Backup-Commit\nDatum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Commit fehlgeschlagen: {result.stderr}")
        return False
    
    print("✅ Commit erstellt")
    
    # Push
    print("\n🚀 Push zu GitHub...")
    result = subprocess.run(["git", "push"], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Push fehlgeschlagen: {result.stderr}")
        return False
    
    print("✅ Pushed to GitHub")
    return True

def qdrant_backup(project_name, description, tech_stack, deployment_info):
    """Speichert Projekt-Info in Qdrant"""
    
    print("\n📝 Speichere in Qdrant...")
    
    # Nächste freie ID ermitteln
    req = urllib.request.Request(
        "http://localhost:6333/collections/project_knowledge/points/scroll",
        data=json.dumps({"limit": 100, "with_payload": True, "with_vector": False}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        result = json.loads(urllib.request.urlopen(req).read())
        existing_ids = [point['id'] for point in result['result']['points']]
        next_id = 600
        while next_id in existing_ids:
            next_id += 1
    except Exception as e:
        print(f"⚠️  Warnung: Konnte bestehende IDs nicht laden: {e}")
        next_id = 600
    
    # Eintrag erstellen
    content = f"""{project_name}

{description}

Tech-Stack:
{tech_stack}

Deployment:
{deployment_info}

Letzte Änderung: {datetime.now().strftime('%Y-%m-%d')}
Status: ✅ Active Development
"""
    
    entry = {
        "id": next_id,
        "vector": [0.0] * 384,
        "payload": {
            "title": f"{project_name} - Project Info",
            "content": content,
            "keywords": [
                project_name.lower().replace(" ", "-"),
                "project", "deployment", "backup",
                "info", "metadata"
            ],
            "category": "deployment",
            "project": project_name.lower().replace(" ", "-"),
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
    
    try:
        urllib.request.urlopen(req)
        print(f"✅ Gespeichert unter ID {next_id}")
        return True
    except Exception as e:
        print(f"❌ Qdrant-Speicherung fehlgeschlagen: {e}")
        return False

def main():
    print("=" * 50)
    print("  Quick Backup - Git + Qdrant")
    print("=" * 50)
    print()
    
    # User Input
    message_type = input("Commit Type (feat/fix/docs/chore) [feat]: ").strip() or "feat"
    description = input("Kurze Beschreibung: ").strip() or "Project update"
    
    # Git Backup
    print("\n" + "=" * 50)
    print("1️⃣  Git Backup")
    print("=" * 50)
    
    git_success = git_backup(message_type, description)
    
    # Qdrant Backup
    print("\n" + "=" * 50)
    print("2️⃣  Qdrant Backup")
    print("=" * 50)
    
    save_qdrant = input("\nProjekt-Info in Qdrant speichern? (j/n) [n]: ").strip().lower()
    
    qdrant_success = False
    if save_qdrant in ['j', 'y', 'ja', 'yes']:
        project_name = input("Projekt-Name: ").strip()
        project_desc = input("Projekt-Beschreibung: ").strip()
        tech_stack = input("Tech-Stack (z.B. Python, React, Docker): ").strip()
        deployment = input("Deployment-Info (z.B. NAS, Port 8080): ").strip()
        
        qdrant_success = qdrant_backup(project_name, project_desc, tech_stack, deployment)
    
    # Zusammenfassung
    print("\n" + "=" * 50)
    print("✅ Backup abgeschlossen")
    print("=" * 50)
    print(f"Git:    {'✅ Erfolg' if git_success else '❌ Fehlgeschlagen'}")
    print(f"Qdrant: {'✅ Erfolg' if qdrant_success else '⏭️  Übersprungen'}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Backup abgebrochen")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        sys.exit(1)
