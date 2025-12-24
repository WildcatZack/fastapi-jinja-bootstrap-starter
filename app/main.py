from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "active_page": "home"},
    )


@app.get("/about", response_class=HTMLResponse)
def read_about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "active_page": "about"},
    )


@app.get("/docs-page", response_class=HTMLResponse)
def read_docs(request: Request):
    return templates.TemplateResponse(
        "docs.html",
        {"request": request, "active_page": "docs"},
    )


@app.get("/styleguide", response_class=HTMLResponse)
def read_styleguide(request: Request):
    return templates.TemplateResponse(
        "styleguide/index.html",
        {"request": request, "active_page": "styleguide", "styleguide_section": "index"},
    )


@app.get("/styleguide/layout", response_class=HTMLResponse)
def read_styleguide_layout(request: Request):
    return templates.TemplateResponse(
        "styleguide/layout.html",
        {"request": request, "active_page": "styleguide", "styleguide_section": "layout"},
    )


@app.get("/styleguide/content", response_class=HTMLResponse)
def read_styleguide_content(request: Request):
    return templates.TemplateResponse(
        "styleguide/content.html",
        {"request": request, "active_page": "styleguide", "styleguide_section": "content"},
    )


@app.get("/styleguide/forms", response_class=HTMLResponse)
def read_styleguide_forms(request: Request):
    return templates.TemplateResponse(
        "styleguide/forms.html",
        {"request": request, "active_page": "styleguide", "styleguide_section": "forms"},
    )


@app.get("/styleguide/components", response_class=HTMLResponse)
def read_styleguide_components(request: Request):
    return templates.TemplateResponse(
        "styleguide/components.html",
        {"request": request, "active_page": "styleguide", "styleguide_section": "components"},
    )


@app.get("/styleguide/utilities", response_class=HTMLResponse)
def read_styleguide_utilities(request: Request):
    return templates.TemplateResponse(
        "styleguide/utilities.html",
        {"request": request, "active_page": "styleguide", "styleguide_section": "utilities"},
    )
