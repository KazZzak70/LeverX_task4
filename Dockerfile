FROM python:3.8.12-slim

WORKDIR /usr/src/app

ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update \
    && apt-get install postgresql gcc python3-dev musl-dev netcat -y

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .