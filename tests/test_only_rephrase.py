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

"""Test real-world communication scenarios that users face every day."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_rephrase import OnlyRephrase, RephraseConfig, RephraseInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_requesting_time_off_from_boss(settings: Any) -> None:
    """Test helping someone request time off professionally."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="Hi, I need to take next Friday off. My cousin is getting married.",
        audience="my manager",
        purpose="request time off",
        tone="professional",
        format="email",
        context="It's short notice and we have a big project due soon",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Professional time-off request:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_apologizing_for_project_delay(settings: Any) -> None:
    """Test helping someone apologize professionally for a delayed project."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="Sorry the report is late. Had some technical issues.",
        audience="client",
        purpose="explain delay and apologize",
        tone="apologetic but professional",
        format="email",
        context="This is the second delay this month and the client is getting frustrated",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Professional apology for delay:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_following_up_with_unresponsive_client(settings: Any) -> None:
    """Test helping someone follow up without being pushy."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="Hi, just checking in on the proposal I sent last week. Haven't heard back.",
        audience="potential client",
        purpose="get a response to my proposal",
        tone="friendly but persistent",
        format="email",
        context="They seemed very interested in our meeting but have gone quiet since I sent the proposal",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Client follow-up:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_asking_for_salary_raise(settings: Any) -> None:
    """Test helping someone request a raise confidently."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="I think I deserve a raise. I've been working really hard.",
        audience="my boss",
        purpose="request a salary increase",
        tone="confident and professional",
        format="email",
        context="I've been here 2 years, took on extra responsibilities, and haven't had a raise yet",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Salary raise request:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_declining_extra_work_politely(settings: Any) -> None:
    """Test helping someone say no to additional work diplomatically."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="I can't take on another project right now. I'm already swamped.",
        audience="my colleague",
        purpose="decline additional work",
        tone="helpful but firm",
        format="email",
        context="They always ask me for help and I have trouble saying no, but I'm really overloaded",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Polite work decline:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_sharing_good_news_with_team(settings: Any) -> None:
    """Test helping someone share success with their team."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="We got the big client! This is huge for our team.",
        audience="my team members",
        purpose="share exciting news",
        tone="enthusiastic but professional",
        format="team message",
        context="This client has been a long-term goal and everyone worked hard on the pitch",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Team success announcement:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_rescheduling_important_meeting(settings: Any) -> None:
    """Test helping someone reschedule a meeting professionally."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="Something came up and I need to move our meeting tomorrow.",
        audience="important client",
        purpose="reschedule our meeting",
        tone="apologetic and accommodating",
        format="email",
        context="This is a quarterly business review that was scheduled weeks ago",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Meeting reschedule:\n%s", rephrased_text)
    assert len(rephrased_text) > 50


@pytest.mark.asyncio  # type: ignore
async def test_explaining_mistake_to_boss(settings: Any) -> None:
    """Test helping someone explain a work mistake honestly."""
    config = RephraseConfig(model=settings.with_model)
    only_rephrase = OnlyRephrase(config=config)

    input_data = RephraseInput(
        original_text="I messed up the client presentation. Wrong data got included.",
        audience="my manager",
        purpose="explain what went wrong and take responsibility",
        tone="accountable and solution-focused",
        format="email",
        context="The client noticed during the meeting and it was embarrassing for everyone",
    )

    result = await only_rephrase.rephrase_text(input_data)
    rephrased_text = result.rephrased_text
    logger.debug("Mistake explanation:\n%s", rephrased_text)
    assert len(rephrased_text) > 50
