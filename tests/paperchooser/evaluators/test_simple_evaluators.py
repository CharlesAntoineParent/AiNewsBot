# ruff: noqa : SLF001
"""Test for paperchooser simple evaluator."""
import datetime
from typing import Any

import numpy as np
import pytest
from freezegun import freeze_time

from paperchooser.evaluators import SimpleEvaluator
from paperchooser.exceptions import PaperAttributeNotFoundError

FAKE_TIME = datetime.datetime(2021, 1, 4, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)


class TestSimpleEvaluator:
    """Test the SimpleEvaluator class."""

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

    @pytest.fixture()
    def bad_paper_infos(self) -> list[dict[str, Any]]:
        """Fixture a list of paper infos."""
        return [
            {
                "Title": "Paper 1",
                "Publication date": datetime.datetime(2021, 1, 1).astimezone(datetime.timezone.utc),
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

    @pytest.fixture()
    def default_simple_evaluator(self) -> SimpleEvaluator:
        """Fixture a SimpleEvaluator instance."""
        return SimpleEvaluator()

    @pytest.fixture()
    def custom_simple_evaluator(self) -> SimpleEvaluator:
        """Fixture a SimpleEvaluator instance with custom weight."""
        return SimpleEvaluator(stars_per_hour_weight=2.0, stars_weight=0.0, date_diff_weight=1.0)

    def test_evaluate_raise(
        self,
        bad_paper_infos: list[dict[str, Any]],
        default_simple_evaluator: SimpleEvaluator,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test the evaluate raise."""
        monkeypatch.setattr(
            SimpleEvaluator,
            "_days_since",
            lambda x, y: 2.0,
        )
        with pytest.raises(PaperAttributeNotFoundError, match=""):
            default_simple_evaluator.evaluate(bad_paper_infos[0])

    def test_evaluate_default(
        self,
        paper_infos: list[dict[str, Any]],
        default_simple_evaluator: SimpleEvaluator,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test the evaluate method with default weights."""
        monkeypatch.setattr(
            SimpleEvaluator,
            "_days_since",
            lambda x, y: 2.0,
        )
        first_expected_score: float = 2.0
        second_expected_score: float = 4.0
        third_expected_score: float = 6.0
        assert default_simple_evaluator.evaluate(paper_infos[0]) == first_expected_score
        assert default_simple_evaluator.evaluate(paper_infos[1]) == second_expected_score
        assert default_simple_evaluator.evaluate(paper_infos[2]) == third_expected_score

    def test_evaluate_custom(
        self,
        paper_infos: list[dict[str, Any]],
        custom_simple_evaluator: SimpleEvaluator,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test the evaluate method with custom weights."""
        monkeypatch.setattr(
            SimpleEvaluator,
            "_days_since",
            lambda x, y: 2.0,
        )
        first_expected_score: float = 2.0
        second_expected_score: float = 4.0
        third_expected_score: float = 6.0
        assert custom_simple_evaluator.evaluate(paper_infos[0]) == first_expected_score
        assert custom_simple_evaluator.evaluate(paper_infos[1]) == second_expected_score
        assert custom_simple_evaluator.evaluate(paper_infos[2]) == third_expected_score

    def test_evaluate_batch_default(
        self,
        paper_infos: list[dict[str, Any]],
        default_simple_evaluator: SimpleEvaluator,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test the evaluate batch method with default weights."""
        monkeypatch.setattr(
            SimpleEvaluator,
            "_days_since",
            lambda x, y: 2.0,
        )
        expected = np.array([2.0, 4.0, 6.0])
        assert (default_simple_evaluator.evaluate_batch(paper_infos) == expected).all()

    def test_evaluate_batch_custom(
        self,
        paper_infos: list[dict[str, Any]],
        custom_simple_evaluator: SimpleEvaluator,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test the evaluate batch method with custom weights."""
        monkeypatch.setattr(
            SimpleEvaluator,
            "_days_since",
            lambda x, y: 2.0,
        )
        expected = np.array([2.0, 4.0, 6.0])
        assert (custom_simple_evaluator.evaluate_batch(paper_infos) == expected).all()

    @freeze_time("2021-01-04")
    def test_days_since(self) -> None:
        """Test days counter."""
        date = datetime.datetime(2021, 1, 1).astimezone(datetime.timezone.utc)
        expected = 3
        assert SimpleEvaluator._days_since(date) == expected

    @freeze_time("2021-01-04")
    def test_days_since_raise(self) -> None:
        """Test days counter raise."""
        date = datetime.datetime(2021, 1, 5).astimezone(datetime.timezone.utc)
        with pytest.raises(AssertionError, match=""):
            SimpleEvaluator._days_since(date)
