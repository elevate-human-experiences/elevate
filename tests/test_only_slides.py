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

"""Module to test the slide generation functionality of the OnlySlides class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_slides import OnlySlides, SlidesConfig, SlidesInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_entrepreneur_pitch_to_investors(settings: Any) -> None:
    """Test realistic scenario: entrepreneur pitching sustainable app to investors."""
    config = SlidesConfig(model=settings.with_model)
    only_slides = OnlySlides(config=config)

    input_data = SlidesInput(
        topic="EcoTracker - an app that helps people reduce their carbon footprint through daily habit tracking",
        audience="potential investors",
        purpose="get seed funding for our startup",
        context="We've built an MVP and have 1000 beta users showing 40% weekly engagement",
        slide_count=6,
        style="professional",
    )

    result = await only_slides.generate_slides(input_data)
    logger.debug("Entrepreneur Pitch Slides:\n%s", result.slides)
    logger.debug("Insights: %s", result.key_insights)
    logger.debug("Tips: %s", result.presentation_tips)

    # Validate complete output structure
    assert result.slides is not None
    assert len(result.slides.strip()) > 0
    assert len(result.key_insights) >= 1
    assert len(result.presentation_tips) >= 1
    assert len(result.next_steps) >= 1
    assert "minute" in result.estimated_duration.lower()


@pytest.mark.asyncio  # type: ignore
async def test_sales_manager_presenting_to_enterprise_client(settings: Any) -> None:
    """Test realistic scenario: sales manager presenting cloud solution to IT director."""
    config = SlidesConfig(model=settings.with_model)
    only_slides = OnlySlides(config=config)

    input_data = SlidesInput(
        topic="CloudSync Pro - secure file sync solution that keeps your team's work safe and accessible",
        audience="IT directors and CTO",
        purpose="convince them to choose our solution over competitors",
        context="They're migrating from outdated file servers and need enterprise-grade security",
        slide_count=5,
        style="professional",
    )

    result = await only_slides.generate_slides(input_data)
    logger.debug("Sales Presentation Slides:\n%s", result.slides)

    # Validate structure
    assert result.slides is not None
    assert len(result.slides.strip()) > 0
    assert len(result.key_insights) >= 1
    assert len(result.presentation_tips) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_manager_explaining_new_system_to_team(settings: Any) -> None:
    """Test realistic scenario: manager introducing workflow automation to skeptical employees."""
    config = SlidesConfig(model=settings.with_model)
    only_slides = OnlySlides(config=config)

    input_data = SlidesInput(
        topic="TechFlow - the new automation tool that will save us hours each week",
        audience="my team members",
        purpose="get everyone excited about using this new system",
        context="Some people are worried it's too complicated or will replace their jobs",
        slide_count=4,
        style="casual",
    )

    result = await only_slides.generate_slides(input_data)
    logger.debug("Team Presentation Slides:\n%s", result.slides)

    # Validate structure
    assert result.slides is not None
    assert len(result.slides.strip()) > 0
    assert len(result.key_insights) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_student_presenting_research_to_professors(settings: Any) -> None:
    """Test realistic scenario: student presenting final project to academic panel."""
    config = SlidesConfig(model=settings.with_model)
    only_slides = OnlySlides(config=config)

    input_data = SlidesInput(
        topic="How AI can optimize energy usage in smart buildings",
        audience="my professors and classmates",
        purpose="demonstrate my research findings and get a good grade",
        context="This is my capstone project and I need to show both the technical work and real-world impact",
        slide_count=8,
        style="technical",
    )

    result = await only_slides.generate_slides(input_data)
    logger.debug("Student Research Slides:\n%s", result.slides)

    # Validate structure
    assert result.slides is not None
    assert len(result.slides.strip()) > 0
    assert len(result.key_insights) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_trainer_teaching_cybersecurity_to_remote_workers(settings: Any) -> None:
    """Test realistic scenario: corporate trainer educating employees about online security."""
    config = SlidesConfig(model=settings.with_model)
    only_slides = OnlySlides(config=config)

    input_data = SlidesInput(
        topic="Staying safe online while working from home",
        audience="remote employees from various departments",
        purpose="teach everyone essential security habits to protect our company",
        context="We've had some close calls with phishing emails and people need practical, easy-to-follow advice",
        slide_count=6,
        style="professional",
    )

    result = await only_slides.generate_slides(input_data)
    logger.debug("Training Slides:\n%s", result.slides)

    # Validate structure
    assert result.slides is not None
    assert len(result.slides.strip()) > 0
    assert len(result.key_insights) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_quick_informal_presentation_to_friends(settings: Any) -> None:
    """Test realistic scenario: casual presentation about a simple app idea."""
    config = SlidesConfig(model=settings.with_model)
    only_slides = OnlySlides(config=config)

    input_data = SlidesInput(
        topic="My simple todo app idea that actually works",
        audience="friends who might want to try it",
        purpose="show them why this app is worth downloading",
        slide_count=3,
        style="casual",
    )

    result = await only_slides.generate_slides(input_data)
    logger.debug("Casual App Demo Slides:\n%s", result.slides)

    # Validate basic structure works even with minimal input
    assert result.slides is not None
    assert len(result.slides.strip()) > 0
    assert len(result.key_insights) >= 1
