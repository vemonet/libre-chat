mkdir -p data

# https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
mkdir -p models
cd models
wget -N https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin
cd ..

mkdir -p vectorstore/db_faiss
cd vectorstore/db_faiss
wget -N https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference/raw/b95e89aa56cf66e7d6b5e48bc17205ba1f5a7fa9/vectorstore/db_faiss/index.faiss
wget -N https://github.com/kennethleungty/Llama-2-Open-Source-LLM-CPU-Inference/raw/b95e89aa56cf66e7d6b5e48bc17205ba1f5a7fa9/vectorstore/db_faiss/index.pkl
cd ..

# https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/
mkdir -p embeddings
cd embeddings
wget -N https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip
