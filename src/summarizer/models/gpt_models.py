"""This module implements the gpt models."""
import secrets
from typing import Any, ClassVar

import openai
import tiktoken

from summarizer.models.base_model import BaseLLM


class GPTModel(BaseLLM):
    """This model is gpt 3.5 turbo with 4k context."""

    min_temp: ClassVar[float] = 0
    max_temp: ClassVar[float] = 0.6
    default_temp: ClassVar[float] = 0
    model_api_name: ClassVar[str] = "gpt-3.5-turbo"

    class Config:
        """This class is used to allow arbitrary types in pydantic."""

        arbitrary_types_allowed = True

    @classmethod
    def random_args(cls) -> dict[str, Any]:
        """This method need to be implemented."""
        tmp = cls.min_temp + (cls.max_temp - cls.min_temp) * (
            secrets.randbelow(1_000_000) / 1_000_000
        )
        return {"temperature": tmp, "model": cls.model_api_name}

    @classmethod
    def default_args(cls) -> dict[str, Any]:
        """This method need to be implemented."""
        return {"temperature": cls.default_temp, "model": cls.model_api_name}

    def predict(self, prompt: str) -> Any:
        """Return prediction from model."""
        predict_args = self.default_args()
        return openai.ChatCompletion.create(messages=prompt, **predict_args)["choices"][0][  # type: ignore[no-untyped-call]
            "message"
        ][
            "content"
        ]

    def random_predict(self, prompt: str) -> Any:
        """Return prediction from model with random parameters."""
        predict_args = self.random_args()
        return openai.ChatCompletion.create(messages=prompt, **predict_args)["choices"][0][
            "message"
        ]["content"]

    def count_tokens(self, prompt: str) -> int:
        """Return the number of tokens in the prompt."""
        encoding = tiktoken.get_encoding("cl100k_base")
        num_tokens = len(encoding.encode(prompt))
        return num_tokens


class GPT35Turbo4(GPTModel):
    """This model is gpt 3.5 turbo with 4k context."""

    max_token: ClassVar[int] = 4000
    model_name: ClassVar[str] = "GPT 3.5 turbo 4k context"
    model_api_name: ClassVar[str] = "gpt-3.5-turbo"


class GPT35Turbo16(GPTModel):
    """This model is gpt 3.5 turbo with 16k context."""

    max_token: ClassVar[int] = 16000
    model_name: ClassVar[str] = "GPT 3.5 turbo 16k context"
    model_api_name: ClassVar[str] = "gpt-3.5-turbo-16k"


class GPT4Turbo8(GPTModel):
    """This model is gpt 4 turbo with 8k context."""

    max_token: ClassVar[int] = 8000
    model_name: ClassVar[str] = "GPT 4 turbo 16k context"
    model_api_name: ClassVar[str] = "gpt-4"


class GPT4Turbo32(GPTModel):
    """This model is gpt 4 turbo with 32k context."""

    max_token: ClassVar[int] = 32000
    model_name: ClassVar[str] = "GPT 4 turbo 16k context"
    model_api_name: ClassVar[str] = "gpt-4-32k"


class GPT4Turbo128(GPTModel):
    """This model is gpt 4 turbo with 128k context."""

    max_token: ClassVar[int] = 128000
    model_name: ClassVar[str] = "GPT 4 turbo 128k context"
    model_api_name: ClassVar[str] = "gpt-4-1106-preview"
