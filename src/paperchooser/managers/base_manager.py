"""Base manager class."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel

from paperchooser.evaluators.base_evaluator import BaseEvaluator


class BaseManager(BaseModel, ABC):
    """Base class for all managers.

    Attributes:
        evaluator (BaseEvaluator): The evaluator used to evaluate the papers.
    """

    evaluator: BaseEvaluator

    @abstractmethod
    def get_best_paper(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get the best papers from the manager.

        Args:
            papers: List[Dict[str, Any]]: Papers to get.

        Returns:
            Info of the best papers
        """

    @abstractmethod
    def rank_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank the papers.

        Args:
            papers (List[Dict[str, Any]]): Dictionnaries containing information about the papers.

        Returns:
            A list of dictionaries containing information about the papers.
        """

    @abstractmethod
    def get_valid_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return the papers respecting selection conditions.

        Args:
            papers (List[Dict[str, Any]]): Dictionnaries containing information about the papers.

        Returns:
            A list of dictionaries containing information about the papers.
        """
        return papers
