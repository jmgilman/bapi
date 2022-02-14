FROM python:3.10-slim-bullseye

ENV BEANFILE beancount/main.beancount
ENV PICKLE 0
ENV HOSTNAME redis
ENV KEY beancount

# Update and install Redis/bdantic packages
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential \
    && pip install -U pip \
    && pip install redis bdantic loguru requests

COPY migration.py /run/migration.py

ENTRYPOINT [ "/usr/local/bin/python", "/run/migration.py" ]