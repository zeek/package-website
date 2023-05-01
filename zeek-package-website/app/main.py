from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.update import update
from fastapi_utils.tasks import repeat_every

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "text": "Hello World!"
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


# example created a dynamic page based on page name, this can be modified for our packages
@app.get("/packages/{package_name}", response_class=HTMLResponse)
async def package(request: Request, package_name: str):
    data = {
        "package": package_name
    }
    return templates.TemplateResponse("package-info.html", {"request": request, "data": data})


@app.on_event("startup")
@repeat_every(seconds=60 * 4)
async def update_helper():
    update("aggregate.meta")
