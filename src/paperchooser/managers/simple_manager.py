"""This module contains the SimpleManager class."""
from typing import Any, Dict, List

import numpy as np

from paperchooser.managers.base_manager import BaseManager


class SimpleManager(BaseManager):
    """This manager get the best valid papers based on date.

    Attributes:
    - max_day (int): The maximum number of days a paper can be old to be selected.
    """

    max_day: int = 14

    def get_best_paper(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get the best papers from the manager.

        Args:
            papers: List[Dict[str, Any]]: Papers to get.

        Returns:
            Info of the best papers
        """
        scores = self.evaluator.evaluate_batch(papers)
        max_id = np.argmax(scores)
        return papers[max_id]

    def rank_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank the papers.

        Args:
            papers (List[Dict[str, Any]]): Dictionnaries containing information about the papers.

        Returns:
            A list of dictionaries containing information about the papers.
        """
        scores = self.evaluator.evaluate_batch(papers)
        idxs_sorted = np.argsort(scores)
        return [papers[idx] for idx in idxs_sorted]

    def get_valid_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return the papers respecting selection conditions.

        Args:
            papers (List[Dict[str, Any]]): A list of dictionaries containing paper infos.

        Returns:
            List[Dict[str, Any]]: Info of only valid papers.
        """
        return [paper for paper in papers if self._is_paper_valid(paper)]

    def _is_paper_valid(self, paper: Dict[str, Any]) -> bool:
        """Check if a paper is valid.

        Args:
            paper (Dict[str, Any]): A dictionary containing information about the paper.

        Returns:
            bool: True if the paper is valid, False otherwise.
        """
        return True
