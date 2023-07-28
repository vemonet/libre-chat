from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, Body, Request, Response

from libre_llm.utils import Prompt, Settings, settings

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


@dataclass
class PromptResponse:
    result: str
    source_documents: Optional[List[Dict]] = None


class LlmRouter(APIRouter):
    """
    Class to deploy a LLM router with FastAPI.
    """

    def __init__(
        self,
        *args: Any,
        path: str = "/prompt",
        llm: Any,
        settings: Settings = settings,
        examples: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Constructor of the LLM API router with the actual calls
        """
        self.path = path
        self.llm = llm
        self.settings = settings
        self.title = self.settings.info.title
        self.description = self.settings.info.description
        self.version = self.settings.info.version
        self.examples = examples if examples else self.settings.info.examples
        example_post = {"prompt": self.examples[0]}

        # Instantiate APIRouter
        super().__init__(
            *args,
            # responses=api_responses,
            **kwargs,
        )

        @self.get(
            self.path,
            name="Prompt the LLM",
            description=self.description,
            response_model=PromptResponse,
        )
        def get_prompt(request: Request, prompt: str = self.examples[0]) -> Response:
            """Send a prompt to the chatbot through HTTP GET operation.

            :param request: The HTTP GET request with a .body()
            :param prompt: Prompt to send to the LLM
            """
            return self.llm.query(prompt)

        @self.post(
            self.path,
            name="Prompt the LLM",
            description=self.description,
            response_description="Prompt response",
            response_model=PromptResponse,
        )
        def post_prompt(
            request: Request,
            prompt: Prompt = Body(..., example=example_post),
        ) -> List[Tuple[str, str]]:
            """Send a prompt to the chatbot through HTTP POST operation.

            :param request: The HTTP POST request with a .body()
            :param prompt: Prompt to send to the LLM.
            """
            return get_prompt(request, prompt.prompt)
