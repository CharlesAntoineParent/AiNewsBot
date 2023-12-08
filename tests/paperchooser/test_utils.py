"""This module contains tests for the utils module."""
import datetime

import pytest

from paperchooser.utils import convert_iso_date


def test_convert_iso_date() -> None:
    """Test valid ISO date."""
    iso_date = "2022-01-01T00:00:00Z"
    expected_datetime = datetime.datetime(2022, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
    assert convert_iso_date(iso_date) == expected_datetime


def test_convert_iso_date_invalid() -> None:
    """Test invalid ISO date."""
    iso_date = "2022-01-0100:00:00"
    with pytest.raises(ValueError, match="Invalid ISO date"):
        convert_iso_date(iso_date)
