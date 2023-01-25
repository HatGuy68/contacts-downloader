from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)



@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    numbers = None
    context = {'request': request, 'numbers': numbers}
    return templates.TemplateResponse("index.html", context)