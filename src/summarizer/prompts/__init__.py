"""This modules defines the prompt."""

from summarizer.prompts.map_reduce_base import MapReduceBase
from summarizer.prompts.map_reduce_child import MapReduceChild
from summarizer.prompts.map_reduce_normal import MapReduceNormal

__all__ = ["MapReduceBase", "MapReduceChild", "MapReduceNormal"]
