FROM python:3

RUN apt update && apt install -y ffmpeg

COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app/

COPY ./main.py .
