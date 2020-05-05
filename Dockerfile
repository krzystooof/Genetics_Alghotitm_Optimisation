FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
COPY . /app/
# Set tests as workdir
WORKDIR /app/pyb/src/tests

# Install octave with ga package
RUN apt-get update
RUN apt-get -y install octave
RUN apt-get install octave-ga

# Run tests
RUN sed -i -e 's/\r$//' entrypoint.sh
CMD ["bash", "entrypoint.sh"]

