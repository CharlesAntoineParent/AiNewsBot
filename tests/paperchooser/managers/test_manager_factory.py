"""Test for paperchooser manager factory."""
# ruff: noqa : SLF001
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
import yaml

from paperchooser.managers import BaseManager
from paperchooser.managers.manager_factory import ManagerFactory


class TestManagerFactory:
    """This class contains unit tests for the ManagerFactory class."""

    @pytest.fixture(scope="session")
    def config(self, tmpdir_factory: pytest.TempdirFactory) -> Generator[Path, None, None]:
        """This creates temp config file for testing and returns path."""
        config = {
            "evaluator": {"class": "DummyEvaluator", "param1": "value1", "param2": "value2"},
            "manager": {"class": "DummyManager", "param3": "value3", "param4": "value4"},
        }
        fn = tmpdir_factory.mktemp("config").join("config.yml")
        config_path = Path(str(fn))
        with config_path.open("w") as f:
            yaml.dump(config, f)
            yield config_path

    def test_create_class_from_config(self, config: Path) -> None:
        """Test that ManagerFactory.create_class_from_config."""
        with patch(
            "paperchooser.managers.manager_factory.ManagerFactory.create_class"
        ) as mock_create_class:
            mock_manager = MagicMock(spec=BaseManager)
            mock_create_class.return_value = mock_manager

            manager = ManagerFactory.create_class_from_config(config)
            with config.open("r") as f:
                expected_config = yaml.safe_load(f)

            mock_create_class.assert_called_once_with(expected_config)
            assert manager == mock_manager

    def test_create_class(self) -> None:
        """Test that ManagerFactory.create_class."""
        config = {
            "evaluator": {"class": "DummyEvaluator", "param1": "value1", "param2": "value2"},
            "manager": {"class": "DummyManager", "param3": "value3", "param4": "value4"},
        }

        with patch(
            "paperchooser.managers.manager_factory.ManagerFactory._get_evaluator"
        ) as mock_get_evaluator, patch(
            "paperchooser.managers.manager_factory.ManagerFactory._get_manager"
        ) as mock_get_manager:
            mock_evaluator = MagicMock()
            mock_get_evaluator.return_value = mock_evaluator
            mock_manager = MagicMock(spec=BaseManager)
            mock_get_manager.return_value = mock_manager

            manager = ManagerFactory.create_class(config)

            mock_get_evaluator.assert_called_once_with(config["evaluator"])
            mock_get_manager.assert_called_once_with(mock_evaluator, config["manager"])
            assert manager == mock_manager

    def test_get_evaluator(self) -> None:
        """Test create evaluator."""
        evaluator_config = {"class": "DummyEvaluator", "param1": "value1", "param2": "value2"}

        with patch("paperchooser.managers.manager_factory.evaluators") as mock_evaluators:
            mock_evaluator_class = MagicMock()
            mock_evaluators.DummyEvaluator = mock_evaluator_class
            mock_evaluator = MagicMock()
            mock_evaluator_class.return_value = mock_evaluator

            evaluator = ManagerFactory._get_evaluator(evaluator_config)

            mock_evaluator_class.assert_called_once_with(param1="value1", param2="value2")
            assert evaluator == mock_evaluator

    def test_get_evaluator_with_invalid_class(self) -> None:
        """Test create evaluator bad evaluator."""
        evaluator_config = {"class": "InvalidEvaluator"}

        with pytest.raises(
            AttributeError,
            match="module 'paperchooser.evaluators' has no attribute 'InvalidEvaluator'",
        ):
            ManagerFactory._get_evaluator(evaluator_config)

    def test_get_manager(self) -> None:
        """Test create manager."""
        evaluator_instance = MagicMock(spec=BaseManager)
        manager_config = {"class": "DummyManager", "param3": "value3", "param4": "value4"}

        with patch("paperchooser.managers.manager_factory.managers") as mock_managers:
            mock_manager_class = MagicMock()
            mock_managers.DummyManager = mock_manager_class
            mock_manager = MagicMock(spec=BaseManager)
            mock_manager_class.return_value = mock_manager

            manager = ManagerFactory._get_manager(evaluator_instance, manager_config)

            mock_manager_class.assert_called_once_with(
                evaluator=evaluator_instance, param3="value3", param4="value4"
            )
            assert manager == mock_manager

    def test_get_manager_with_invalid_class(self) -> None:
        """Test create manager bad config."""
        evaluator_instance = MagicMock(spec=BaseManager)
        manager_config = {"class": "InvalidManager"}

        with pytest.raises(
            AttributeError, match="module 'paperchooser.managers' has no attribute 'InvalidManager'"
        ):
            ManagerFactory._get_manager(evaluator_instance, manager_config)
