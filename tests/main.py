from libre_chat.chat_endpoint import ChatEndpoint
from libre_chat.llm import Llm
from libre_chat.utils import parse_config

# Run default model, used in docker container
# Config is retrieved from env variables

conf = parse_config("chat.yml")
# conf = parse_config("tests/llm-with-vectorstore.yml")
llm = Llm(conf=conf)
app = ChatEndpoint(llm=llm, conf=conf)
