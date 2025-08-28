from celery import Celery
from PIL import Image
import os
from time import sleep

app = Celery("tasks", broker="redis://localhost")

@app.task
def greet():
    sleep(3)
    return "What's up!?"

@app.task
def create_thumbnail_task(filepath, w, h):
    sleep(4)
    img = Image.open(filepath)
    img.thumbnail((w, h))

    # inc filepath is 'uploads/img1.jpg' and basename extracts the last part of the path
    filename = os.path.basename(filepath)
    # so, 'img1.png' is split into img1 and .png
    name, ext = os.path.splitext(filename)

    output_path = f"results/{name}_thumb{ext}"
    img.save(output_path)

    return output_path

@app.task
def resize_image_task(filepath, w, h):
    img = Image.open(filepath)
    new_img = img.resize((w, h))

    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)

    output_path = f"results/{name}_thumb{ext}"
    new_img.save(output_path)

    return output_path

@app.task
def transform_image_task(filepath, mode):
    img = Image.open(filepath)
    new_img = img.convert(mode)

    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)

    output_path = f"results/{name}_thumb{ext}"
    new_img.save(output_path)

    return output_path