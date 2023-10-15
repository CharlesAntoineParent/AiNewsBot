"""This module create the exceptions for the paperswithcode.com scrapper."""


class PapersWithCodeNoResponseTimeOutError(Exception):
    """Exception raised when a request to paperswithcode.com times out and no response is received.

    Attributes:
        message: Explanation of the error.
    """


class PaperAttributeNotFoundError(Exception):
    """Exception raised when a request to paperswithcode.com times out and no response is received.

    Attributes:
        message: Explanation of the error.
    """
