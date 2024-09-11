"""This modules are the evaluators that will be used to evaluate the papers."""
from paperchooser.evaluators.base_evaluator import BaseEvaluator
from paperchooser.evaluators.simple_evaluator import SimpleEvaluator

__all__ = [
    "BaseEvaluator",
    "SimpleEvaluator",
]
