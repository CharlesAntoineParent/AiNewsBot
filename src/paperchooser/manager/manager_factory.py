"""This module contains the manager factory class."""
from ast import literal_eval
from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel
from pydantic_core import ValidationError

from paperchooser.evaluator import *  # noqa: F403
from paperchooser.manager.base_manager import BaseManager


class ManagerFactory(BaseModel):
    """This class is a factory that create a manager from a config file or a config dictionnary."""

    @staticmethod
    def create_class_from_config(config_path: str) -> BaseManager:
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
    def create_class(config: Dict[str, Any]) -> BaseManager:
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
    def _get_evaluator(evaluator_config: Dict[str, Any]) -> BaseEvaluator:  # noqa: F405
        """This function instantiate the evaluator if found.

        Args:
            evaluator_config (Dict[str, Any]): Config dictionnary of the evaluator.

        Returns:
            BaseEvaluator: The instantiate evaluator based on config
        """
        class_name = evaluator_config.pop("class_name")
        try:
            evaluator_class = literal_eval(class_name)
            evaluator: BaseEvaluator = evaluator_class(**evaluator_config)  # noqa: F405
        except (NameError, ValidationError) as e:
            msg = f"Class {class_name} not found or invalid config."
            raise ValueError(msg) from e
        else:
            return evaluator

    @staticmethod
    def _get_manager(
        evaluator: BaseEvaluator, manager_config: Dict[str, Any]  # noqa: F405
    ) -> BaseManager:
        """This function instantiate the manager if found.

        Args:
            evaluator (BaseEvaluator): Evalutor to use.
            manager_config (Dict[str, Any]): Config dictionnary of the manager.

        Returns:
            BaseManager: The instantiate manager based on config
        """
        class_name = manager_config.pop("class_name")
        try:
            manager_class = literal_eval(class_name)
            manager: BaseManager = manager_class(evaluator=evaluator, **manager_config)
        except (NameError, ValidationError) as e:
            msg = f"Class {class_name} not found or invalid config."
            raise ValueError(msg) from e
        else:
            return manager
