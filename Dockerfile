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
RUN pip install coverage

# Run tests
RUN chmod 755 e2e/entrypoint.sh
RUN bash e2e/entrypoint.sh
