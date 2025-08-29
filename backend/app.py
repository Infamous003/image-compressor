from fastapi import FastAPI, File, UploadFile
from enum import Enum
import shutil
from .tasks import create_thumbnail_task, resize_image_task, transform_image_task, celery_app
from celery.result import AsyncResult

class ImageModes(str, Enum):
    BW = "1"
    GRAYSCALE = "L"
    P = "P"

app = FastAPI()

@app.get("/")
def home():
    return {"what's up": "danger!"}

@app.post("/thumbnail", description="Create a thumbnail, maintaining the aspect ratio")
def create_thumbnail(file: UploadFile = File(),
                     width: int = 128,
                     height: int = 128):
    filepath = f"uploads/{file.filename}"

    # saving the file to /uploads/ directory
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = create_thumbnail_task.delay(filepath, width, height)
    return {"task_id": task.id, "status": "PENDING"}


@app.post("/resize", description="Resize the image, ignoring the aspect ratio")
def resize_image(width: int,
                 height: int,
                 file: UploadFile = File()):
    filepath = f"uploads/{file.filename}"
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = resize_image_task.delay(filepath, width, height)
    return {"task_id": task.id, "status": "PENDING"}

@app.post("/transform", description="Resize the image, ignoring the aspect ratio")
def transform_image(mode: ImageModes,
                    file: UploadFile = File()):

    filepath = f"uploads/{file.filename}"
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = transform_image_task.delay(filepath, mode)
    return {"task_id": task.id, "status": "PENDING"}


@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    result = None
    if task_result.successful():
        result = task_result.result

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": result
    }