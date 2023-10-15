"""This modules implements the scrapper for paperswithcode."""
from scrapper.papers_with_code_scrapper.exceptions import (
    PaperAttributeNotFoundError,
    PapersWithCodeNoResponseTimeOutError,
)
from scrapper.papers_with_code_scrapper.paper_scrapper import PapersWithCodePaperScrapper
from scrapper.papers_with_code_scrapper.trending_papers_scrapper import (
    PapersWithCodeTrendingScrapper,
)

__all__ = [
    "PapersWithCodeTrendingScrapper",
    "PapersWithCodeNoResponseTimeOutError",
    "PaperAttributeNotFoundError",
    "PapersWithCodePaperScrapper",
]
