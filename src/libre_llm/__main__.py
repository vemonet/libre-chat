import typer
import uvicorn

cli = typer.Typer(help="Deploy API and web UI for LLMs, such as llama2, using langchain.")


@cli.command()
def cli_api(
    host: str = typer.Option("localhost", help="Host URL"),
    port: int = typer.Option(8000, help="URL port"),
    workers: int = typer.Option(1, help="Number of workers"),
    debug: bool = typer.Option(True, help="Display debug logs"),
) -> None:
    uvicorn.run(
        "libre_llm.api:app",
        host=host,
        port=port,
        reload=False,
        log_level="debug" if debug else "info",
        workers=workers,
        # limit_concurrency=workers,
        # limit_max_requests=workers,
    )


if __name__ == "__main__":
    cli()
