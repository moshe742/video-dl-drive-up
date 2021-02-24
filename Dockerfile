FROM python:3

COPY requirements.txt ./
RUN pip install -r requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app/

COPY ./main.py .
