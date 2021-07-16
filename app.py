import time
import json

from flask import Flask, request
from .object_detect import ObjectDetect

labels_file = "models/coco_labels.txt"
model_file = "models/detect.tflite"

object_detector = ObjectDetect(labels_file, model_file)

app = Flask(__name__)
app.debug = True


@app.route('/detect', methods=["POST"])
def detect_object():
    file = request.files['image']
    start_time = time.monotonic()
    results = object_detector.predict(file)
    elapsed_ms = (time.monotonic() - start_time) * 1000
    return {
        "predictions": results,
        "elapsed_ms": elapsed_ms
    }

