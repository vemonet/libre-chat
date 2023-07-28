from libre_llm.llm import Llm
from libre_llm.llm_endpoint import LlmEndpoint
from libre_llm.utils import parse_config

# Run default model, used in docker container
# Config is retrieved from env variables

conf = parse_config("llm.yml")
# conf = parse_config("tests/llm-with-vectorstore.yml")
llm = Llm(conf=conf)
app = LlmEndpoint(llm=llm, conf=conf)
