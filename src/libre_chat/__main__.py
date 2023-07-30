import logging
import shutil
from typing import Optional

import typer
import uvicorn

from libre_chat import __version__
from libre_chat.chat_conf import default_conf, parse_config
from libre_chat.chat_endpoint import ChatEndpoint
from libre_chat.llm import Llm
from libre_chat.utils import BOLD, END, log, log_format

cli = typer.Typer(help="Deploy API and web UI for LLMs, such as Llama 2, using langchain.")


@cli.command("start")
def start(
    config: str = typer.Argument(default_conf.config_path, help="Path to the libre-chat YAML configuration file"),
    # model: str = typer.Option(conf.llm.model_path, help="Path to the model binary"),
    # vector: str = typer.Option(conf.vector.vector_path, help="Path to the vector db folder"),
    host: str = typer.Option("localhost", help="Host URL"),
    port: int = typer.Option(8000, help="URL port"),
    workers: int = typer.Option(1, help="Number of workers"),
    log_level: str = typer.Option("info", help="Log level (info, debug, warn, error)"),
) -> None:
    logging.basicConfig(level=logging.getLevelName(log_level.upper()))
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = log_format
    log_config["formatters"]["default"]["fmt"] = log_format

    conf = parse_config(config)
    llm = Llm(conf=conf)
    app = ChatEndpoint(llm=llm, conf=conf)
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level=log_level,
        workers=workers,
        # log_config=log_config,
    )


@cli.command("build")
def build(
    config: str = typer.Argument(default_conf.config_path, help="Path to the libre-chat YAML configuration file"),
    vector: Optional[str] = typer.Option(None, help="Path to the vector db folder"),
    documents: Optional[str] = typer.Option(None, help="Path to the folder containing documents to vectorize"),
    log_level: str = typer.Option("info", help="Log level (info, debug, warn, error)"),
) -> None:
    logging.basicConfig(level=logging.getLevelName(log_level.upper()))
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = log_format
    log_config["formatters"]["default"]["fmt"] = log_format

    conf = parse_config(config)
    if vector:
        conf.vector.vector_path = vector
    if documents:
        conf.vector.documents_path = documents
    log.info(f"Vectorizing documents from {BOLD}{documents}{END} as vectorstore in {conf.vector.vector_path}")
    shutil.rmtree(conf.vector.vector_path)
    llm = Llm(conf=conf)
    llm.build_vectorstore()
    log.info(f"Documents successfully vectorized in {BOLD}{conf.vector.vector_path}{END}")


@cli.command("version")
def version() -> None:
    print(__version__)


if __name__ == "__main__":
    cli()
