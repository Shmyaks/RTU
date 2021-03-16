FROM python:3.9.2-alpine3.13 

RUN mkdir -p /usr/src/app
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt