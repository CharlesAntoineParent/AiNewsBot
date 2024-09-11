"""ainewsbot REST API."""

import logging
from typing import Any

import coloredlogs
import uvicorn
from fastapi import FastAPI

from ainewsbot.pipeline import PaperRetrieverPipeline

app = FastAPI()
SUMMARIZER_URL = "http://summarizer:8000"
SCRAPPER_URL = "http://scrapper:8000"
EVALUATOR_URL = "http://paperchooser:8000"

pipeline = PaperRetrieverPipeline(
    summarizer_url=SUMMARIZER_URL, scrapper_url=SCRAPPER_URL, paperchooser_url=EVALUATOR_URL
)


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
    return "Ai News Bot Generator"


@app.get("/daily_paper")
def get_daily_paper() -> dict[str, Any]:
    """Read root."""
    out = pipeline.run()
    return out


def main() -> None:
    """Main function to run the app."""
    uvicorn.run(app, host="localhost", port=8003)


if __name__ == "__main__":
    main()
