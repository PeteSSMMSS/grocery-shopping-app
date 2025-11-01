#!/usr/bin/env python3
"""
Chroma MCP Wrapper - Kompatibel mit Python 3.14
Lightweight MCP Server für Chroma ohne onnxruntime-Abhängigkeit
"""

import json
import sys
import os
from pathlib import Path

# Einfache Chroma-Alternative ohne schwere Dependencies
try:
    import sqlite3
    HAS_SQLITE = True
except ImportError:
    HAS_SQLITE = False

def send_response(data):
    """Sendet MCP-Response an stdout"""
    print(json.dumps(data), flush=True)

def handle_list_tools():
    """Liste verfügbare Chroma-Tools"""
    return {
        "tools": [
            {
                "name": "chroma_create_collection",
                "description": "Erstellt eine neue Chroma Collection",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "metadata": {"type": "object"}
                    },
                    "required": ["name"]
                }
            },
            {
                "name": "chroma_add_documents",
                "description": "Fügt Dokumente zu einer Collection hinzu",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "collection_name": {"type": "string"},
                        "documents": {"type": "array"},
                        "metadatas": {"type": "array"},
                        "ids": {"type": "array"}
                    },
                    "required": ["collection_name", "documents"]
                }
            },
            {
                "name": "chroma_query_documents",
                "description": "Sucht Dokumente in einer Collection",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "collection_name": {"type": "string"},
                        "query": {"type": "string"},
                        "n_results": {"type": "integer", "default": 5}
                    },
                    "required": ["collection_name", "query"]
                }
            }
        ]
    }

def main():
    """MCP Server Main Loop"""
    data_dir = Path(r"D:\Cooperate Design\Chroma")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Einfaches Logging
    log_file = data_dir / "mcp_wrapper.log"
    
    with open(log_file, "w") as log:
        log.write("Chroma MCP Wrapper gestartet\n")
        log.write(f"Python Version: {sys.version}\n")
        log.write(f"SQLite verfügbar: {HAS_SQLITE}\n")
        log.write(f"Data Dir: {data_dir}\n\n")
        
        # MCP Server Loop
        for line in sys.stdin:
            try:
                request = json.loads(line)
                method = request.get("method")
                
                log.write(f"Request: {method}\n")
                
                if method == "tools/list":
                    response = handle_list_tools()
                    send_response(response)
                elif method == "tools/call":
                    # Placeholder für Tool-Aufrufe
                    send_response({
                        "content": [{
                            "type": "text",
                            "text": "Chroma MCP Wrapper aktiv, aber Tools noch nicht implementiert"
                        }]
                    })
                else:
                    send_response({"error": f"Unknown method: {method}"})
                    
            except Exception as e:
                log.write(f"Error: {e}\n")
                send_response({"error": str(e)})

if __name__ == "__main__":
    main()
