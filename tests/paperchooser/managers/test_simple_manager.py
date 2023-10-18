# ruff: noqa : SLF001
"""Test for paperchooser simple manager."""
import datetime
from typing import Any, List

import numpy as np
import pytest
from freezegun import freeze_time

from paperchooser.evaluators import BaseEvaluator
from paperchooser.managers import SimpleManager


class MockEvaluator(BaseEvaluator):
    """Mock evaluator."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize."""

    def evaluate_batch(
        self, all_paper_info: List[dict[str, Any]]
    ) -> np.ndarray[Any, np.dtype[np.float64]]:
        """Evaluate a batch of papers based on their information."""
        return np.array([float(i) for i in range(len(all_paper_info))])

    def evaluate(self, paper_info: dict[str, Any]) -> float:
        """Evaluate a single paper based on its information."""
        return 1.0


class TestSimpleManager:
    """This class tests the SimpleManager class."""

    @pytest.fixture()
    def manager_with_mocked_evaluator(self, monkeypatch: pytest.MonkeyPatch) -> SimpleManager:
        """Fixture a mock evaluator."""
        return SimpleManager(evaluator=MockEvaluator())

    @pytest.fixture()
    def paper_infos(self) -> list[dict[str, Any]]:
        """Fixture a list of paper infos."""
        return [
            {
                "Title": "Paper 1",
                "Publication date": datetime.datetime(2021, 1, 1).astimezone(datetime.timezone.utc),
                "Stars": 1,
                "Stars per hour": 1,
            },
            {
                "Title": "Paper 2",
                "Publication date": datetime.datetime(2021, 1, 2).astimezone(datetime.timezone.utc),
                "Stars": 2,
                "Stars per hour": 2,
            },
            {
                "Title": "Paper 3",
                "Publication date": datetime.datetime(2021, 1, 3).astimezone(datetime.timezone.utc),
                "Stars": 3,
                "Stars per hour": 3,
            },
        ]

    def test_get_best_paper(
        self, paper_infos: list[dict[str, Any]], manager_with_mocked_evaluator: SimpleManager
    ) -> None:
        """Test get_best_paper."""
        assert manager_with_mocked_evaluator.get_best_paper(paper_infos) == paper_infos[-1]

    def test_rank_papers(
        self, paper_infos: list[dict[str, Any]], manager_with_mocked_evaluator: SimpleManager
    ) -> None:
        """Test rank_papers."""
        ranked_papers = manager_with_mocked_evaluator.rank_papers(paper_infos)
        assert ranked_papers == paper_infos

    @freeze_time("2021-01-04")
    def test_is_valid_paper_true(
        self, paper_infos: list[dict[str, Any]], manager_with_mocked_evaluator: SimpleManager
    ) -> None:
        """Test paper valid."""
        assert manager_with_mocked_evaluator._is_paper_valid(paper_infos[0])

    @freeze_time("2021-01-20")
    def test_is_valid_paper_false(
        self, paper_infos: list[dict[str, Any]], manager_with_mocked_evaluator: SimpleManager
    ) -> None:
        """Test paper not valid."""
        assert not manager_with_mocked_evaluator._is_paper_valid(paper_infos[0])

    @freeze_time("2021-01-17")
    def test_get_valid_papers(
        self, paper_infos: list[dict[str, Any]], manager_with_mocked_evaluator: SimpleManager
    ) -> None:
        """The get valid papers."""
        assert manager_with_mocked_evaluator.get_valid_papers(paper_infos) == [paper_infos[-1]]
