FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
RUN apt-get update
RUN apt-get -y install octave
RUN apt-get install octave-ga

WORKDIR /app

COPY . /app/
RUN sed -i -e 's/\r$//' pyb/src/tests/run_test.sh


