# FastAPI + Jinja + Bootstrap Starter

A minimal FastAPI starter that pairs Jinja templates with Bootstrap styling and ships with Docker Compose for both hot-reload development and production builds.

## Features
- FastAPI app configured with Jinja2 templates and static file serving
- Bootstrap 5 compiled locally from source (no CDN) with room for theme customization
- Reusable base layout plus navbar partial and demo page
- Dockerfile with dev and production targets; Compose profiles for each and a Node-based asset watcher

## Getting started

### Prerequisites
- Docker and Docker Compose
- Alternatively, a local Python 3.11 environment with `pip`
- Node 20+ for building Bootstrap assets

### Run with Docker (development)
```bash
docker compose up --build
```
The dev services mount your local files, run the Node asset watcher (`npm run dev`), and start `uvicorn --reload` at [http://localhost:8000](http://localhost:8000).

### Run with Docker (production profile)
```bash
docker compose --profile production up --build
```
This builds the optimized image using the `prod` stage (including compiled Bootstrap assets) and exposes the app on port 8000.

### Run without Docker
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npm install
npm run build
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting broken CSS/JS

If the navbar toggle, icons, or layout look unstyled, the compiled assets likely
weren't generated. Grab these quick diagnostics so we can pinpoint the issue:

1. Check whether the dev asset watcher produced the files (look for the copy and
   watch steps completing):

   ```bash
   docker compose logs assets --tail=50
   docker compose logs assets --follow
   ```

2. Confirm the compiled outputs exist and aren't placeholders (placeholder files
   are only a few lines long):

   ```bash
   ls -lh app/static/css app/static/js app/static/fonts
   head -n 8 app/static/css/main.css
   head -n 8 app/static/js/main.js
   head -n 8 app/static/css/bootstrap-icons.css
   ```

3. If the assets are missing or still placeholders, rerun the build and capture
   the logs:

   ```bash
   npm run build
   # or inside Docker: docker compose run --rm assets npm run build
   ```

Sharing the logs from steps 1–3 will make it straightforward to see whether the
Sass/esbuild pipeline finished and whether the icon fonts were copied into
`app/static/fonts`.

## Project structure
- `app/main.py`: FastAPI app wiring templates, static files, and the demo route
- `app/templates/`: Jinja templates with `base.html`, navbar partial, and `index.html`
- `app/static/`: Static assets output from the Node build (`npm run build`)
- `frontend/`: Source files for Bootstrap customization (`scss` and `js` entry points)
- `Dockerfile`: Multi-stage build with frontend asset compilation and Python stages
- `docker-compose.yml`: Dev service, asset watcher, and a `production` profile for the prod image

## Extending
- Customize Bootstrap variables or add components in `frontend/scss/main.scss`
- Add JavaScript behavior in `frontend/js/main.js`
- Add routes in `app/main.py` or split into routers under `app/`
- Create more templates in `app/templates` and static files in `app/static`
- Adjust environment variables or ports in `docker-compose.yml` as needed
