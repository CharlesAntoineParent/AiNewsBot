"""This module contains the pipeline for the paper retriever."""

from typing import Any
from urllib.parse import urljoin

import requests
from pydantic import BaseModel

TRENDING_PAPERS_ENDPOINT = "paper/trending_papers"
EVALUATE_PAPERS_ENDPOINT = "selection/best"


class PaperRetrieverPipeline(BaseModel):
    """This class is the pipeline for the paper retriever.

    It has the role to organize the different api calls to get the papers.

    Args:
        summarizer_url (str): Summarizer api url
        paperchooser_url (str): Paperchooser api url
        scrapper_url (str): Scrapper api url
    """

    summarizer_url: str
    paperchooser_url: str
    scrapper_url: str

    def get_papers(self, nb_papers: int = 20) -> Any:
        """This method scrap the papers from the scrapper.

        Args:
            nb_papers (int, optional): [description]. Defaults to 20.

        Returns:
            list[dict[str, Any]]: [description]
        """
        url = urljoin(self.scrapper_url, TRENDING_PAPERS_ENDPOINT)
        params = {"nb_papers": nb_papers}
        response = requests.get(url, params=params, timeout=10)
        papers = response.json()
        return papers

    def score_papers(self, papers: list[dict[str, Any]]) -> Any:
        """This method score the papers with the paperchooser.

        Args:
            papers (list[dict[str, Any]]): [description]

        Returns:
            list[dict[str, Any]]: [description]
        """
        url = urljoin(self.paperchooser_url, EVALUATE_PAPERS_ENDPOINT)
        response = requests.post(url, json=papers, timeout=10)
        paper = response.json()
        return paper

    def get_all_info(self, paper_url: str) -> Any:
        """This returns full paper info."""
        url = urljoin(self.scrapper_url, "paper/")
        params = {"paper_url": paper_url[1:]}
        response = requests.post(url, params=params, timeout=10)
        paper = response.json()
        return paper

    def get_summary(self, paper_url: str) -> Any:
        """This method get the summary of a paper.

        Args:
            paper_url (str): [description]

        Returns:
            str: [description]
        """
        url = urljoin(self.summarizer_url, "summarize")
        params = {"paper_url": paper_url}
        response = requests.post(url, params=params, timeout=600)
        summary = response.json()
        return summary

    def run(self) -> dict[str, Any]:
        """Run the pipeline.

        Returns:
            dict[str, Any]: [description]
        """
        papers = self.get_papers()
        paper = self.score_papers(papers)
        paper_info = self.get_all_info(paper["URL"])
        summary = self.get_summary(paper_info["pdf_url"])
        paper_info["Summary"] = summary
        return paper_info
