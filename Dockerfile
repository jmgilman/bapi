FROM python:3.8-alpine

ENV BAPI_WORK_DIR="/run/beancount"
ENV HOST=0.0.0.0
ENV PORT=8080

WORKDIR /run

RUN apk --update add --no-cache build-base libffi-dev libxml2-dev libxslt-dev && \
    pip3 install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml /run
COPY poetry.lock /run

RUN mkdir /run/app && \
    mkdir /run/beancount && \
    poetry install --no-dev && \
    apk del build-base libffi-dev && \
    rm -rf /root/.cache

RUN addgroup --system user && \
    adduser --system --ingroup user --home /home/user user && \
    chown -R user:user ${BAPI_WORK_DIR}

COPY /app /run/app
USER user

CMD uvicorn app.main:app --host $HOST --port $PORT