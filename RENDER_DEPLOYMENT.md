# Render deployment

## Render service settings

- Runtime: `Python 3`
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --workers 1 --threads 4 --timeout 120 app:app`
- Health check path: `/health`

The same settings are included in `render.yaml` for Blueprint deployments.

## Required environment variable

Set `DATABASE_URL` in the Render dashboard to the Aiven service URI. Both
PostgreSQL and MySQL are supported.

For the Aiven PostgreSQL service, use the full `Service URI` shown in Aiven:

```text
postgres://avnadmin:PASSWORD@HOST:PORT/defaultdb?sslmode=require
```

Click `CLICK TO REVEAL PASSWORD` in Aiven before copying. Do not use
placeholder text like `actual_user`, `actual_password`, `mysql_host`, or
`actual-hostname.provider.com`.

The app creates the required tables and product catalogue automatically on
startup. `SECRET_KEY` is generated automatically when deploying with the
Blueprint; for a manually created service, add a long random `SECRET_KEY` in
the Render dashboard.

## Local development

Gunicorn is a Linux/Unix server and does not run on Windows. Continue to use:

```powershell
.\venv\Scripts\Activate.ps1
python app.py
```
