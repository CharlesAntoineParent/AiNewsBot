"""ainewsbot REST API."""

import logging

import coloredlogs
import uvicorn
from fastapi import FastAPI
from rich.logging import RichHandler

from scrapper.routers import trending_papers

logging.basicConfig(
    level="WARNING",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
app = FastAPI()
app.include_router(trending_papers.router)


@app.on_event("startup")
def startup_event() -> None:
    """Run API startup events."""
    # Remove all handlers associated with the root logger object.
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)
    # Add coloredlogs' coloured StreamHandler to the root logger.
    coloredlogs.install()


@app.get("/")
def read_root() -> str:
    """Read root."""
    return "Ai scrapper"


def main() -> None:
    """Main function to run the app."""
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
