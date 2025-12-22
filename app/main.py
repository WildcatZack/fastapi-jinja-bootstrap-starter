from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


def theme_context(request: Request) -> dict[str, str]:
    theme = request.query_params.get("theme", "").lower()
    if theme == "kentucky":
        return {
            "theme_class": "theme-kentucky",
            "theme_query": "?theme=kentucky",
            "theme_name": "kentucky",
        }

    return {"theme_class": "", "theme_query": "", "theme_name": "default"}


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "active_page": "home", **theme_context(request)},
    )


@app.get("/about", response_class=HTMLResponse)
def read_about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "active_page": "about", **theme_context(request)},
    )


@app.get("/docs-page", response_class=HTMLResponse)
def read_docs(request: Request):
    return templates.TemplateResponse(
        "docs.html",
        {"request": request, "active_page": "docs", **theme_context(request)},
    )
