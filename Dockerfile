FROM python:3.7-alpine

ENV FLASK_APP app/app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV=development
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN apk add build-base libffi-dev
RUN pip install -r requirements.txt