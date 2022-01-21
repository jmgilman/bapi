FROM python:3.8

ENV BAPI_WORK_DIR="/run/beancount"
ENV HOST=0.0.0.0
ENV PORT=8080

RUN mkdir /run/app
RUN mkdir /run/beancount

COPY /app /run/app
COPY pyproject.toml /run 

WORKDIR /run
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD uvicorn app.main:app --host $HOST --port $PORT