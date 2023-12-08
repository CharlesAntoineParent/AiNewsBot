"""This module contains the SimpleEvaluator class."""
import datetime
import logging
from typing import Any, List

import numpy as np

from paperchooser.evaluators import BaseEvaluator
from paperchooser.exceptions import PaperAttributeNotFoundError
from paperchooser.utils import convert_iso_date


class SimpleEvaluator(BaseEvaluator):
    """This evaluator gives score based on ponderation of stars and age of the paper.

    Attributes:
    - stars_per_hour_weight (float): The weight of stars per day in the evaluation.
    - stars_weight (float): The weight of stars in the evaluation.
    - date_diff_weight (float): The weight of date difference in the evaluation.
    """

    stars_per_hour_weight: float = 1.0
    stars_weight: float = 1.0
    date_diff_weight: float = 1.0

    def evaluate(self, paper_info: dict[str, Any]) -> float:
        """Evaluate a single paper based on its information.

        Args:
            paper_info (dict): A dictionary containing information about the paper.

        Returns:
            float: The evaluation score of the paper.
        """
        try:
            score: float = 0.0
            score += self.stars_per_hour_weight * float(paper_info["Stars per hour"])
            score += self.stars_weight * float(paper_info["Stars"])
            date = convert_iso_date(paper_info["Publication date"])
            score *= self.date_diff_weight ** self._days_since(date)
        except KeyError as e:
            raise PaperAttributeNotFoundError from e
        return score

    def evaluate_batch(
        self, all_paper_info: List[dict[str, Any]]
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        """Evaluate a batch of papers based on their information.

        Args:
            all_paper_info (List[dict]): Dictionnaries containing information about the papers.

        Returns:
            List[float]: A list of evaluation scores for each paper.
        """
        batch_out = []
        for paper_info in all_paper_info:
            try:
                batch_out.append(self.evaluate(paper_info))
            except PaperAttributeNotFoundError:
                msg = f"Paper {paper_info['Title']} does not have all the required attributes."
                logging.warning(msg)
        return np.array(batch_out)

    @staticmethod
    def _days_since(date: datetime.datetime) -> float:
        """Calculate the number of days between today and a given datetime.

        Args:
            date (datetime): Date.

        Returns:
            int: The number of days between today and the given datetime.
        """
        today = datetime.datetime.now().astimezone(datetime.timezone.utc)
        nb_days: float = (today - date).days
        assert nb_days >= 0, "Papers cannot be published in the future."
        return nb_days
