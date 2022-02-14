FROM python:3.10-slim-bullseye

# Update and install Beancount/aiohttp
RUN apt-get update \
    && apt-get install --no-install-recommends -y build-essential curl \
    && pip install -U pip \
    && pip install beancount aiohttp

RUN mkdir -p /static
COPY app.py /run/app.py

ENTRYPOINT [ "/usr/local/bin/python", "/run/app.py" ]