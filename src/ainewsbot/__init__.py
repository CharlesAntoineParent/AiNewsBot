"""ainewsbot package."""
from ainewsbot.api import app
from ainewsbot.pipeline import PaperRetrieverPipeline

__all__ = ["app", "PaperRetrieverPipeline"]
