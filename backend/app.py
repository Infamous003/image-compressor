from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
import os
from PIL import Image, ImageOps
from io import BytesIO
from enum import Enum

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
def create_thumbnail(file: UploadFile = File(), width: int = 128, height: int = 128):
    img = Image.open(file.file)
    new_img = img.copy()
    size = (width, height)
    new_img.thumbnail(size)

    # Putting the img in the buffer(memory)
    buffer = BytesIO()
    new_img.save(buffer, format="PNG")

    # bringing back the cursor to the start of the file
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

@app.post("/resize", description="Resize the image, ignoring the aspect ratio")
def resize_image(width: int,
                 height: int,
                 file: UploadFile = File()):
    img = Image.open(file.file)

    size = (width, height)
    new_img = img.resize(size)

    buffer = BytesIO()
    new_img.save(buffer, format="PNG")

    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")

@app.post("/transform", description="Resize the image, ignoring the aspect ratio")
def transform_image(mode: ImageModes,
                    file: UploadFile = File()):
    img = Image.open(file.file)

    new_img = img.convert(mode)

    buffer = BytesIO()
    new_img.save(buffer, format="PNG")

    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

