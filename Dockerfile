FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
RUN apt-get update
RUN apt-get install octave
WORKDIR /app

COPY . /app/

