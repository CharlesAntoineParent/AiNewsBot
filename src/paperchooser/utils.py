"""Defines utility functions for the paperchooser package."""
from datetime import datetime


def convert_iso_date(iso_date: str) -> datetime:
    """Convert an ISO date to a datetime object.

    Args:
        iso_date (str): ISO date.

    Returns:
        datetime: Datetime object.
    """
    try:
        input_date_str = iso_date.replace("Z", "+00:00")
        input_datetime = datetime.fromisoformat(input_date_str)
    except ValueError as e:
        msg = f"Invalid ISO date: {iso_date}"
        raise ValueError(msg) from e
    return input_datetime
