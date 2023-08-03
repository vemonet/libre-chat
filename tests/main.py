import logging

from libre_chat.chat_conf import parse_conf
from libre_chat.chat_endpoint import ChatEndpoint
from libre_chat.llm import Llm

# STart the API endpoint, used in docker container and tests

logging.basicConfig(level=logging.getLevelName("INFO"))

conf = parse_conf("chat.yml")
# conf = parse_conf("config/chat-vectorstore-qa.yml")
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf)
