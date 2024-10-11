# app/routers/home.py

import logging
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from .. import models  # Updated import
from ..utils.video_processing import gen_frames
from ..utils.image_processing import get_description, get_captured_images
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    logger.info("Serving home page.")
    return templates.TemplateResponse("home.html", {"request": request})

@router.post("/set_model")
async def set_model(model: str = Form(...), model_path: Optional[str] = Form(None)):
    if not model_path:
        model_path = "app/current_best.pt"
    logger.info(f"Received model: {model}, model_path: {model_path}")
    try:
        models.load_model(model, model_path=model_path)
        logger.info(f"Model '{model}' with path '{model_path}' loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading model '{model}': {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error."})
    return RedirectResponse(url="/", status_code=303)

@router.get("/video_feed")
async def video_feed():
    logger.info("Starting video feed.")
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.get("/description")
def description():
    logger.info("Fetching description.")
    return JSONResponse(get_description())

@router.get("/captured_images")
def captured_images():
    logger.info("Fetching captured images.")
    return JSONResponse(get_captured_images())

# conda activate yolov10-env 
# uvicorn app.main:app --reload 
