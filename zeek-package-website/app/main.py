from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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


@app.get("/")
async def home():
    data = {
        "text": "hi"
    }
    return {"data": data}


@app.get("/page/{page_name}")
async def page(page_name: str):
    data = {
        "page": page_name
    }
    return {"data": data}
