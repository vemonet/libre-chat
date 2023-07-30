import logging

from libre_chat.chat_conf import parse_config
from libre_chat.chat_endpoint import ChatEndpoint
from libre_chat.llm import Llm

# Run default config, used in docker container

logging.basicConfig(level=logging.getLevelName("INFO"))

conf = parse_config("chat.yml")
# conf = parse_config("config/chat-vectorstore-qa.yml")
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf)
