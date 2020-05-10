FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/app

RUN mkdir /app
COPY . /app/
# Set tests as workdir
WORKDIR /app/tests

# Install octave with ga package
RUN apt-get update
RUN apt-get -y install octave
RUN apt-get install octave-ga

# Run tests
RUN chmod 755 entrypoint.sh
RUN bash entrypoint.sh
