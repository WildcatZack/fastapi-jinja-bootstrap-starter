import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FastAPI Jinja Bootstrap Starter")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

log = logging.getLogger("uvicorn.error")


@app.on_event("startup")
async def warn_if_static_not_built() -> None:
    """Emit a clear log message when CSS/JS/icon assets are placeholders.

    This helps surface cases where the frontend build has not completed, which
    would manifest as missing Bootstrap styles, icon glyphs, or navbar
    interactivity. The placeholders are committed for source control but should
    be replaced by running `npm run build` (or the Compose dev profile).
    """

    placeholder_markers = {
        Path("app/static/css/main.css"): "Built CSS output.",
        Path("app/static/js/main.js"): "Built JS output.",
        Path("app/static/css/bootstrap-icons.css"): "Bootstrap Icons CSS placeholder.",
    }

    missing: list[str] = []
    placeholders: list[str] = []

    for path, marker in placeholder_markers.items():
        if not path.exists():
            missing.append(str(path))
            continue

        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:200]
        except Exception as exc:  # pragma: no cover - defensive logging only
            log.warning("Unable to read %s: %s", path, exc)
            continue

        if marker in head:
            placeholders.append(str(path))

    if missing or placeholders:
        log.warning(
            "Static assets need a frontend build. Missing: %s; placeholders: %s. "
            "Run `npm run build` locally or check `docker compose logs assets` "
            "to confirm the dev watcher finished copying CSS/JS/icons.",
            ", ".join(missing) if missing else "none",
            ", ".join(placeholders) if placeholders else "none",
        )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    context = {
        "request": request,
        "page_title": "Welcome",
        "hero_title": "FastAPI × Jinja × Bootstrap",
        "hero_lead": (
            "A ready-to-use starter with Dockerized development and production builds. "
            "Use this scaffold to ship your next idea faster."
        ),
        "features": [
            {
                "title": "Jinja templating",
                "description": "Compose reusable pages with a base layout and partials.",
                "icon": "bi-braces",
            },
            {
                "title": "Bootstrap styling",
                "description": "Leverage Bootstrap 5 components and utilities from day one.",
                "icon": "bi-bootstrap",
            },
            {
                "title": "Docker ready",
                "description": "Hot-reload for local dev and a production image profile.",
                "icon": "bi-box-seam",
            },
        ],
    }
    return templates.TemplateResponse("index.html", context)
