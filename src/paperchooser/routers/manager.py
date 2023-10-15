"""Router for the paperchooser manager."""

import os
from typing import Any, Dict, List

from fastapi import APIRouter

from paperchooser.manager import ManagerFactory

manager_router = APIRouter(prefix="/selection", tags=["paperchooser"])
CONFIG_PATH = os.environ.get("CONFIG_PATH", "./src/paperchooser/config/base_chooser.yaml")
manager = ManagerFactory.create_class_from_config(CONFIG_PATH)


@manager_router.post("/ranker")
async def rank_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Post method returning a list of valid papers ranked by score.

    Args:
        papers (List[Dict[str, Any]]): Papers to filter and order.

    Returns:
        List[Dict[str, Any]] : List of valid papers ranked by score.
    """
    ranked_papers = manager.rank_papers(papers)
    return ranked_papers


@manager_router.post("/validator")
async def validate_papers(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return a list of valid papers.

    Args:
        papers (List[Dict[str, Any]]): Papers to filter and order.

    Returns:
        List[Dict[str, Any]] : List of valid papers.
    """
    ranked_papers = manager.get_valid_papers(papers)
    return ranked_papers


@manager_router.post("/best")
async def get_best_paper(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Return the highest ranked paper.

    Args:
        papers (List[Dict[str, Any]]): Candidate papers.

    Returns:
        Dict[str, Any] : Paper info of the highest ranked paper.
    """
    return manager.get_best_paper(papers)
