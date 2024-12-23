FROM python:3.10

WORKDIR /app


COPY ["./.env", "./requirements.txt", "./"]
COPY ./core /app/core

ENV PYTHONPATH=/app

COPY ./http_ca.crt /usr/local/share/ca-certificates/http_ca.crt
RUN update-ca-certificates

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
