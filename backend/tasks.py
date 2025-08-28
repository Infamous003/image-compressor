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