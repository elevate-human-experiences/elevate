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

"""Module to test the Q&A generation functionality of the OnlyQA class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_qa import OnlyQA, QAConfig, QAInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_qa_generation_from_product_docs(settings: Any) -> None:
    """Test Q&A generation from product documentation."""
    input_text = (
        "Product: CloudSync Pro\n"
        "CloudSync Pro is a cloud storage solution that allows users to sync files across multiple devices. "
        "Features include: automatic backup, file versioning, real-time collaboration, and 256-bit encryption. "
        "Pricing: Basic plan ($5/month for 100GB), Pro plan ($15/month for 1TB), Enterprise plan (custom pricing). "
        "System requirements: Windows 10+, macOS 10.15+, or Linux Ubuntu 18.04+. "
        "Support is available 24/7 via chat, email, and phone."
    )
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(input_text=input_text)
    result = await only_qa.generate_answers(input_data)
    qa_output = result.answers
    logger.debug("Q&A Generation Output:\n%s", qa_output)

    # Basic validation - ensure output contains typical Q&A patterns
    assert qa_output is not None
    assert len(qa_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_qa_generation_from_technical_docs(settings: Any) -> None:
    """Test Q&A generation from technical documentation."""
    input_text = (
        "API Documentation: UserAuth Service\n"
        "The UserAuth service provides authentication endpoints for user management. "
        "Endpoints: POST /api/auth/login (authenticate user), POST /api/auth/register (create new user), "
        "GET /api/auth/profile (get user profile), POST /api/auth/logout (end session). "
        "Authentication uses JWT tokens with 24-hour expiration. "
        "Rate limiting: 100 requests per minute per IP. "
        "Error codes: 401 (unauthorized), 403 (forbidden), 429 (rate limit exceeded), 500 (server error)."
    )
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(input_text=input_text)
    result = await only_qa.generate_answers(input_data)
    qa_output = result.answers
    logger.debug("Technical Q&A Generation Output:\n%s", qa_output)

    # Basic validation
    assert qa_output is not None
    assert len(qa_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_qa_generation_from_user_manual(settings: Any) -> None:
    """Test Q&A generation from user manual content."""
    input_text = (
        "User Manual: SmartHome Controller\n"
        "Getting Started: Download the SmartHome app from your app store. "
        "Setup: Connect the controller to your Wi-Fi network using the setup wizard. "
        "Adding devices: Tap '+' in the app, select device type, and follow pairing instructions. "
        "Supported devices: lights, thermostats, door locks, security cameras, and smart plugs. "
        "Troubleshooting: If device won't pair, ensure it's in pairing mode and within 30 feet of controller. "
        "For connection issues, restart both the controller and your router."
    )
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(input_text=input_text)
    result = await only_qa.generate_answers(input_data)
    qa_output = result.answers
    logger.debug("User Manual Q&A Generation Output:\n%s", qa_output)

    # Basic validation
    assert qa_output is not None
    assert len(qa_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_qa_generation_from_faq_content(settings: Any) -> None:
    """Test Q&A generation from existing FAQ content to enhance it."""
    input_text = (
        "Existing FAQ for EcoTracker App:\n"
        "Q: How do I track my carbon footprint?\n"
        "A: Open the app and log your daily activities like transportation, energy use, and consumption.\n"
        "Q: Is my data secure?\n"
        "A: Yes, all data is encrypted and stored locally on your device.\n"
        "Additional info: The app also provides personalized recommendations to reduce your environmental impact. "
        "Premium features include detailed analytics, goal setting, and community challenges."
    )
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(input_text=input_text)
    result = await only_qa.generate_answers(input_data)
    qa_output = result.answers
    logger.debug("FAQ Enhancement Output:\n%s", qa_output)

    # Basic validation
    assert qa_output is not None
    assert len(qa_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_qa_generation_empty_input(settings: Any) -> None:
    """Test Q&A generation with empty input."""
    input_text = ""
    config = QAConfig(model=settings.with_model)
    only_qa = OnlyQA(config=config)
    input_data = QAInput(input_text=input_text)
    result = await only_qa.generate_answers(input_data)
    qa_output = result.answers
    logger.debug("Empty Input Q&A Output:\n%s", qa_output)

    # Should handle empty input gracefully
    assert qa_output is not None
