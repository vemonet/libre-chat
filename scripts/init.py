import logging

from libre_chat.conf import parse_conf
from libre_chat.llm import Llm

# Initialize the Llm (pre-download files if not present, build the vectorstore)
# Runs before the API to avoid running on multiple workers

logging.basicConfig(level=logging.getLevelName("INFO"))

# TODO: take conf as arg?
conf = parse_conf("chat.yml")
llm = Llm(conf=conf)
