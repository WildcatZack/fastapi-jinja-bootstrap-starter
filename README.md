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
