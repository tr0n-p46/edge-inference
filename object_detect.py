import re
import numpy as np
import json

from PIL import Image
from tflite_runtime.interpreter import Interpreter


def load_labels(labels_file):
    """Loads the labels file. Supports files with or without index numbers."""
    with open(labels_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        labels = {}
        for row_number, content in enumerate(lines):
            pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
            if len(pair) == 2 and pair[0].strip().isdigit():
                labels[int(pair[0])] = pair[1].strip()
            else:
                labels[row_number] = pair[0].strip()
    return labels


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class ObjectDetect:
    def __init__(self, labels_file, model_file):
        self.labels = load_labels(labels_file)
        self.interpreter = Interpreter(model_file)
        self.interpreter.allocate_tensors()

    def get_dims(self):
        _, input_height, input_width, _ = self.interpreter.get_input_details()[0]['shape']
        return input_width, input_height

    def set_input_tensor(self, image):
        """Sets the input tensor."""
        tensor_index = self.interpreter.get_input_details()[0]['index']
        input_tensor = self.interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def get_output_tensor(self, index):
        """Returns the output tensor at the given index."""
        output_details = self.interpreter.get_output_details()[index]
        tensor = np.squeeze(self.interpreter.get_tensor(output_details['index']))
        return tensor

    def detect_objects(self, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(image)
        self.interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(0)
        classes = self.get_output_tensor(1)
        scores = self.get_output_tensor(2)
        count = int(self.get_output_tensor(3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results

    def predict(self, image):
        image = Image.open(image).convert('RGB').resize(self.get_dims(), Image.ANTIALIAS)
        results = self.detect_objects(image, 0.4)
        predictions = []
        for obj in results:
            res = {
                'label': self.labels[int(obj['class_id'].tolist())],
                'score': str(obj['score'].tolist() * 100) + "%"
            }
            predictions.append(res)
        return predictions






