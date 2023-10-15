"""Base class for all evaluators."""

from abc import ABC, abstractmethod
from typing import Any, List

import numpy as np
from pydantic import BaseModel


class BaseEvaluator(ABC, BaseModel):
    """Base class for all evaluators."""

    @abstractmethod
    def evaluate(self, paper_info: dict[Any, str]) -> float:
        """Evaluate the model.

        Args:
            paper_info (dict[Any, str]): Dictionnary containing paper info.

        Returns:
            Score for the given paper
        """

    @abstractmethod
    def evaluate_batch(
        self, all_paper_info: List[dict[Any, str]]
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        """Evaluate the model on a batch of data.

        Args:
            all_paper_info (List[dict[Any, str]]): A list of dictionaries containing information
            about the papers.

        Returns:
            An array containing scores for each paper
        """
