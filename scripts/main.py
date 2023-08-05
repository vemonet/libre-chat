import logging

from libre_chat.conf import parse_conf
from libre_chat.endpoint import ChatEndpoint
from libre_chat.llm import Llm

# Start the API endpoint, used in docker container and dev scripts

logging.basicConfig(level=logging.getLevelName("INFO"))

conf = parse_conf("chat.yml")
# conf = parse_conf("config/chat-vectorstore-qa.yml")
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf)
