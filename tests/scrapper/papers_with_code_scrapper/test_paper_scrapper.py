"""Test the PapersWithCodePaperScrapper class."""
# ruff: noqa : SLF001
from typing import Any

import pytest
import requests
import vcr
from bs4 import BeautifulSoup

from scrapper.papers_with_code_scrapper import (
    PaperAttributeNotFoundError,
    PapersWithCodePaperScrapper,
    utils,
)


def mock_raise_attribute_error(*args: Any, **kwargs: Any) -> None:
    """Mock a raise AttributeError."""
    msg = "NoneType object has no attribute 'find'"
    raise AttributeError(msg)


PAPERS_WITH_CODE_URL = "https://paperswithcode.com/"

PAPER_W_OFFICIAL_CODE_CASSETTE_PATH = (
    "tests/scrapper/papers_with_code_scrapper/fixtures/vcr_cassettes/paper_w_code.yaml"
)
PAPER_W_OFFICIAL_CODE = "paper/dreamgaussian-generative-gaussian-splatting"

PAPER_WO_OFFICIAL_CODE_CASSETTE_PATH = (
    "tests/scrapper/papers_with_code_scrapper/fixtures/vcr_cassettes/paper_wo_code.yaml"
)
PAPER_WO_OFFICIAL_CODE = "paper/searching-for-mobilenetv3"


def mock_bad_response(*args: Any, **kwargs: Any) -> requests.Response:
    """Mock a request bad response."""
    response = requests.Response()
    response.status_code = 404
    return response


def mock_good_reponse(*args: Any, **kwargs: Any) -> requests.Response:
    """Mock a request good response."""
    response = requests.Response()
    response.status_code = 200
    return response


