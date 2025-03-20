"""Test the elevate module."""


def test_elevate() -> None:
    """Test the elevate module."""
    from elevate import hello

    assert hello() == "Hello from elevate!"
