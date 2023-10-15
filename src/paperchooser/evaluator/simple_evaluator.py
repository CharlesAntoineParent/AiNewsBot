"""This module contains the SimpleEvaluator class."""
from typing import Any, List

import numpy as np

from paperchooser.evaluator.base_evaluator import BaseEvaluator


class SimpleEvaluator(BaseEvaluator):
    """This evaluator gives score based on ponderation of stars and age of the paper.

    Attributes:
    - stars_per_day_weight (float): The weight of stars per day in the evaluation.
    - stars_weight (float): The weight of stars in the evaluation.
    - date_diff_weight (float): The weight of date difference in the evaluation.
    """

    stars_per_day_weight: float = 1.0
    stars_weight: float = 1.0
    date_diff_weight: float = 1.0

    def evaluate(self, paper_info: dict[Any, str]) -> float:
        """Evaluate a single paper based on its information.

        Args:
            paper_info (dict): A dictionary containing information about the paper.

        Returns:
            float: The evaluation score of the paper.
        """
        return 1.0

    def evaluate_batch(
        self, all_paper_info: List[dict[Any, str]]
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        """Evaluate a batch of papers based on their information.

        Args:
            all_paper_info (List[dict]): Dictionnaries containing information about the papers.

        Returns:
            List[float]: A list of evaluation scores for each paper.
        """
        return np.array([1.0 for _ in all_paper_info])