class TestPapersWithCodePaperScrapper:
    """This class tests the PapersWithCodePaperScrapper class."""

    @pytest.fixture()
    def paper_scrapper(self, monkeypatch: pytest.MonkeyPatch) -> PapersWithCodePaperScrapper:
        """Return a PapersWithCodePaperScrapper instance."""
        with monkeypatch.context() as m:
            m.setattr(requests, "get", mock_good_reponse)
            instance = PapersWithCodePaperScrapper(paper_url_path=PAPER_W_OFFICIAL_CODE)
        return instance

    @pytest.fixture()
    def paper_page_content(self) -> BeautifulSoup:
        """Return a paper page content with everything."""
        paper_url = f"{PAPERS_WITH_CODE_URL}{PAPER_W_OFFICIAL_CODE}"
        with vcr.use_cassette(PAPER_W_OFFICIAL_CODE_CASSETTE_PATH):
            response = requests.get(paper_url, timeout=10)
            page_content = BeautifulSoup(response.content, "html.parser")
        return page_content

    @pytest.fixture()
    def paper_page_content_no_code(self) -> BeautifulSoup:
        """Return a paper page content of a paper without official code."""
        paper_url = f"{PAPERS_WITH_CODE_URL}{PAPER_WO_OFFICIAL_CODE}"
        with vcr.use_cassette(PAPER_WO_OFFICIAL_CODE_CASSETTE_PATH):
            response = requests.get(paper_url, timeout=10)
            page_content = BeautifulSoup(response.content, "html.parser")
        return page_content

    def test_init_not_found_url_path(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test init PapersWithCodePaperScrapper not found error."""
        monkeypatch.setattr(requests, "get", mock_bad_response)
        with pytest.raises(ValueError, match="Paper url path .* not found"):
            PapersWithCodePaperScrapper(paper_url_path="paper/test")

    def test_init_bad_path(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test init PapersWithCodePaperScrapper bad path error."""
        monkeypatch.setattr(requests, "get", mock_bad_response)
        with pytest.raises(ValueError, match="Paper endpoint must start with paper/"):
            PapersWithCodePaperScrapper(paper_url_path="wrongpath/test")

    @vcr.use_cassette(PAPER_W_OFFICIAL_CODE_CASSETTE_PATH)
    def test_init_valid(
        self,
    ) -> None:
        """Test the init method of the PapersWithCodePaperScrapper class."""
        PapersWithCodePaperScrapper(paper_url_path=PAPER_W_OFFICIAL_CODE)

    @vcr.use_cassette(PAPER_W_OFFICIAL_CODE_CASSETTE_PATH)
    def test_connect_to_paper_valid_url(self, paper_scrapper: PapersWithCodePaperScrapper) -> None:
        """Test that the connect_to_paper method returns a requests.Response object."""
        paper_response = paper_scrapper._connect_to_paper()
        assert isinstance(paper_response, requests.Response)

    @vcr.use_cassette(PAPER_W_OFFICIAL_CODE_CASSETTE_PATH)
    def test_connect_to_paper_invalid_url(
        self,
        paper_scrapper: PapersWithCodePaperScrapper,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that the connect_to_paper method returns a requests.Response object."""
        monkeypatch.setattr(requests, "get", mock_bad_response)
        with pytest.raises(ValueError, match="Request to .* returned status code .*"):
            paper_scrapper._connect_to_paper()

    def test_get_pdf_url(self, paper_page_content: BeautifulSoup) -> None:
        """Test that get pdf."""
        expected_url = "https://arxiv.org/pdf/2309.16653v1.pdf"
        pdf_url = PapersWithCodePaperScrapper._get_pdf_url(paper_page_content)
        assert pdf_url == expected_url

    def test_get_pdf_url_not_found(
        self, paper_page_content: BeautifulSoup, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test get the offical paper url error not found."""
        monkeypatch.setattr(
            utils,
            "clean_str_tag_text",
            lambda x: "NOTPDF",
        )
        with pytest.raises(PaperAttributeNotFoundError, match="PDF url not found"):
            PapersWithCodePaperScrapper._get_pdf_url(paper_page_content)

    def test_get_pdf_url_section_not_found(
        self, paper_page_content: BeautifulSoup, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test get pdf error not found."""
        monkeypatch.setattr(
            BeautifulSoup,
            "find",
            lambda *args, **kwargs: mock_raise_attribute_error(*args, **kwargs),
        )
        with pytest.raises(
            PaperAttributeNotFoundError,
            match="Element not found during scrapping (.*_get_pdf_url)",
        ):
            PapersWithCodePaperScrapper._get_pdf_url(paper_page_content)

    def test_get_abstract(self, paper_page_content: BeautifulSoup) -> None:
        """Test get the abstract."""
        expected_abstract_starts_with = "Recent advances in 3D content"
        expected_abstract_ends_with = "compared to existing methods."
        abstract: str = PapersWithCodePaperScrapper._get_abstract(paper_page_content)
        assert abstract.startswith(expected_abstract_starts_with)
        assert abstract.endswith(expected_abstract_ends_with)

    def test_get_abstract_not_found(
        self, paper_page_content: BeautifulSoup, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test get the abstract error not found."""
        monkeypatch.setattr(
            BeautifulSoup,
            "find",
            lambda *args, **kwargs: mock_raise_attribute_error(*args, **kwargs),
        )
        with pytest.raises(
            PaperAttributeNotFoundError,
            match="Element not found during scrapping (.*_get_abstract)",
        ):
            PapersWithCodePaperScrapper._get_abstract(paper_page_content)

    def test_get_official_code_url(self, paper_page_content: BeautifulSoup) -> None:
        """Test get the offical paper url."""
        expected_url = "https://github.com/dreamgaussian/dreamgaussian"
        url = PapersWithCodePaperScrapper._get_official_code_url(paper_page_content)
        assert url == expected_url

    def test_get_official_code_url_no_official(
        self, paper_page_content_no_code: BeautifulSoup
    ) -> None:
        """Test get the offical paper url error not found."""
        with pytest.raises(PaperAttributeNotFoundError, match="Official code url not found"):
            PapersWithCodePaperScrapper._get_official_code_url(paper_page_content_no_code)
