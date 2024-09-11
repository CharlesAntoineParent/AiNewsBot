"""ainewsbot REST API."""

import logging
from pathlib import Path

import coloredlogs
import uvicorn
from fastapi import FastAPI

from summarizer.chains import ChainFactory

app = FastAPI()

CONFIG_PATH = Path("./src/summarizer/config/base.yaml")
chain = ChainFactory.build_chain_from_yaml(CONFIG_PATH)


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
    return "Ai summarizer"


@app.post("/summarize")
async def summarize_paper(paper_url: str) -> str:
    """Post method returning a summary of the given paper.

    Args:
        paper_url (str): Url to the paper.

    Returns:
        str : Summary of the paper.
    """
    return chain.run_chain(paper_url)


def main() -> None:
    """Main function to run the app."""
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
