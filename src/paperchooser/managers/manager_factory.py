"""This module contains the manager factory class."""
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel
from pydantic_core import ValidationError

from paperchooser import evaluators, managers


class ManagerFactory(BaseModel):
    """This class is a factory that create a manager from a config file or a config dictionnary."""

    @staticmethod
    def create_class_from_config(config_path: Path) -> managers.BaseManager:
        """Create a manager from a config file.

        Args:
            config_path (str): Path to the config file.

        Returns:
            BaseManager: The instantiate manager based on config
        """
        with Path(config_path).open("r") as f:
            config = yaml.safe_load(f)
        return ManagerFactory.create_class(config)

    @staticmethod
    def create_class(config: Dict[str, Any]) -> managers.BaseManager:
        """This function create a manager from a config dictionnary.

        Args:
            config (Dict[str, Any]): Config dictionnary.

        Returns:
            BaseManager: The instantiate manager based on config
        """
        evaluator = ManagerFactory._get_evaluator(config["evaluator"])
        manager = ManagerFactory._get_manager(evaluator, config["manager"])
        return manager

    @staticmethod
    def _get_evaluator(evaluator_config: Dict[str, Any]) -> evaluators.BaseEvaluator:
        """This function instantiate the evaluator if found.

        Args:
            evaluator_config (Dict[str, Any]): Config dictionnary of the evaluator.

        Returns:
            BaseEvaluator: The instantiate evaluator based on config
        """
        class_name = evaluator_config.pop("class")
        try:
            evaluator_class = getattr(evaluators, class_name)
            evaluator_instance: evaluators.BaseEvaluator = evaluator_class(**evaluator_config)
        except (NameError, ValidationError) as e:
            msg = f"Class {class_name} not found or invalid config."
            raise ValueError(msg) from e
        else:
            return evaluator_instance

    @staticmethod
    def _get_manager(
        evaluator_instance: evaluators.BaseEvaluator, manager_config: Dict[str, Any]
    ) -> managers.BaseManager:
        """This function instantiate the manager if found.

        Args:
            evaluator_instance (BaseEvaluator): Evalutor to use.
            manager_config (Dict[str, Any]): Config dictionnary of the manager.

        Returns:
            BaseManager: The instantiate manager based on config
        """
        class_name = manager_config.pop("class")
        try:
            manager_class = getattr(managers, class_name)
            manager: managers.BaseManager = manager_class(
                evaluator=evaluator_instance, **manager_config
            )
        except (NameError, ValidationError) as e:
            msg = f"Class {class_name} not found or invalid config."
            raise ValueError(msg) from e
        else:
            return manager
