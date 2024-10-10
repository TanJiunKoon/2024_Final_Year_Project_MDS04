# app/routers/contact_us.py

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/contact_us", response_class=HTMLResponse)
async def contact_us(request: Request):
    return templates.TemplateResponse("contact_us.html", {"request": request})
