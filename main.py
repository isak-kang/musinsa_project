from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.DB import get_item

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.get("/top100", response_class=HTMLResponse)
async def index(request: Request):
    items = get_item()  # DB에서 가져온 아이템 목록
    return templates.TemplateResponse("top100.html", context={"request": request, "context": items})

@app.get("/item_detail/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: int):
    items = get_item()  # DB에서 가져온 아이템 목록
    item = next((item for item in items if item["item_id"] == item_id), None)
    if item:
        return templates.TemplateResponse("item_detail.html", {"request": request, "item": item})
    else:
        return HTMLResponse("Item not found", status_code=404)