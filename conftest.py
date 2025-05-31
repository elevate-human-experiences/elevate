from dataclasses import dataclass

import pytest


@dataclass
class Settings:
    with_model: str
    # You can add other fields here if you need to pass more config


def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Register a command-line option `--with-model` so that running
        pytest --with-model=chatgpt
    will set `config.getoption("with_model") == "chatgpt"`.
    """
    parser.addoption(
        "--with-model",
        action="store",
        default="chatgpt",
        help="Name of the model to use (e.g. chatgpt, claude, gemini, etc.)",
    )


@pytest.fixture(scope="session")  # type: ignore
def settings(pytestconfig: pytest.Config) -> Settings:
    """
    A fixture that returns a Settings object. Tests can do:

        def test_foo(settings):
            model = settings.model_name
            ...
    """
    with_model = pytestconfig.getoption("with_model")
    import logging

    logger = logging.getLogger(__name__)
    logger.info(f"Using model: {with_model}")
    return Settings(with_model=with_model)
