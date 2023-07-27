from libre_llm.llm import Llm
from libre_llm.llm_endpoint import LlmEndpoint

# Run default model, used in docker container
# Config is retrieved from env variables

# llm = Llm(vector_path=None)
llm = Llm()
app = LlmEndpoint(llm=llm)
