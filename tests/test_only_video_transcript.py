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

"""Module to test video transcript analysis functionality for real user scenarios."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_video_transcript import OnlyVideoTranscript, VideoTranscriptConfig, VideoTranscriptInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_student_analyzing_lecture_recording(settings: Any) -> None:
    """Test a student reviewing a missed calculus lecture to prepare for an exam."""
    config = VideoTranscriptConfig(model=settings.with_model)
    analyzer = OnlyVideoTranscript(config=config)

    # Realistic lecture transcript
    transcript = """
    Good morning everyone. Today we're covering derivatives and their applications in calculus.
    Remember, a derivative represents the rate of change of a function at any given point.
    Think of it like the speedometer in your car - it tells you how fast you're going at that exact moment.

    The power rule is your best friend here. If you have x to the n, the derivative is n times x to the n minus one.
    So x squared becomes 2x, x cubed becomes 3x squared, and so on.

    For your homework this week, practice problems 15 through 30 in chapter 4.
    There will be a quiz on Friday covering everything we've discussed today.
    Make sure you understand the chain rule - it will definitely be on your midterm exam next month.

    Office hours are Tuesday and Thursday from 2 to 4 PM if you need extra help.
    """

    input_data = VideoTranscriptInput(
        transcript=transcript,
        purpose="study for upcoming calculus exam",
        context="missed lecture due to illness",
        focus_areas=["key formulas", "homework assignments", "exam information"],
        time_available="standard",
    )

    result = await analyzer.analyze(input_data)

    assert result.summary is not None
    assert len(result.key_insights) > 0
    assert "derivatives" in result.summary.lower() or any(
        "derivative" in insight.lower() for insight in result.key_insights
    )
    assert result.content_type == "educational"
    assert len(result.action_items) > 0
    logger.debug(f"Analysis: {result.summary}")


@pytest.mark.asyncio  # type: ignore
async def test_professional_reviewing_missed_team_meeting(settings: Any) -> None:
    """Test a professional catching up on a project planning meeting they missed."""
    config = VideoTranscriptConfig(model=settings.with_model)
    analyzer = OnlyVideoTranscript(config=config)

    # Realistic meeting transcript
    transcript = """
    Alright everyone, let's start our weekly project sync. Sarah, can you give us an update on the mobile app redesign?

    Sure, we've completed the user research phase and identified three key pain points in the current interface.
    Users are struggling with the checkout process, the search functionality is confusing, and the navigation feels cluttered.

    Based on these findings, I recommend we prioritize the checkout flow redesign first.
    We should be able to complete that by the end of next week if we get approval from the design team.

    Mike, can you work with Sarah on the technical requirements? We'll need to make sure the backend can handle the new payment integration.
    Also, let's schedule a client review meeting for Friday to show them our progress.

    Action items: Sarah will create mockups by Wednesday, Mike will review technical specs by Thursday,
    and I'll reach out to the client to confirm the Friday meeting time.

    Any questions before we move on to the budget discussion?
    """

    input_data = VideoTranscriptInput(
        transcript=transcript,
        purpose="catch up on project status and my responsibilities",
        context="team planning meeting I missed due to client call",
        focus_areas=["action items", "deadlines", "my tasks"],
        time_available="quick",
    )

    result = await analyzer.analyze(input_data)

    assert result.summary is not None
    assert len(result.action_items) > 0
    assert result.content_type == "meeting"
    assert any("friday" in action.lower() for action in result.action_items) or any(
        "friday" in step.lower() for step in result.next_steps
    )
    logger.debug(f"Action items found: {result.action_items}")


@pytest.mark.asyncio  # type: ignore
async def test_researcher_analyzing_conference_presentation(settings: Any) -> None:
    """Test a researcher extracting insights from a conference keynote for their literature review."""
    config = VideoTranscriptConfig(model=settings.with_model)
    analyzer = OnlyVideoTranscript(config=config)

    # Realistic conference presentation transcript
    transcript = """
    Thank you for that introduction. Today I want to discuss our recent findings on sustainable urban development
    and how AI can help cities become more environmentally efficient.

    Our research team analyzed data from 50 cities worldwide over the past three years.
    We found that cities implementing AI-driven traffic management reduced carbon emissions by an average of 23%.

    The key insight here is that small, data-driven optimizations can have massive cumulative effects.
    For example, optimizing traffic light timing based on real-time traffic patterns not only reduces emissions
    but also improves quality of life for residents.

    I want to emphasize three critical success factors we identified:
    First, cities need robust data collection infrastructure.
    Second, they must invest in training local staff to maintain these systems.
    Third, and this is crucial, they need to engage with residents throughout the implementation process.

    We're planning to publish our full methodology and results in the Journal of Urban Studies next quarter.
    I encourage you to follow our ongoing work at the Sustainable Cities Research Institute.
    """

    input_data = VideoTranscriptInput(
        transcript=transcript,
        purpose="gather insights for my urban planning research paper",
        context="conference keynote on AI and sustainability",
        focus_areas=["research findings", "methodology", "key statistics"],
        time_available="detailed",
    )

    result = await analyzer.analyze(input_data)

    assert result.summary is not None
    assert len(result.key_insights) > 0
    assert result.content_type == "presentation"
    assert "23%" in result.summary or any("23%" in insight for insight in result.key_insights)
    assert len(result.related_topics) > 0
    logger.debug(f"Key insights: {result.key_insights}")


@pytest.mark.asyncio  # type: ignore
async def test_empty_transcript_validation(settings: Any) -> None:
    """Test that empty or whitespace-only transcripts raise appropriate errors."""
    config = VideoTranscriptConfig(model=settings.with_model)
    analyzer = OnlyVideoTranscript(config=config)

    # Test completely empty string
    input_data = VideoTranscriptInput(transcript="", purpose="test validation", context="unit test")
    with pytest.raises(ValueError, match="Transcript cannot be empty or contain only whitespace"):
        await analyzer.analyze(input_data)

    # Test whitespace-only string
    input_data = VideoTranscriptInput(transcript="   \n  \t  ", purpose="test validation", context="unit test")
    with pytest.raises(ValueError, match="Transcript cannot be empty or contain only whitespace"):
        await analyzer.analyze(input_data)


@pytest.mark.asyncio  # type: ignore
async def test_parent_reviewing_school_board_meeting(settings: Any) -> None:
    """Test a parent analyzing a school board meeting to understand policy changes affecting their child."""
    config = VideoTranscriptConfig(model=settings.with_model)
    analyzer = OnlyVideoTranscript(config=config)

    # Realistic school board meeting transcript
    transcript = """
    Good evening everyone. Tonight we're discussing several important policy changes for the upcoming school year.

    First, we're implementing a new homework policy across all grade levels.
    Elementary students will have no more than 30 minutes of homework per night,
    middle school students no more than 60 minutes, and high school students no more than 90 minutes.

    This change takes effect immediately when school starts in September.
    Teachers will receive training on how to design meaningful assignments within these time limits.

    Second, we're introducing a new technology policy regarding cell phones and tablets.
    Students in grades K-5 will not be permitted to bring personal devices to school.
    Grades 6-8 may bring devices but they must remain in lockers during class time.
    High school students may use devices during lunch and between classes only.

    Parents, please make sure to review these policies with your children before the school year begins.
    We'll be sending home detailed information packets next week.
    Any violations of these policies will result in the device being confiscated until a parent can retrieve it.
    """

    input_data = VideoTranscriptInput(
        transcript=transcript,
        purpose="understand new school policies that will affect my 7th-grade daughter",
        context="school board meeting about policy changes",
        focus_areas=["homework policy", "technology rules", "what I need to do as a parent"],
        time_available="standard",
    )

    result = await analyzer.analyze(input_data)

    assert result.summary is not None
    assert len(result.action_items) > 0
    assert result.content_type == "meeting"
    assert "60 minutes" in result.summary or any("60 minutes" in insight for insight in result.key_insights)
    logger.debug(f"Parent action items: {result.action_items}")
