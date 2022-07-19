FROM python:3.10.5

WORKDIR /app

COPY /requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1



