"""This modules are the evaluators that will be used to evaluate the papers."""
from paperchooser.evaluator.base_evaluator import BaseEvaluator
from paperchooser.evaluator.simple_evaluator import SimpleEvaluator

__all__ = [
    "BaseEvaluator",
    "SimpleEvaluator",
]
