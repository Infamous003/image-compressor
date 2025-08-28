from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
from enum import Enum
import shutil
from .tasks import create_thumbnail_task, resize_image_task, transform_image_task

class ImageModes(str, Enum):
    BW = "1"
    GRAYSCALE = "L"
    P = "P"

class CompressModes(int, Enum):
    LOW = 85
    MEDIUM = 70
    HIGH = 50

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