# Deployment Guide

## Strategic Product Placement Analysis

Instructions for deploying the Flask application to production environments.

---

## Deployment Options

| Platform | Difficulty | Cost | Recommended For |
|----------|------------|------|-----------------|
| Local (dev) | Easy | Free | Development |
| Heroku | Medium | Free tier available | Quick demos |
| PythonAnywhere | Easy | Free tier available | Student projects |
| AWS EC2 | Advanced | Pay-as-you-go | Production |
| Azure App Service | Medium | Free tier available | Enterprise |
| Docker | Medium | Varies | Containerized deploy |

---

## Option 1: Local Development Server

```bash
python app.py
```

- URL: http://127.0.0.1:5000
- Debug mode: enabled
- **Not for production use**

---

## Option 2: Gunicorn (Production WSGI)

### Install
```bash
pip install gunicorn
```

### Run
```bash
# Linux/macOS
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Windows (use waitress instead)
pip install waitress
waitress-serve --port=8000 app:app
```

### Configuration
| Flag | Value | Purpose |
|------|-------|---------|
| `-w 4` | 4 workers | Concurrent request handling |
| `-b 0.0.0.0:8000` | Bind address | Listen on all interfaces, port 8000 |
| `--timeout 120` | 120s | Tableau embed may need longer timeout |

---

## Option 3: Docker Deployment

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
```

### Build and Run
```bash
docker build -t product-placement-analysis .
docker run -p 5000:5000 -e TABLEAU_DASHBOARD_URL="your-url" product-placement-analysis
```

### docker-compose.yml (optional)
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_SECRET_KEY=change-me-in-production
      - TABLEAU_DASHBOARD_URL=https://public.tableau.com/views/...
      - TABLEAU_STORY_URL=https://public.tableau.com/views/...
    volumes:
      - ./data:/app/data:ro
```

---

## Option 4: Heroku

### Prerequisites
- Heroku CLI installed
- Heroku account

### Steps

1. Create `Procfile`:
   ```
   web: gunicorn app:app --timeout 120
   ```

2. Create `runtime.txt`:
   ```
   python-3.10.12
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create product-placement-analysis
   heroku config:set FLASK_SECRET_KEY=your-secret-key
   heroku config:set TABLEAU_DASHBOARD_URL=your-dashboard-url
   heroku config:set TABLEAU_STORY_URL=your-story-url
   git push heroku main
   ```

4. Open: `heroku open`

---

## Option 5: PythonAnywhere

1. Sign up at https://www.pythonanywhere.com
2. Upload project files via **Files** tab
3. Create virtualenv: `mkvirtualenv --python=python3.10 venv`
4. Install: `pip install -r requirements.txt`
5. Configure **Web** tab:
   - Source code: `/home/username/dataanalyis`
   - WSGI file: point to Flask app
6. Reload web app

### WSGI Configuration
```python
import sys
path = '/home/username/dataanalyis'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FLASK_SECRET_KEY` | Yes (prod) | Session encryption key |
| `TABLEAU_DASHBOARD_URL` | Yes | Tableau Public dashboard embed URL |
| `TABLEAU_STORY_URL` | Yes | Tableau Public story embed URL |
| `FLASK_DEBUG` | No | Set `False` in production |
| `FLASK_PORT` | No | Default 5000 |

### Update app.py for Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

TABLEAU_DASHBOARD_URL = os.getenv(
    'TABLEAU_DASHBOARD_URL',
    'https://public.tableau.com/views/ProductPositioningAnalysis/Dashboard'
)
TABLEAU_STORY_URL = os.getenv(
    'TABLEAU_STORY_URL',
    'https://public.tableau.com/views/ProductPositioningAnalysis/Story'
)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-me')
```

---

## Tableau Public Integration

### Pre-Deployment Checklist

- [ ] Workbook published to Tableau Public
- [ ] Dashboard embed URL tested in browser
- [ ] Story embed URL tested in browser
- [ ] URLs updated in environment variables or `app.py`
- [ ] Embed loads correctly from deployed domain (not just localhost)

### CORS / iframe Notes
Tableau Public embeds work via iframe/JavaScript API. No additional CORS configuration needed on the Flask side.

---

## Security Best Practices

1. **Never commit** `.env` files or `kaggle.json` to version control
2. **Change** `SECRET_KEY` from default in production
3. **Disable** `debug=True` in production (`app.run(debug=False)`)
4. **Use HTTPS** — configure SSL via reverse proxy (Nginx, Caddy)
5. **Read-only** data directory mount in Docker

---

## Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /app/static;
        expires 30d;
    }
}
```

---

## Post-Deployment Verification

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" https://your-domain.com/
# Expected: 200

# API check
curl https://your-domain.com/api/kpis
# Expected: JSON with status "success"

# Static assets
curl -s -o /dev/null -w "%{http_code}" https://your-domain.com/static/css/style.css
# Expected: 200
```

---

## Monitoring

| Tool | Purpose |
|------|---------|
| Heroku Logs | `heroku logs --tail` |
| Docker Logs | `docker logs <container-id>` |
| Uptime Robot | Free uptime monitoring |
| Sentry | Error tracking (optional) |

---

## Rollback Procedure

1. Identify last working commit: `git log --oneline`
2. Revert: `git revert <commit-hash>`
3. Redeploy: `git push heroku main` or rebuild Docker image
4. Verify endpoints return 200

---

## Support

- Installation issues → [Installation.md](Installation.md)
- Tableau publishing → [Tableau_Public_Publishing_Guide.md](../tableau/Tableau_Public_Publishing_Guide.md)
- User-facing help → [User_Guide.md](User_Guide.md)
