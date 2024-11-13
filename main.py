from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.DB import get_item
from utils.graph import graph_url
from analysis_model.size_recommend.XGB import predict_size

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
    


@app.api_route("/item_detail/{item_id}", methods=["GET", "POST"], response_class=HTMLResponse)
async def item_detail(
    request: Request,
    item_id: int,
    input_height: float = Form(None),
    input_weight: float = Form(None),
    input_gender: str = Form(None)
):
    items = get_item()  # DB에서 가져온 아이템 목록
    item = next((item for item in items if item["item_id"] == item_id), None)
    
    if not item:
        return HTMLResponse("Item not found", status_code=404)
    
    # GET 요청 처리
    if request.method == "GET":
        # 그래프 URL 생성
        graph_url_value = graph_url(item["positive_ratio"], item["negative_ratio"])
        return templates.TemplateResponse("item_detail.html", {"request": request, "item": item, "graph_url": graph_url_value})

    # POST 요청 처리
    elif request.method == "POST":
        try:
            # 사이즈 예측 수행
            size = predict_size(input_height, input_weight, input_gender)
            # GET과 동일한 그래프 URL 생성
            graph_url_value = graph_url(item["positive_ratio"], item["negative_ratio"])
            return templates.TemplateResponse("item_detail.html", {"request": request, "item": item, "size": size, "graph_url": graph_url_value})
        except ValueError as e:
            return HTMLResponse(str(e), status_code=400)

