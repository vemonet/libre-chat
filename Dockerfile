ARG BASE_IMAGE=python:3.11
# ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3
# cf. https://ngc.nvidia.com/catalog/containers/nvidia:pytorch

FROM ${BASE_IMAGE}

WORKDIR /app

RUN pip install --upgrade pip

ADD tests/download.sh ./download.sh

RUN ./download.sh && \
    rm download.sh

ADD . .

RUN pip install -e .

ENV LIBRECHAT_WORKERS=8

ENTRYPOINT [ "gunicorn", "tests.main:app", "-w", "$LIBRECHAT_WORKERS", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]
# ENTRYPOINT [ "uvicorn", "tests.main:app", "--host", "0.0.0.0" ]
