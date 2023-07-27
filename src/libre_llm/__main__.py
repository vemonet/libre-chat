import typer
import uvicorn

from libre_llm import __version__
from libre_llm.llm import Llm
from libre_llm.llm_endpoint import LlmEndpoint
from libre_llm.utils import settings

cli = typer.Typer(help="Deploy API and web UI for LLMs, such as llama2, using langchain.")


@cli.command("start")
def start(
    model: str = typer.Option(settings.model_path, help="Path to the model binary"),
    vector: str = typer.Option(settings.vector_path, help="Path to the vector db folder"),
    host: str = typer.Option("localhost", help="Host URL"),
    port: int = typer.Option(8000, help="URL port"),
    workers: int = typer.Option(1, help="Number of workers"),
    debug: bool = typer.Option(True, help="Display debug logs"),
) -> None:
    print(f"Starting LLM from model {model}, and vector db {vector}")
    llm = Llm(model_path=model, vector_path=vector)
    app = LlmEndpoint(llm=llm)
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
    model: str = typer.Option(settings.model_path, help="Path to the model binary"),
    vector: str = typer.Option(settings.vector_path, help="Path to the vector db folder"),
    data: str = typer.Option(settings.data_path, help="Path to the data folder to vectorize"),
    debug: bool = typer.Option(True, help="Display debug logs"),
) -> None:
    print(f"Vectorizing documents from {data} to the vector db {vector}")
    llm = Llm(model_path=model, vector_path=vector, data_path=data)
    vector_path = llm.build_vector_db()
    print(f"Data vectorized in {vector_path}")


@cli.command("version")
def version() -> None:
    print(__version__)


if __name__ == "__main__":
    cli()
