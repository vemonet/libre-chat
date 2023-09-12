ARG BASE_IMAGE=python:3.11
# ARG BASE_IMAGE=nvcr.io/nvidia/cuda:12.2.0-devel-ubuntu20.04
# 2.7GB cf. https://ngc.nvidia.com/catalog/containers/nvidia:cuda
# ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3
# 8.5GB cf. https://ngc.nvidia.com/catalog/containers/nvidia:pytorch

FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
ARG GPU_ENABLED=false
ENV LIBRECHAT_WORKERS=1

# CUDA image required to install python
RUN apt-get update && \
    apt-get install -y software-properties-common wget unzip && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y python3.11 && \
    ln -s /usr/bin/python3.11 /usr/bin/python && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    pip install --upgrade pip



# Pre-download embeddings in /data
WORKDIR /app/embeddings
RUN wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip && \
    unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip && \
    rm all-MiniLM-L6-v2.zip

# WORKDIR /app/models
# RUN wget https://huggingface.co/TheBloke/LLaMa-7B-GGML/resolve/main/llama-7b.ggmlv3.q3_K_L.bin

# Install app in /app
WORKDIR /app

# Pre-install requirements to use cache when re-building
ADD scripts/requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt

ADD . .
RUN bash -c "if [ $GPU_ENABLED == 'true' ] ; then pip install .[gpu] ; else pip install . ; fi"

# We use /data as workdir for models, embeddings, vectorstore
WORKDIR /data

VOLUME [ "/data" ]

ENTRYPOINT [ "/app/scripts/start.sh" ]
