import typer
import uvicorn

from libre_llm import __version__
from libre_llm.llm import Llm
from libre_llm.llm_endpoint import LlmEndpoint
from libre_llm.utils import parse_config, settings

cli = typer.Typer(help="Deploy API and web UI for LLMs, such as llama2, using langchain.")


@cli.command("start")
def start(
    config: str = typer.Option(settings.llm.model_path, help="Path to the libre-llm YAML config file, usually llm.yml"),
    # model: str = typer.Option(settings.llm.model_path, help="Path to the model binary"),
    # vector: str = typer.Option(settings.vector.vector_path, help="Path to the vector db folder"),
    host: str = typer.Option("localhost", help="Host URL"),
    port: int = typer.Option(8000, help="URL port"),
    workers: int = typer.Option(1, help="Number of workers"),
    debug: bool = typer.Option(True, help="Display debug logs"),
) -> None:
    if config:
        settings = parse_config(config)
    llm = Llm(
        model_path=settings.llm.model_path,
        model_type=settings.llm.model_type,
        model_download=settings.llm.model_download,
        embeddings_path=settings.vector.embeddings_path,
        embeddings_download=settings.vector.embeddings_download,
        vector_path=settings.vector.vector_path,
        vector_download=settings.vector.vector_download,
        documents_path=settings.vector.documents_path,
        max_new_tokens=settings.llm.max_new_tokens,
        temperature=settings.llm.temperature,
        return_source_documents=settings.vector.return_source_documents,
        vector_count=settings.vector.vector_count,
        chunk_size=settings.vector.chunk_size,
        chunk_overlap=settings.vector.chunk_overlap,
        template_variables=settings.template.variables,
        template_prompt=settings.template.prompt,
    )
    app = LlmEndpoint(llm=llm, settings=settings)
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level="debug" if debug else "info",
        workers=workers,
    )


@cli.command("build")
def build(
    model: str = typer.Option(settings.llm.model_path, help="Path to the model binary"),
    vector: str = typer.Option(settings.vector.vector_path, help="Path to the vector db folder"),
    data: str = typer.Option(settings.vector.documents_path, help="Path to the data folder to vectorize"),
    debug: bool = typer.Option(True, help="Display debug logs"),
) -> None:
    print(f"Vectorizing documents from {data} to the vector db {vector}")
    llm = Llm(model_path=model, vector_path=vector, documents_path=data)
    vector_path = llm.build_vector_db()
    print(f"Data vectorized in {vector_path}")


@cli.command("version")
def version() -> None:
    print(__version__)


if __name__ == "__main__":
    cli()
