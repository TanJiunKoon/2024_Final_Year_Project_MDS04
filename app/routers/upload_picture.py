# app/routers/upload_picture.py

import logging
from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..utils.image_processing import process_uploaded_image

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)

@router.get("/upload_picture", response_class=HTMLResponse)
async def upload_picture_form(request: Request):
    logger.info("Serving upload picture form.")
    return templates.TemplateResponse("upload_picture.html", {"request": request})

@router.post("/process_picture", response_class=HTMLResponse)
async def process_picture(request: Request, file: UploadFile = File(...)):
    logger.info(f"Received picture upload: {file.filename}")
    try:
        result_html = await process_uploaded_image(file)
        logger.info("Picture processed successfully.")
    except Exception as e:
        logger.error(f"Error processing picture: {e}")
        return HTMLResponse(content="An error occurred during processing.", status_code=500)
    return templates.TemplateResponse("process_picture.html", {"request": request, "result_html": result_html})
