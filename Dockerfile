ARG BASE_IMAGE=python:3.11
# ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3
# cf. https://ngc.nvidia.com/catalog/containers/nvidia:pytorch

FROM ${BASE_IMAGE}

ENV LIBRECHAT_WORKERS=8

RUN pip install --upgrade pip

# Add config, models, vectorstore to /data
WORKDIR /data

ADD scripts/download.sh ./download.sh
RUN ./download.sh && \
    rm download.sh

# Install app in /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
RUN pip install -e .

WORKDIR /data

ENTRYPOINT [ "/app/scripts/start.sh" ]
