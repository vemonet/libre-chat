#!/bin/bash

# Use this script to quickly download the default model and embeddings

# https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/
mkdir -p embeddings
cd embeddings
wget -N https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip
rm all-MiniLM-L6-v2.zip
cd ..

# https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
mkdir -p models
cd models
wget -N https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin

# 3rd largest 70B q5:
# wget -N https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGML/resolve/main/llama-2-70b-chat.ggmlv3.q5_K_M.bin

# 2nd largest 70B q6 in 2 files:
# wget -N https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGML/resolve/main/llama-2-70b-chat.ggmlv3.q6_K.z01
# wget -N https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGML/resolve/main/llama-2-70b-chat.ggmlv3.q6_K.zip
# cat llama-2-70b-chat.ggmlv3.q6_K*  >llama-2-70b-chat.ggmlv3.q6.zip
# unzip -d llama-2-70b-chat.ggmlv3.q6.zip
cd ..
