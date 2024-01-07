#!/bin/bash

# Use this script to quickly download the default model and embeddings

# https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/
mkdir -p embeddings
cd embeddings
wget -N https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip
rm all-MiniLM-L6-v2.zip
cd ..

mkdir -p models
cd models
wget -N https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF/resolve/main/mixtral-8x7b-instruct-v0.1.Q2_K.gguf

cd ..
