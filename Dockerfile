FROM ghcr.io/astral-sh/uv:python3.13-alpine

ARG CODE_DIR
WORKDIR ${CODE_DIR}

COPY pyproject.toml uv.lock ${CODE_DIR}/
RUN uv sync --locked --no-python-downloads

ARG USER=djangouser
ARG UGROUP=djangogroup

# activate venv by adding it first in path
ENV VIRTUAL_ENV=${CODE_DIR}/.venv STATICFILES_DIR=${CODE_DIR}/staticfiles MEDIAFILES_DIR=${CODE_DIR}/mediafiles LOGS_DIR=${CODE_DIR}/logs
ENV PATH="$VIRTUAL_ENV/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN addgroup -S ${UGROUP} && adduser -S ${USER} -G ${UGROUP} && mkdir app staticfiles mediafiles logs && chown -R ${USER}:${UGROUP} staticfiles mediafiles logs
COPY ./backend ./app

USER ${USER}
WORKDIR ${CODE_DIR}/app

# entry point used for DB and other services to boot up
# ENTRYPOINT [ "executable" ]
