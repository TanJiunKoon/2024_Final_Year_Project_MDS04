# app/routers/upload_video.py

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from ..utils.video_processing import process_video_background

import uuid
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

task_status = {}
task_results = {}
processed_videos_dir = "app/static/processed_videos"

@router.get("/upload_video", response_class=HTMLResponse)
async def upload_video_form(request: Request):
    return templates.TemplateResponse("upload_video.html", {"request": request})

@router.post("/process_video", response_class=JSONResponse)
async def process_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    # Generate a unique task ID
    task_id = str(uuid.uuid4())
    task_status[task_id] = "Processing"

    # Save the uploaded file to a temporary location
    temp_video_path = f"app/static/temp_video_{task_id}.mp4"
    with open(temp_video_path, "wb") as f:
        f.write(await file.read())

    # Start the background task
    background_tasks.add_task(process_video_background, temp_video_path, task_id, task_status, task_results)

    # Return the task ID to the client
    return {"task_id": task_id}

@router.get("/video_status/{task_id}")
async def video_status(task_id: str):
    status = task_status.get(task_id, "Unknown")
    if status == "Processing":
        return {"status": "Processing"}
    elif status == "Completed":
        result_html = task_results.get(task_id, "")
        # Clean up the task data
        del task_status[task_id]
        del task_results[task_id]
        return {"status": "Completed", "result_html": result_html}
    else:
        return {"status": "Error"}
