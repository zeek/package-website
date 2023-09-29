from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


# example created a dynamic page based on page name, this can be modified for our packages
@app.get("/packages/{package_name}", response_class=HTMLResponse)
async def package(request: Request, package_name: str):
    result = p.get_info(package_name)
    if result is not None:
        readme = markdown.markdown(result["readme"])
    else:
        readme = "<p>This package does not appear to have a README</p>"
    data = {
        "package_name": package_name,
        "package_info": result,
        "package_readme": readme
    }
    # send users back to home page if package does not exist
    if result is not None:
        return templates.TemplateResponse("package-info.html", {"request": request, "data": data})
    else:
        return templates.TemplateResponse("index.html", {"request": request})


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    results = s.search(query)
    data = {
        "query": query,
        "results": results
    }
    return templates.TemplateResponse("search.html", {"request": request, "data": data})

@app.on_event("startup")
@repeat_every(seconds=60 * 4)
async def update_helper():
    update("aggregate.meta")