# FastAPI Starter

## Quick start
1. Create your local environment file:
   ```bash
   cp .env.example .env
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open http://127.0.0.1:8000/ in your browser.

## UI proof

- Visit `/` to see the Bootstrap navbar, alert, and card components.
- Click `About` or `Docs` (`/about`, `/docs-page`) to confirm the active nav state updates.
- Use the "Toggle theme" button in the navbar (or the hero buttons) to switch between the default palette and the Kentucky theme. The selection is persisted in `localStorage` under `preferred-theme` so it survives refreshes and restarts. Clear that key (or toggle again) to reset. Bootstrap's built-in light/dark modes remain intact because the overrides stay scoped to the optional theme class.

## Development

- Build and start dev containers:
  ```bash
  docker compose up --build
  ```
- `api`: FastAPI with reload on port 8000.
- `assets`: Node watcher that rebuilds frontend assets into `app/static/`.

## Production image

Build the production image with compiled assets:
```bash
docker build -t <name> .
```

Run the container:
```bash
docker run -p 8000:8000 <name>
```

The production image bakes in frontend assets and does not require Node at runtime.

## Verification

- Development loop:
  - `docker compose up --build`
  - Edit `frontend/src/styles.scss` to rebuild `app/static/app.css`.
  - Edit `frontend/src/index.js` to rebuild `app/static/app.js`.
  - Updates to `app/templates/` render on refresh without restarting the server.
- Production check:
  - `docker build -t <name> .`
  - `docker run -p 8000:8000 <name>`
  - Confirm `http://127.0.0.1:8000/static/app.css` returns HTTP 200.
