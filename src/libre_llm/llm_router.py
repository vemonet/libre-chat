from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, Body

from libre_llm.utils import Prompt, defaults

__all__ = [
    "LlmRouter",
]

api_responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = {
    200: {
        "description": "SPARQL query results",
        "content": {
            "application/sparql-results+json": {
                "results": {"bindings": []},
                "head": {"vars": []},
            },
            "application/json": {
                "results": {"bindings": []},
                "head": {"vars": []},
            },
            "text/csv": {"example": "s,p,o"},
            "application/sparql-results+csv": {"example": "s,p,o"},
            "text/turtle": {"example": "service description"},
            "application/sparql-results+xml": {"example": "<root></root>"},
            "application/xml": {"example": "<root></root>"},
            # "application/rdf+xml": {
            #     "example": '<?xml version="1.0" encoding="UTF-8"?> <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:RDF>'
            # },
        },
    },
    400: {
        "description": "Bad Request",
    },
    403: {
        "description": "Forbidden",
    },
    422: {
        "description": "Unprocessable Entity",
    },
}


class LlmRouter(APIRouter):
    """
    Class to deploy a LLM router with FastAPI.
    """

    def __init__(
        self,
        *args: Any,
        llm: Any,
        path: str = "/",
        title: str = defaults.title,
        description: str = defaults.description,
        version: str = defaults.version,
        public_url: str = "https://your-endpoint/sparql",
        favicon: str = defaults.favicon,
        examples: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Constructor of the SPARQL endpoint, everything happens here.
        FastAPI calls are defined in this constructor
        """
        self.llm = llm
        self.title = title
        self.description = description
        self.version = version
        self.path = path
        self.favicon = favicon
        self.examples = examples if examples else [defaults.example_prompt]
        if len(self.examples) < 1:
            self.examples.append(defaults.example_prompt)
        example_prompt = {"prompt": self.examples[0]}

        # Instantiate APIRouter
        super().__init__(
            *args,
            # responses=api_responses,
            **kwargs,
        )

        @self.post("/prompt", description=self.description, response_description="Prompt response", response_model={})
        def send_prompt(
            prompt: Prompt = Body(..., example=example_prompt),
        ) -> List[Tuple[str, str]]:
            return self.llm.query(prompt.prompt)
