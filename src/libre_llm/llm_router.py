from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, Body

from libre_llm.utils import Prompt, settings

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
    source_documents: Optional[List[Dict]]


class LlmRouter(APIRouter):
    """
    Class to deploy a LLM router with FastAPI.
    """

    def __init__(
        self,
        *args: Any,
        llm: Any,
        path: str = "/",
        title: str = settings.info.title,
        description: str = settings.info.description,
        version: str = settings.info.version,
        public_url: str = settings.info.public_url,
        favicon: str = settings.info.favicon,
        examples: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Constructor of the LLM API router with the actual calls
        """
        self.llm = llm
        self.title = title
        self.description = description
        self.version = version
        self.path = path
        self.favicon = favicon
        self.examples = examples if examples else [settings.info.example_prompt]
        if len(self.examples) < 1:
            self.examples.append(settings.info.example_prompt)
        example_prompt = {"prompt": self.examples[0]}

        # Instantiate APIRouter
        super().__init__(
            *args,
            # responses=api_responses,
            **kwargs,
        )

        @self.post(
            "/prompt",
            description=self.description,
            response_description="Prompt response",
            response_model=PromptResponse,
        )
        def send_prompt(
            prompt: Prompt = Body(..., example=example_prompt),
        ) -> List[Tuple[str, str]]:
            return self.llm.query(prompt.prompt)
