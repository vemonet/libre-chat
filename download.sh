# https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML
mkdir -p models
cd models
wget -N https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q3_K_L.bin
cd ..

# https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/
mkdir -p embeddings
cd embeddings
wget -N https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip
unzip -d all-MiniLM-L6-v2 all-MiniLM-L6-v2.zip
cd ..
