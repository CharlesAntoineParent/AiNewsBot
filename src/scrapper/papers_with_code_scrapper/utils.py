"""This module implements utils function for scrappers."""


def clean_str_tag_text(text: str) -> str:
    """Cleans the text of a tag.

    Args:
        text (str): The text to clean.

    Returns:
        str: The cleaned text.
    """
    return text.strip().replace("\n", "")


def clean_digit_tag_text(text: str) -> float:
    """Cleans str digits of a tag.

    Args:
        text (str): The text representing a float to clean.

    Returns:
        float: The cleaned float in the text.
    """
    str_digit = clean_str_tag_text(text)
    str_digit = str_digit.replace(",", "")
    return float(str_digit)
