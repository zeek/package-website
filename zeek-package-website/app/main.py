from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from api.routes.api import router as api_router
# from core.events import create_start_app_handler
# from core.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION


# def get_application() -> FastAPI:
#    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
#    application.include_router(api_router, prefix=API_PREFIX)
#    pre_load = False
#    if pre_load:
#        application.add_event_handler("startup", create_start_app_handler(application))
#    return application


# app = get_application()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
