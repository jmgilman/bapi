# ----- BASE ----- #
FROM python:3.10-slim-bullseye as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.12 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

ENV BAPI_WORK_DIR /beancount
ENV BAPI_ENTRYPOINT main.beancount

FROM python-base as builder-base

# Update and install pre-requisites
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

# Install runtime deps
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev

# ----- DEV ----- #
FROM python-base as development

ENV FASTAPI_ENV=development

# Copy poetry and runtime deps
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Copy entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Install dev deps
WORKDIR $PYSETUP_PATH
RUN poetry install

# Copy app
COPY ./app /run/app
WORKDIR /run

# Setup work directory
RUN mkdir -p ${BAPI_WORK_DIR}

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "main:app"]

# ----- PROD ----- #
FROM python-base as production
ENV FASTAPI_ENV=production

# Add non-root user
RUN addgroup --system app && adduser --system --group app

# Copy poetry and runtime deps
COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY ./gunicorn_conf.py /gunicorn_conf.py

# Copy entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copy app
COPY ./app /run/app
WORKDIR /run

# Setup work directory
RUN mkdir -p ${BAPI_WORK_DIR}
RUN chown -R app:app ${BAPI_WORK_DIR}

USER app

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--config /gunicorn_conf.py", "app.main:app" ]