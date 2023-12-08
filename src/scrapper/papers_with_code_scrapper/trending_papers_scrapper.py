"""This module contains a class for scraping trending papers from paperswithcode.com."""
import datetime
import logging
from functools import wraps
from typing import Any, Callable, Dict, List

import bs4
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from scrapper.papers_with_code_scrapper import PapersWithCodeNoResponseTimeOutError, utils

SUCCESS_STATUS_CODE = 200
DATE_FORMAT = "%d %b %Y"


def check_status_code(url: str, time_out_seconds: float) -> Callable[..., Any]:
    """A decorator that checks the status code of a HTTP response.

    Args:
        url (str): The URL to check.
        time_out_seconds (float): The time out in seconds.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """A decorator that checks the status code of a HTTP response.

        Args:
            func: The function to decorate.

        Returns:
            The decorated function.
        """

        @wraps(func)
        def wrapper(self: object, *args: Any, **kwargs: Any) -> Any:
            response = requests.get(url, timeout=time_out_seconds)
            if response.status_code != SUCCESS_STATUS_CODE:
                msg = f"Request to {url} returned status code {response.status_code}"
                raise PapersWithCodeNoResponseTimeOutError(msg)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class PapersWithCodeTrendingScrapper(BaseModel):
    """A class for scraping trending papers from paperswithcode.com.

    Attributes:
        max_number_of_papers (int): The maximum number of papers to retrieve.
        url (str): The URL of the Papers with Code website.
    """

    time_out_seconds: int = 20
    url: str = "https://paperswithcode.com/"

    @check_status_code(url, time_out_seconds)
    def get_best_papers(self, nb_papers: int = 10) -> List[Dict[str, Any]]:
        """Retrieves a list of paper titles from the Papers with Code website.

        Args:
            nb_papers (int): Number of papers to get

        Returns:
            List[Dict[str, Any]]: List of infos of the best papers.
        """
        papers: List[Dict[str, Any]] = []
        page_number = 0
        while len(papers) < nb_papers:
            page_number += 1
            page_papers = self.get_page_papers(page_number)
            papers.extend(page_papers)
        return papers[:nb_papers]

    @check_status_code(url, time_out_seconds)
    def get_page_papers(self, page_number: int) -> List[Dict[str, Any]]:
        """Retrieves a list of paper titles from a specified page on the Papers with Code website.

        Args:
            page_number (int): The page number to retrieve papers from.

        Returns:
            List[Dict[str, Any]]: List of infos of the best papers.
        """
        endpoint = f"{self.url}?page={page_number}"
        response = requests.get(endpoint, timeout=self.time_out_seconds)
        soup = BeautifulSoup(response.content, "html.parser")
        raw_paper_content = soup.find_all("div", {"class": "row infinite-item item paper-card"})

        return [
            PapersWithCodeTrendingScrapper._raw_paper_content_to_dict(paper)
            for paper in raw_paper_content
        ]

    @staticmethod
    def _raw_paper_content_to_dict(raw_paper_content: bs4.element.Tag) -> Dict[str, Any]:
        """Converts raw paper content to a dictionary.

        Args:
            raw_paper_content (bs4.element.Tag): The raw paper content to convert.

        Returns:
            Dict[str, Any]: The converted raw paper content.
        """
        try:
            paper_dict: Dict[str, Any] = {}
            paper_dict["Title"] = PapersWithCodeTrendingScrapper._get_paper_title(raw_paper_content)
            paper_dict["URL"] = PapersWithCodeTrendingScrapper._get_paper_url(raw_paper_content)
            paper_dict["Publication date"] = PapersWithCodeTrendingScrapper._get_publication_date(
                raw_paper_content
            )
            paper_dict["Stars"] = PapersWithCodeTrendingScrapper._get_nb_stars(raw_paper_content)
            paper_dict["Stars per hour"] = PapersWithCodeTrendingScrapper._get_nb_stars_per_minutes(
                raw_paper_content
            )
        except Exception:  # noqa: BLE001
            logging.warning("Error while parsing paper content")
        return paper_dict

    @staticmethod
    def _get_paper_url(raw_paper_content: bs4.element.Tag) -> str:
        """Retrieves the URL of the paper.

        Args:
            raw_paper_content (bs4.elelemt.Tag): The raw paper content

        Returns:
            str: The URL of the paper.
        """
        title_raw = raw_paper_content.find("h1").find("a")
        title: str = title_raw["href"]
        return title

    @staticmethod
    def _get_paper_title(raw_paper_content: bs4.element.Tag) -> str:
        """Retrieves the title of the paper.

        Args:
            raw_paper_content (bs4.elelemt.Tag): The raw paper content

        Returns:
            str: The name of the paper.
        """
        raw_title: str = raw_paper_content.find("h1").text
        return utils.clean_str_tag_text(raw_title)

    @staticmethod
    def _get_publication_date(raw_paper_content: bs4.element.Tag) -> datetime.datetime:
        """Retrieves the publication date of the paper.

        Args:
            raw_paper_content (bs4.elelemt.Tag): The raw paper content

        Returns:
            str: The publication date of the paper.
        """
        publication_date_raw = raw_paper_content.find(
            "span", class_="author-name-text item-date-pub"
        ).text
        str_date = utils.clean_str_tag_text(publication_date_raw)
        date = datetime.datetime.strptime(str_date, DATE_FORMAT).astimezone(datetime.timezone.utc)
        return date

    @staticmethod
    def _get_nb_stars(raw_paper_content: bs4.element.Tag) -> int:
        """Retrieves the number of stars for a paper.

        Args:
            raw_paper_content (bs4.elelemt.Tag): The raw paper content

        Returns:
            int: The number of stars for the paper.
        """
        raw_value = raw_paper_content.find("span", class_="badge badge-secondary").text
        float_value = utils.clean_digit_tag_text(raw_value)
        return int(float_value)

    @staticmethod
    def _get_nb_stars_per_minutes(raw_paper_content: bs4.element.Tag) -> float:
        """Retrieves the number of stars per minutes for a paper.

        Args:
            raw_paper_content (bs4.elelemt.Tag): The raw paper content

        Returns:
            float: The number of stars per minutes for the paper.
        """
        nb_stars_per_hours_raw = raw_paper_content.find(
            "div", class_="stars-accumulated text-center"
        ).text
        nb_stars_per_hours_raw = nb_stars_per_hours_raw.replace("stars / hour", "")
        nb_stars_per_hours = utils.clean_digit_tag_text(nb_stars_per_hours_raw)
        return nb_stars_per_hours
