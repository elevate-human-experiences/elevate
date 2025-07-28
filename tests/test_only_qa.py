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

"""Test the user-friendly knowledge assistant functionality."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_qa import OnlyQA, QAConfig, QAInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_team_explanation_scenario(settings: Any) -> None:
    """Test explaining a product to team members for a presentation."""
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(
        topic="CloudSync Pro - our new cloud storage solution with automatic backup, file versioning, real-time collaboration, and 256-bit encryption. Pricing starts at $5/month for 100GB.",
        context="I need to present this to our sales team next week",
        purpose="Help them understand key features and pricing to discuss with clients",
        specific_questions="What are the main benefits? How should we position this against competitors?",
    )
    result = await only_qa.generate_answers(input_data)
    main_answer = result.main_answer
    logger.debug("Team Explanation Output:\n%s", main_answer)

    # Validate user-friendly output
    assert main_answer is not None
    assert len(main_answer.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_developer_onboarding_scenario(settings: Any) -> None:
    """Test helping a new developer understand our authentication system."""
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(
        topic="UserAuth Service API with endpoints for login, register, profile, and logout. Uses JWT tokens with 24-hour expiration and rate limiting of 100 requests/minute.",
        context="I'm a new developer who needs to integrate user authentication into our mobile app",
        purpose="Understand how to implement login/logout functionality properly",
        specific_questions="What endpoints do I need? How do I handle JWT tokens and error responses?",
    )
    result = await only_qa.generate_answers(input_data)
    main_answer = result.main_answer
    logger.debug("Developer Onboarding Output:\n%s", main_answer)

    # Validate helpful response
    assert main_answer is not None
    assert len(main_answer.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_customer_support_scenario(settings: Any) -> None:
    """Test helping a customer support agent assist users with setup issues."""
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(
        topic="SmartHome Controller setup: download app, connect to Wi-Fi, add devices (lights, thermostats, door locks, cameras, smart plugs). Common issues: devices not pairing, connection problems.",
        context="I work in customer support and get lots of calls about device pairing problems",
        purpose="Create a quick reference guide for common setup issues and solutions",
        specific_questions="What are the most common setup problems and their step-by-step solutions?",
    )
    result = await only_qa.generate_answers(input_data)
    main_answer = result.main_answer
    logger.debug("Customer Support Output:\n%s", main_answer)

    # Validate practical response
    assert main_answer is not None
    assert len(main_answer.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_marketing_content_scenario(settings: Any) -> None:
    """Test creating marketing content from product information."""
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(
        topic="EcoTracker App: track carbon footprint by logging daily activities, get personalized recommendations, secure local data storage. Premium features: detailed analytics, goal setting, community challenges.",
        context="I'm writing marketing copy for our app store listing and website",
        purpose="Highlight key benefits that will convince people to download and use the app",
        specific_questions="What makes this app special? What problems does it solve for environmentally conscious users?",
    )
    result = await only_qa.generate_answers(input_data)
    main_answer = result.main_answer
    logger.debug("Marketing Content Output:\n%s", main_answer)

    # Validate marketing-focused response
    assert main_answer is not None
    assert len(main_answer.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_minimal_input_scenario(settings: Any) -> None:
    """Test handling minimal user input gracefully."""
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(topic="Help me understand project management", context="", purpose="", specific_questions="")
    result = await only_qa.generate_answers(input_data)
    main_answer = result.main_answer
    logger.debug("Minimal Input Output:\n%s", main_answer)

    # Should handle minimal input gracefully
    assert main_answer is not None
