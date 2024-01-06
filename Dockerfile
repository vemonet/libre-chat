ARG BASE_IMAGE=python:3.11

FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive
ARG GPU_ENABLED=false
ENV LIBRECHAT_WORKERS=1

RUN apt-get update && \
    apt-get install -y software-properties-common git vim build-essential python3-dev wget unzip && \
    pip3 install --upgrade pip


# # Pre-download embeddings in /data
# WORKDIR /app/embeddings
# RUN wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip && \
#     unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip && \
#     rm all-MiniLM-L6-v2.zip

# WORKDIR /app/models
# RUN wget https://huggingface.co/TheBloke/Mixtral-8x7B-v0.1-GGUF/resolve/main/mixtral-8x7b-v0.1.Q2_K.gguf

# Install app in /app
WORKDIR /app

# Pre-install requirements to use cache when re-building
ADD scripts/requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm requirements.txt

ADD . .
RUN bash -c "if [ $GPU_ENABLED == 'true' ] ; then pip install .[gpu] ; else pip install . ; fi"

# We use /data as workdir for models, embeddings, vectorstore
WORKDIR /data

VOLUME [ "/data" ]

ENTRYPOINT [ "/app/scripts/start.sh" ]
