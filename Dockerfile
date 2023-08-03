ARG BASE_IMAGE=python:3.11
# ARG BASE_IMAGE=nvcr.io/nvidia/pytorch:23.06-py3
# cf. https://ngc.nvidia.com/catalog/containers/nvidia:pytorch

FROM ${BASE_IMAGE}

ENV LIBRECHAT_WORKERS=8

RUN pip install --upgrade pip

# Pre-download embeddings in /data
WORKDIR /data/embeddings
RUN wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip && \
    unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip && \
    rm all-MiniLM-L6-v2.zip

# Install app in /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
RUN pip install -e .

WORKDIR /data

ENTRYPOINT [ "/app/scripts/start.sh" ]
