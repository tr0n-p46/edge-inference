# syntax=docker/dockerfile:1
FROM python:3.7-buster
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt
RUN pip3 install --index-url https://google-coral.github.io/py-repo/ tflite_runtime
EXPOSE 5000
CMD ["flask", "run"]