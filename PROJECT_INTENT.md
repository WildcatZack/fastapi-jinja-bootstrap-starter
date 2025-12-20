# Project Intent — fastapi-jinja-bootstrap-starter (opinionated)

## Who this is for
This template is for *me + future me*. It is documented, opinionated, and optimized for speed and repeatability.

## The promise
I should never have to wire up:
- FastAPI + Jinja
- Bootstrap (via SCSS build)
- Docker dev/prod workflows

…ever again. Fork → running in under ~10 minutes.

## Non-goals
- This is not a universal framework or a “covers every case” starter.
- This is not a long-form tutorial.
- End users should not need Node at runtime.
- The repo should not require committing compiled frontend assets.

## Asset pipeline philosophy
- Frontend source lives in `frontend/` (SCSS/JS/etc.).
- Compiled outputs are produced into the backend static directory (e.g. `app/static/`).
- Compiled outputs are not committed to git.
- Production assets are built at image build time (multi-stage) and copied into the final runtime image.
- Development assets are rebuilt automatically (watch/hot reload) via a separate dev container.

## Canonical runtime paths
- Templates: `app/templates/`
- Static assets served by app: `app/static/`
- Frontend sources: `frontend/`

## Canonical workflows

### Development (docker compose)
- `docker compose up` is the primary dev path.
- Two containers are allowed in dev:
  1) `api` container: FastAPI + Jinja with Python reload
  2) `assets` container: Node watcher that recompiles assets into `app/static/`

Host should NOT store `node_modules`:
- `node_modules` lives in a named Docker volume attached to the `assets` container.

### Production (single container image)
- Production output is a single container image.
- Node is not present in the final runtime image.
- Assets are built in a Node build stage and copied into the Python runtime stage.

## Definition of done (minimum)
- Fresh fork:
  - `docker compose up`
  - opens in browser and renders a page using Jinja
  - Bootstrap styling is applied
  - editing a template reloads in dev
  - editing frontend source triggers rebuilt static assets in dev

## What to remove if it causes confusion
If something introduces ambiguity or “fallback magic” (e.g., placeholder assets, automatic CDN fallback), prefer removing it over expanding documentation or adding workarounds.
