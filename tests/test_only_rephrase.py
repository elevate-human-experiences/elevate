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
from elevate.only_rephrase import OnlyRephrase, RephraseConfig, RephraseInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_formal(settings: Any) -> None:
    """Test the rephrase_text method with a formal style."""
    input_message = """
    I need 2 days of sick leave.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="formal", length="lengthy")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Formal Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_informal(settings: Any) -> None:
    """Test the rephrase_text method with an informal style."""
    input_message = """
    I need 2 days of sick leave.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="informal", length="short")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Informal Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_urgent(settings: Any) -> None:
    """Test the rephrase_text method with an urgent style."""
    input_message = """
    This is a serious problem that needs to be addressed immediately.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="urgent", length="lengthy")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Urgent Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_enthusiastic(settings: Any) -> None:
    """Test the rephrase_text method with an enthusiastic style."""
    input_message = """
    I'm so excited about this project!
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="enthusiastic", length="medium")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Enthusiastic Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_informative(settings: Any) -> None:
    """Test the rephrase_text method with an informative style."""
    input_message = """
    The system utilizes a multi-threaded architecture to improve performance.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="informative", length="lengthy")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Informative Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_apologetic(settings: Any) -> None:
    """Test the rephrase_text method with an apologetic style."""
    input_message = """
    I apologize for the delay in my response. I understand that this has caused inconvenience, and I am truly sorry.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="apologetic", length="lengthy")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Apologetic Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_friendly(settings: Any) -> None:
    """Test the rephrase_text method with a friendly style."""
    input_message = """
    Hey, let's catch up over coffee sometime soon.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="friendly", length="short")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Friendly Rephrase:\n%s", rephrased_text)


@pytest.mark.asyncio  # type: ignore
async def test_rephase_text_technical(settings: Any) -> None:
    """Test the rephrase_text method with a technical style."""
    input_message = """
    Our application leverages containerization and orchestration to optimize deployment pipelines.
    """
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)
    input_data = RephraseInput(message=input_message, tone="technical", length="detailed")
    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Technical Rephrase:\n%s", rephrased_text)
