"""Test ainewsbot."""

import ainewsbot


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(ainewsbot.__name__, str)
