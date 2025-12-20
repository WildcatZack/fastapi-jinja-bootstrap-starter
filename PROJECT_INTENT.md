# Project Intent — fastapi-jinja-bootstrap-starter (opinionated)

## Who this is for
This template is for me + future me. It is documented, opinionated, and optimized for speed and repeatability.

## The promise
I should never have to wire up the following again:
- FastAPI + Jinja
- Bootstrap (SCSS build pipeline)
- Docker dev/prod workflows (dev: hot reload, prod: single image)

Fork → running in under ~10 minutes.

## Non-goals
- Not a universal framework or “covers every case” starter.
- Not a long-form tutorial.
- End users should not need Node at runtime.
- The repo should not require committing compiled frontend assets.

## Asset pipeline philosophy
- Frontend source lives in `frontend/` (SCSS/JS/etc.)
- Compiled outputs are produced into the backend static directory (served by the app), e.g. `app/static/`
- Compiled outputs are NOT committed to git
- Production assets are built at image build time (multi-stage) and copied into the final runtime image
- Development assets are rebuilt automatically via a separate dev container

## Canonical paths (expected)
- Backend app: `app/`
- Templates: `app/templates/`
- Static assets (served): `app/static/`
- Frontend sources: `frontend/`

## Canonical workflows

### Development (docker compose)
- `docker compose up` is the primary dev path
- Two containers are allowed in dev:
  1) `api`: FastAPI + Jinja with Python reload
  2) `assets`: Node watcher that recompiles assets into `app/static/`
- Host should NOT store `node_modules`:
  - `node_modules` lives in a named Docker volume attached to the `assets` container

### Production (single container image)
- Production output is a single container image
- Node is not present in the final runtime image
- Assets are built in a Node build stage and copied into the Python runtime stage

## Definition of done (minimum)
A fresh fork can:
- run `docker compose up`
- render a Jinja page
- apply Bootstrap styling
- hot reload templates in dev
- rebuild static assets in dev when frontend sources change
- build a single production image with baked assets
