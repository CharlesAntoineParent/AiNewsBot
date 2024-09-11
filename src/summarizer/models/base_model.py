"""This module contains the BaseLLM class."""
from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel


class BaseLLM(BaseModel, ABC):
    """This class is the abc class for all possible LLM."""

    max_token: ClassVar[int]
    name: ClassVar[str]

    @property
    def max_token(self) -> int:
        """Get the max number of token for the model."""
        return self.max_token

    @property
    def name(self) -> str:
        """Get the model name."""
        return self.name

    @abstractmethod
    def predict(self, prompt: str) -> str:
        """Return prediction from model."""

    @abstractmethod
    def random_predict(self, prompt: str) -> str:
        """Return prediction from model with random arguments."""

    @abstractmethod
    def count_tokens(self, prompt: str) -> int:
        """Return the number of tokens in the prompt."""
