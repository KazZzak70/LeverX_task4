FROM python:3.8.12-slim

WORKDIR /home/user/PycharmProjects/LeverX_task4

ENV PYTHONDOWNWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apt-get update \
    && apt-get install postgresql gcc python3-dev musl-dev netcat -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .

COPY . .

ENTRYPOINT ["/home/user/PycharmProjects/LeverX_task4/entrypoint.sh"]