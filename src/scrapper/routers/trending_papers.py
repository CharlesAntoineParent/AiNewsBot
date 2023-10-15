"""Router for the trending papers endpoint."""
from typing import Any, Dict, List

from fastapi import APIRouter

from scrapper.papers_with_code_scrapper import PapersWithCodeTrendingScrapper

router = APIRouter(prefix="/trending_papers", tags=["trending_papers"])
scrapper = PapersWithCodeTrendingScrapper()


@router.get("/")
def get_trending_papers_info(nb_papers: int = 10) -> List[Dict[str, Any]]:
    """Get the trending papers from paperswithcode.com."""
    papers: List[Dict[str, Any]] = scrapper.get_best_papers(nb_papers)
    return papers
