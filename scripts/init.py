import logging
import os
import shutil

from libre_chat import log, parse_conf

# from libre_chat.vectorstore import build_vectorstore

# Initialize the Llm at docker run (pre-download files if not present, build the vectorstore)
# Runs before the API to avoid running on multiple workers

logging.basicConfig(level=logging.getLevelName("INFO"))

log.info("🚀 Initializing the Llm: download files if not present, build vectorstore")

# TODO: take conf as arg?
conf = parse_conf("chat.yml")

default_model = "mixtral-8x7b-instruct-v0.1.Q2_K.gguf"
default_embeddings = "all-MiniLM-L6-v2"
default_document = "drug_repositioning_for_alzheimer_disease.pdf"

# Put the default 7B model in /data if not present
if not os.path.exists(conf.llm.model_path) and conf.llm.model_path.endswith(default_model):
    try:
        log.info("Initializing default model from docker image")
        shutil.move(f"/app/models/{default_model}", conf.llm.model_path)
    except Exception as e:
        log.info(f"Could not initialize default model from docker image: {e}")

if not os.path.exists(conf.vector.embeddings_path) and conf.vector.embeddings_path.endswith(
    default_embeddings
):
    try:
        log.info("Initializing default embeddings from docker image")
        shutil.move(f"/app/embeddings/{default_embeddings}", conf.vector.embeddings_path)
    except Exception as e:
        log.info(f"Could not initialize default embeddings from docker image: {e}")

# if len(os.listdir(conf.vector.documents_path)) < 1:
#     # If no docs we add a default one to enable building the vectorstore
#     shutil.copy(f"/app/documents/{default_document}", conf.vector.documents_path)

# build_vectorstore(conf)

# llm = Llm(conf=conf)
