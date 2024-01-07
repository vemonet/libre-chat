ARG BASE_IMAGE=nvcr.io/nvidia/cuda:12.1.0-runtime-ubuntu22.04

# ARG BASE_IMAGE=python:3.11
# 2.7GB cf. https://ngc.nvidia.com/catalog/containers/nvidia:cuda
# ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3
# 8.5GB cf. https://ngc.nvidia.com/catalog/containers/nvidia:pytorch

# CUDA image: https://github.com/oobabooga/text-generation-webui/blob/main/docker/Dockerfile

FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
ENV LIBRECHAT_WORKERS=1

# CUDA image requires to install python
RUN apt-get update && \
    apt-get install -y software-properties-common git vim build-essential python3-dev wget unzip && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py && \
    pip3 install --upgrade pip

# Install app in /app
WORKDIR /app

# Pre-install requirements to use cache when re-building
ADD scripts/requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

ADD . .
RUN pip3 install -e .[gpu]

# We use /data as workdir for models, embeddings, vectorstore
WORKDIR /data

VOLUME [ "/data" ]

ENTRYPOINT [ "/app/scripts/start.sh" ]
