from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="FastAPI Jinja Bootstrap Starter")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


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
