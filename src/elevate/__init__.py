"""Elevate package."""

from .only_json import OnlyJson


def hello() -> str:
    """Return a greeting."""
    return "Hello from elevate!"


__all__ = ["OnlyJson", "hello"]
