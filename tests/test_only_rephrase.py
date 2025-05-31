# MIT License
#
# Copyright (c) 2025 elevate-human-experiences
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module to test the text rephrasing functionalities of the OnlyRephrase class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_rephrase import OnlyRephrase


logger = setup_logging(logging.DEBUG)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_formal(settings: Any) -> None:
    """Test the rephrase_text method with a formal style."""
    input_message = """
    I need 2 days of sick leave.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = await only_rephrase.rephrase_text(input_message, "formal", "lengthy")
    logger.debug("Formal Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_informal(settings: Any) -> None:
    """Test the rephrase_text method with an informal style."""
    input_message = """
    I need 2 days of sick leave.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = await only_rephrase.rephrase_text(input_message, "informal", "short")
    logger.debug("Informal Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_urgent(settings: Any) -> None:
    """Test the rephrase_text method with an urgent style."""
    input_message = """
    This is a serious problem that needs to be addressed immediately.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = await only_rephrase.rephrase_text(input_message, "urgent", "lengthy")
    logger.debug("Urgent Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_enthusiastic(settings: Any) -> None:
    """Test the rephrase_text method with an enthusiastic style."""
    input_message = """
    I'm so excited about this project!
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = await only_rephrase.rephrase_text(input_message, "enthusiastic", "medium")
    logger.debug("Enthusiastic Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_informative(settings: Any) -> None:
    """Test the rephrase_text method with an informative style."""
    input_message = """
    The system utilizes a multi-threaded architecture to improve performance.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = await only_rephrase.rephrase_text(input_message, "informative", "lengthy")
    logger.debug("Informative Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_apologetic(settings: Any) -> None:
    """Test the rephrase_text method with an apologetic style."""
    input_message = """
    I apologize for the delay in my response. I understand that this has caused inconvenience, and I am truly sorry.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = await only_rephrase.rephrase_text(input_message, "apologetic", "lengthy")
    logger.debug("Apologetic Rephrase:\n%s", rephrased_text)


def test_rephase_text_friendly(settings: Any) -> None:
    """Test the rephrase_text method with a friendly style."""
    input_message = """
    Hey, let's catch up over coffee sometime soon.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = only_rephrase.rephrase_text(input_message, "friendly", "short")
    logger.debug("Friendly Rephrase:\n%s", rephrased_text)


def test_rephase_text_technical(settings: Any) -> None:
    """Test the rephrase_text method with a technical style."""
    input_message = """
    Our application leverages containerization and orchestration to optimize deployment pipelines.
    """
    only_rephrase = OnlyRephrase(with_model=settings.with_model)
    rephrased_text = only_rephrase.rephrase_text(input_message, "technical", "detailed")
    logger.debug("Technical Rephrase:\n%s", rephrased_text)
