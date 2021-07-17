import time

from flask import Flask, request
from .backend import FaceRecognition

tmp_image_path = "/tmp/image.jpg"
models_path = "models/"
images_path = "images/"


recognizer = FaceRecognition(models_path, images_path)
app = Flask(__name__)


@app.route('/recognize', methods=["POST"])
def detect_object():
    file = request.files['image']
    file.save(tmp_image_path)
    start_time = time.monotonic()
    results = recognizer.predict(tmp_image_path)
    elapsed_ms = (time.monotonic() - start_time) * 1000
    return {
        "predictions": results,
        "elapsed_ms": elapsed_ms
    }

