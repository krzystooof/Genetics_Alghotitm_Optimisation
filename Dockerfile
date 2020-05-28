FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/app

RUN mkdir /app
COPY . /app/

# Install octave with ga package
RUN apt-get update
RUN apt-get -y install octave
RUN apt-get install octave-ga
RUN pip install coverage
# Run e2e tests
WORKDIR /app/tests/e2e
RUN chmod 755 entrypoint.sh
RUN bash entrypoint.sh
# Run unit tests

### Uncomment this, when propper unit test are delivered ###
#WORKDIR /app/tests/unit
#RUN python -m coverage run -m unittest discover
#RUN python -m coverage report
