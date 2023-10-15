"""This modulle implements the scrapper for a specific paper."""
import re
from functools import wraps
from typing import Any, Callable

import pydantic
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from scrapper.papers_with_code_scrapper import utils
from scrapper.papers_with_code_scrapper.exceptions import PaperAttributeNotFoundError

SUCCESS_STATUS_CODE = 200
NOT_FOUND_STATUS_CODE = 404


def check_for_not_found(func: Callable[..., Any]) -> Callable[..., Any]:
    """A decorator that checks the status code of a HTTP response.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except AttributeError as e:
            if re.match(".* object has no attribute .*", str(e)):
                msg = f"Element not found during scrapping ({func.__name__})"
                raise PaperAttributeNotFoundError(msg) from e
            raise

    return wrapper


class PapersWithCodePaperScrapper(BaseModel):
    """A class for scraping trending papers from paperswithcode.com."""

    paper_url_path: str
    time_out_seconds: int = 20
    url: str = "https://paperswithcode.com/"

    @pydantic.model_validator(mode="after")
    def check_paper_endpoint(self) -> "PapersWithCodePaperScrapper":
        """Validate the paper endpoint."""
        if not self.paper_url_path.startswith("paper/"):
            msg = "Paper endpoint must start with paper/"
            raise ValueError(msg)
        paper_url = f"{self.url}{self.paper_url_path}"
        response = requests.get(paper_url, timeout=self.time_out_seconds)
        if response.status_code == NOT_FOUND_STATUS_CODE:
            msg = f"Paper url path {paper_url} not found"
            raise ValueError(msg)
        return self

    def get_all_paper_info(self) -> dict[str, Any]:
        """Get all the paper info."""
        paper_info = {}
        paper_response = self._connect_to_paper()
        page_content = BeautifulSoup(paper_response.content, "html.parser")
        paper_info["pdf_url"] = self._get_pdf_url(page_content)
        paper_info["official implementation"] = self._get_official_code_url(page_content)
        paper_info["abstract"] = self._get_abstract(page_content)
        return paper_info

    def _connect_to_paper(self) -> requests.Response:
        """Connect to the paper."""
        paper_url = f"{self.url}{self.paper_url_path}"
        response = requests.get(paper_url, timeout=self.time_out_seconds)
        if response.status_code != SUCCESS_STATUS_CODE:
            msg = f"Request to {paper_url} returned status code {response.status_code}"
            raise ValueError(msg)
        return response

    @staticmethod
    @check_for_not_found
    def _get_pdf_url(page_content: BeautifulSoup) -> str:
        """Get the pdf url.

        Args:
            page_content (BeautifulSoup): Content of the paper's page.

        Returns:
            str : Paper's pdf url
        """
        abstract_section = page_content.find("div", {"class": "paper-abstract"})
        urls = abstract_section.find_all("a", {"class": "badge badge-light"})
        for url_raw in urls:
            if utils.clean_str_tag_text(url_raw.text) == "PDF":
                return str(url_raw["href"])
        msg = "PDF url not found"
        raise PaperAttributeNotFoundError(msg)

    @staticmethod
    @check_for_not_found
    def _get_abstract(page_content: BeautifulSoup) -> str:
        """Get the abstract.

        Args:
            page_content (BeautifulSoup): Content of the paper's page.

        Returns:
            str : Paper's abstract on paperswithcode website.
        """
        abstract_section = page_content.find("div", {"class": "paper-abstract"})
        return utils.clean_str_tag_text(abstract_section.find("p").text)

    @staticmethod
    @check_for_not_found
    def _get_official_code_url(page_content: BeautifulSoup) -> str:
        """Get the offical paper url.

        Args:
            page_content (BeautifulSoup): Content of the paper's page.

        Returns:
            str : Paper's official code url.
        """
        implementations_table = page_content.find("div", {"id": "implementations-short-list"})
        all_implementations = implementations_table.find_all("div", {"class": "row"})
        for implementation in all_implementations:
            if implementation.find("span", {"class": "badge badge-info is-official-code"}):
                return str(implementation.find("a")["href"])
        msg = "Official code url not found"
        raise PaperAttributeNotFoundError(msg)
