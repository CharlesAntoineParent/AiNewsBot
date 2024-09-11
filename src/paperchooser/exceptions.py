"""This module create the exceptions for the paperswithcode.com scrapper."""


class PaperAttributeNotFoundError(Exception):
    """Exception raised when a paper is passed trough paperchooser and has not the right form.

    Attributes:
        message: Explanation of the error.
    """
