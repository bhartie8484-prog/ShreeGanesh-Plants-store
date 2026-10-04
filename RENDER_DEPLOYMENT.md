# Render deployment

## Render service settings

- Runtime: `Python 3`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --workers 1 --threads 4 --timeout 120 app:app`
- Health check path: `/health`

The same settings are included in `render.yaml` for Blueprint deployments.

## Required environment variable

Set `DATABASE_URL` in the Render dashboard to a publicly reachable MySQL URL:

```text
mysql://USERNAME:PASSWORD@HOST:3306/plant_store
```

Do not use `localhost` in production. Import `database/schema.sql` into that
database before opening the store. `SECRET_KEY` is generated automatically
when deploying with the Blueprint; for a manually created service, add a long
random `SECRET_KEY` in the Render dashboard.

## Local development

Gunicorn is a Linux/Unix server and does not run on Windows. Continue to use:

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```
