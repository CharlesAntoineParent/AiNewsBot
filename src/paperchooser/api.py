"""Paperchooser REST API."""

import logging

import coloredlogs
from fastapi import FastAPI

from paperchooser.routers.manager import manager_router

app = FastAPI()
app.include_router(manager_router)


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
    return "Ai paperchooser"
