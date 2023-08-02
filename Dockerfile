ARG BASE_IMAGE=python:3.11
# ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3
# cf. https://ngc.nvidia.com/catalog/containers/nvidia:pytorch

FROM ${BASE_IMAGE}

ENV LIBRECHAT_WORKERS=8

WORKDIR /app

RUN pip install --upgrade pip

ADD scripts/download.sh ./download.sh
RUN ./download.sh && \
    rm download.sh

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
RUN pip install -e .

ENTRYPOINT [ "/app/scripts/start.sh" ]
