#!/bin/bash
# Qdrant MCP Launcher mit Dependency-Fix
# Aktiviert UV und startet mcp-server-qdrant mit allen Dependencies

# UV aktivieren
source "$HOME/.local/bin/env" 2>/dev/null || true

# Environment Variables
export QDRANT_LOCAL_PATH="D:\\Cooperate Design\\Qdrant"
export COLLECTION_NAME="${COLLECTION_NAME:-dev_knowledge}"
export EMBEDDING_MODEL="${EMBEDDING_MODEL:-sentence-transformers/all-MiniLM-L6-v2}"
export TOOL_STORE_DESCRIPTION="${TOOL_STORE_DESCRIPTION:-Speichere Wissen über Projekte, Infrastructure, Code-Snippets, APIs, Docker-Konfigurationen}"
export TOOL_FIND_DESCRIPTION="${TOOL_FIND_DESCRIPTION:-Durchsuche das Langzeitgedächtnis nach relevantem Wissen}"

# FastMCP Dependencies installieren (falls noch nicht vorhanden)
export FASTMCP_DEPENDENCIES="fastembed,qdrant-client"

# Starte mcp-server-qdrant
exec uvx mcp-server-qdrant "$@"
