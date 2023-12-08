"""Router for the trending papers endpoint."""
from typing import Any, Dict, List

from fastapi import APIRouter

from scrapper.papers_with_code_scrapper import (
    PapersWithCodePaperScrapper,
    PapersWithCodeTrendingScrapper,
)

router = APIRouter(prefix="/paper", tags=["trending_papers"])
scrapper = PapersWithCodeTrendingScrapper()


@router.get("/trending_papers")
def get_trending_papers_info(nb_papers: int = 10) -> List[Dict[str, Any]]:
    """Get the trending papers from paperswithcode.com."""
    papers: List[Dict[str, Any]] = scrapper.get_best_papers(nb_papers)
    return papers


@router.post("/")
def get_paper_info(paper_url: str) -> dict[str, Any]:
    """Get the trending papers from paperswithcode.com."""
    paper: PapersWithCodePaperScrapper = PapersWithCodePaperScrapper(paper_url_path=paper_url)
    return paper.get_all_paper_info()
