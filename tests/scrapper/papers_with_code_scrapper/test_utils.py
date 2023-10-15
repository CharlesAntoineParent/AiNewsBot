# ruff: noqa : SLF001
"""This file test the paper with code scrapper utils."""

from scrapper.papers_with_code_scrapper import utils

PAPERSWITH_CODE_CASSETTE_PATH = (
    "tests/papers_with_code_scrapper/fixtures/vcr_cassettes/test_get_page_papers.yaml"
)
PAPERSWITH_CODE_ENDPOINT = "https://paperswithcode.com/"


class TestScrapperUtils:
    """This class tests the paperswithcode scrapper utils."""

    def test_clean_digit_tag_text_coma(
        self,
    ) -> None:
        """Test that the get_nb_stars method returns the correct number of stars."""
        raw_value = "          1,000,000.00     "
        expected_value = 1000000.0
        converted_value = utils.clean_digit_tag_text(raw_value)
        assert converted_value == expected_value

    def test_clean_digit_tag_text_float(
        self,
    ) -> None:
        """Test that the get_nb_stars method returns the correct number of stars."""
        raw_value = "          200.67     "
        expected_value = 200.67
        converted_value = utils.clean_digit_tag_text(raw_value)
        assert converted_value == expected_value
