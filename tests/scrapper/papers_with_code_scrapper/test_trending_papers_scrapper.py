# ruff: noqa : SLF001
"""Test the PapersWithCodeTrendingScrapper class."""
import datetime

import bs4
import pytest
import requests
import vcr

from scrapper.papers_with_code_scrapper import PapersWithCodeTrendingScrapper

PAPERSWITH_CODE_CASSETTE_PATH = (
    "tests/scrapper/papers_with_code_scrapper/fixtures/vcr_cassettes/test_get_page_papers.yaml"
)
PAPERSWITH_CODE_ENDPOINT = "https://paperswithcode.com/"


class TestPapersWithCodeTrendingScrapper:
    """This class tests the PapersWithCodeTrendingScrapper class."""

    @pytest.fixture()
    def instanciante_papers_with_code_trending_scrapper(self) -> PapersWithCodeTrendingScrapper:
        """Fixture a PapersWithCodeTrendingScrapper instance."""
        return PapersWithCodeTrendingScrapper()

    @pytest.fixture()
    def paper_tag(self) -> bs4.element.Tag:
        """Fixture a paper tag."""
        with vcr.use_cassette("tests/scrapper/papers_with_code_scrapper/fixtures/paper_tag.html"):
            response = requests.get(PAPERSWITH_CODE_ENDPOINT, timeout=10)
            page_content = bs4.BeautifulSoup(response.content, "html.parser")
            paper_contents = page_content.find_all(
                "div", {"class": "row infinite-item item paper-card"}
            )
            yield paper_contents[0]

    @vcr.use_cassette(PAPERSWITH_CODE_CASSETTE_PATH)
    def test_get_paper_papers(
        self,
        monkeypatch: pytest.MonkeyPatch,
        instanciante_papers_with_code_trending_scrapper: PapersWithCodeTrendingScrapper,
    ) -> None:
        """Test that the get_paper_titles method returns a list of paper titles."""
        monkeypatch.setattr(
            PapersWithCodeTrendingScrapper,
            "_raw_paper_content_to_dict",
            lambda x: {},
        )
        expected_length: int = 9
        paper_titles = instanciante_papers_with_code_trending_scrapper.get_page_papers(0)
        assert isinstance(paper_titles, list)
        assert isinstance(paper_titles[0], dict)
        assert len(paper_titles) == expected_length

    def test_get_nb_stars(
        self,
        paper_tag: bs4.element.Tag,
    ) -> None:
        """Test that the get_nb_stars method returns the correct number of stars."""
        expected_nb_stars: int = 855
        nb_stars = PapersWithCodeTrendingScrapper._get_nb_stars(paper_tag)
        assert isinstance(nb_stars, int)
        assert nb_stars == expected_nb_stars

    def test_get_nb_stars_per_minutes(self, paper_tag: bs4.element.Tag) -> None:
        """Test that the get_nb_stars_per_minutes method returns the correct number of stars."""
        expected_nb_stars_per_minutes: float = 5.83
        nb_stars_per_minutes = PapersWithCodeTrendingScrapper._get_nb_stars_per_minutes(paper_tag)
        assert isinstance(nb_stars_per_minutes, float)
        assert nb_stars_per_minutes == expected_nb_stars_per_minutes

    def test_get_paper_path(
        self,
        paper_tag: bs4.element.Tag,
    ) -> None:
        """Test that the get_nb_stars method returns the correct number of stars."""
        expected_paper_path: str = "/paper/dreamgaussian-generative-gaussian-splatting"
        paper_path = PapersWithCodeTrendingScrapper._get_paper_url(paper_tag)
        assert paper_path == expected_paper_path

    def test_get_paper_titles(
        self,
        paper_tag: bs4.element.Tag,
    ) -> None:
        """Test that the get_nb_stars method returns the correct number of stars."""
        expected_paper_title: str = (
            "DreamGaussian: Generative Gaussian Splatting for Efficient 3D Content Creation"
        )
        paper_title = PapersWithCodeTrendingScrapper._get_paper_title(paper_tag)
        assert paper_title == expected_paper_title

    def test_get_publication_date(
        self,
        paper_tag: bs4.element.Tag,
    ) -> None:
        """Test that the get_nb_stars method returns the correct number of stars."""
        expected_publication_date: datetime.datetime = datetime.datetime(2023, 9, 28).astimezone(
            datetime.timezone.utc
        )
        publication_date = PapersWithCodeTrendingScrapper._get_publication_date(paper_tag)
        assert publication_date == expected_publication_date
