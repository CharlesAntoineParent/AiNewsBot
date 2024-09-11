"""This modules implements the manager used for the paperchooser."""

from paperchooser.managers.base_manager import BaseManager
from paperchooser.managers.manager_factory import ManagerFactory
from paperchooser.managers.simple_manager import SimpleManager

__all__ = ["ManagerFactory", "BaseManager", "SimpleManager"]
