# GitHub Workflows (optional)

Dieser Ordner kann für GitHub Actions verwendet werden, z.B. für:

- **CI/CD:** Automatische Tests beim Push
- **Docker Build:** Automatisches Image-Building
- **Deployment:** Automatisches Deployment auf NAS

## Beispiel-Workflows (optional)

### 1. CI - Tests ausführen

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build containers
        run: docker compose up -d --build
      - name: Check health
        run: |
          sleep 10
          curl http://localhost:8080/health
```

### 2. Auto-Deploy auf NAS

```yaml
# .github/workflows/deploy.yml
name: Deploy to NAS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.NAS_HOST }}
          username: ${{ secrets.NAS_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /volume1/docker/einkaufen
            git pull
            /usr/local/bin/docker-compose down
            /usr/local/bin/docker-compose up -d --build
```

**Secrets in GitHub eintragen:**
- `NAS_HOST`: 192.168.178.123
- `NAS_USER`: Pierre
- `SSH_PRIVATE_KEY`: Dein SSH Private Key

---

Für den Anfang ist das manuelle Deployment (siehe DEPLOYMENT.md) ausreichend!
