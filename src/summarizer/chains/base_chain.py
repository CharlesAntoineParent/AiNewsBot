"""This module contains the BaseChain class."""
from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseChain(BaseModel, ABC):
    """Base class for all chains."""

    @abstractmethod
    def run_chain(self, pdf_url: str) -> str:
        """Return prediction from model."""
