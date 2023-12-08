"""This module implements the MapReduceBase class."""
from abc import ABC, abstractmethod

from pydantic import BaseModel


class MapReduceBase(BaseModel, ABC):
    """Base class for map-reduce models."""

    @staticmethod
    @abstractmethod
    def get_reduce(content: str) -> list[dict[str, str]]:
        """Return reduce prompt."""

    @staticmethod
    @abstractmethod
    def get_map(summarized_content: list[str]) -> list[dict[str, str]]:
        """Return map prompt."""
