# VS Code Projekt-Template Automatisierung

## 📁 Option 1: User Templates (Empfohlen)

### Setup (Einmalig):

1. **Erstelle Template-Ordner:**
   ```bash
   mkdir -p ~/vscode-templates/default-project
   ```

2. **Kopiere Template-Dateien:**
   ```bash
   cp -r .github ~/vscode-templates/default-project/
   cp -r .devtools ~/vscode-templates/default-project/
   cp -r .vscode ~/vscode-templates/default-project/
   ```

3. **Erstelle Template-Script:**
   ```bash
   # ~/vscode-templates/new-project.sh
   #!/bin/bash
   PROJECT_NAME="$1"
   cp -r ~/vscode-templates/default-project "$PROJECT_NAME"
   cd "$PROJECT_NAME"
   code .
   ```

### Verwendung:
```bash
~/vscode-templates/new-project.sh mein-neues-projekt
```

---

## 📁 Option 2: VS Code Extension

### Installation:

1. **Installiere "Project Templates" Extension:**
   ```
   Ctrl+Shift+P → Extensions: Install Extensions
   Suche: "Project Manager" oder "Project Templates"
   ```

2. **Template registrieren:**
   - Öffne dieses Projekt
   - `Ctrl+Shift+P` → `Project Manager: Save Project`
   - Name: "Default VS Code Template"

### Verwendung:
```
Ctrl+Shift+P → Project Manager: Open Project
→ Wähle Template
→ Clone/Copy
```

---

## 📁 Option 3: Git Template Repository

### Setup (Einmalig):

1. **Erstelle Git Repo als Template:**
   ```bash
   cd ~/vscode-templates
   git init default-project
   cd default-project
   
   # Kopiere Files
   cp -r /path/to/grocery-app/.github .
   cp -r /path/to/grocery-app/.devtools .
   cp -r /path/to/grocery-app/.vscode .
   
   # Erstelle README
   echo "# VS Code Project Template" > README.md
   
   git add .
   git commit -m "Initial template"
   
   # Optional: Push zu GitHub als Template Repo
   gh repo create vscode-project-template --template --public
   git push -u origin main
   ```

2. **Als GitHub Template markieren:**
   - GitHub → Repository Settings
   - ✅ Template repository

### Verwendung:
```bash
# Neues Projekt von Template
git clone https://github.com/DEIN_USER/vscode-project-template.git mein-projekt
cd mein-projekt
rm -rf .git
git init
code .
```

---

## 📁 Option 4: Shell Alias (Schnellste Methode)

### Setup in `.bashrc` oder `.zshrc`:

```bash
# VS Code Projekt Creator
function new-vscode-project() {
    PROJECT_NAME="$1"
    TEMPLATE_PATH="$HOME/vscode-templates/default-project"
    
    if [ -z "$PROJECT_NAME" ]; then
        echo "Usage: new-vscode-project <name>"
        return 1
    fi
    
    # Kopiere Template
    cp -r "$TEMPLATE_PATH" "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    
    # Git Init
    git init
    
    # Öffne in VS Code
    code .
    
    echo "✅ Projekt '$PROJECT_NAME' erstellt!"
}
```

### Verwendung:
```bash
new-vscode-project mein-neues-projekt
```

---

## 📁 Option 5: VS Code Task (Im Projekt)

### Erstelle `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Init New Project with Template",
      "type": "shell",
      "command": "${workspaceFolder}/.devtools/init-vscode-project.sh",
      "args": ["${input:projectName}", "${input:projectPath}"],
      "problemMatcher": []
    }
  ],
  "inputs": [
    {
      "id": "projectName",
      "type": "promptString",
      "description": "Projektname"
    },
    {
      "id": "projectPath",
      "type": "promptString",
      "description": "Projekt-Pfad",
      "default": "../"
    }
  ]
}
```

### Verwendung:
```
Ctrl+Shift+P → Tasks: Run Task
→ "Init New Project with Template"
```

---

## 📁 Option 6: NPM Package (Global)

### Setup:

1. **Erstelle Package:**
   ```bash
   mkdir -p ~/npm-packages/create-vscode-project
   cd ~/npm-packages/create-vscode-project
   
   npm init -y
   ```

2. **Erstelle `bin/create-vscode-project.js`:**
   ```javascript
   #!/usr/bin/env node
   const fs = require('fs-extra');
   const path = require('path');
   
   const projectName = process.argv[2];
   const templatePath = path.join(__dirname, '../template');
   
   if (!projectName) {
       console.error('❌ Projektname erforderlich');
       process.exit(1);
   }
   
   fs.copySync(templatePath, projectName);
   console.log(`✅ Projekt '${projectName}' erstellt!`);
   ```

3. **Installiere global:**
   ```bash
   npm link
   ```

### Verwendung:
```bash
create-vscode-project mein-projekt
```

---

## 🎯 Empfehlung für dich

**Verwende Option 4 (Shell Alias) + Option 2 (Scripts):**

1. **Einmalig Setup:**
   ```bash
   # Füge zu ~/.bashrc hinzu:
   alias new-project="$HOME/Desktop/Einkaufen/.devtools/init-vscode-project.sh"
   
   source ~/.bashrc
   ```

2. **Neues Projekt erstellen:**
   ```bash
   new-project mein-neues-projekt ~/projects/
   ```

3. **Automatisch:**
   - ✅ Copilot Instructions kopiert
   - ✅ Dev-Tools kopiert
   - ✅ VS Code Settings erstellt
   - ✅ Qdrant ready
   - ✅ MCP Server connected

---

## 📝 Nächste Schritte

1. **Wähle eine Methode** (Empfehlung: Option 4)
2. **Teste es:**
   ```bash
   new-project test-projekt
   cd test-projekt
   code .
   ```
3. **Prüfe:**
   - `.github/copilot-instructions.md` ✓
   - `.devtools/` mit allen Files ✓
   - `/qd test` funktioniert ✓

---

## 🔄 Updates propagieren

**Wenn du die Template-Files updatest:**

```bash
# Update Template
cp .github/copilot-instructions.md ~/vscode-templates/default-project/.github/
cp .devtools/* ~/vscode-templates/default-project/.devtools/

# Bestehende Projekte updaten:
find ~/projects -name ".github" -type d -exec cp \
  ~/vscode-templates/default-project/.github/copilot-instructions.md \
  {}/copilot-instructions.md \;
```
