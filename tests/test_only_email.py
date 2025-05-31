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

"""Module to test the email generation functionalities of the OnlyEmail class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_email import OnlyEmail


logger = setup_logging(logging.DEBUG)


@pytest.mark.asyncio  # type: ignore
async def test_personal_email(settings: Any) -> None:
    """Test the generation of a personal email."""
    personal_email_input_message = """
    A birthday wishes for John Doe.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(personal_email_input_message, "personal")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_professional_email(settings: Any) -> None:
    """Test the generation of a professional email."""
    professional_email_input_message = """
    Email to boss regarding, asking a sick leave for 3 days.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(professional_email_input_message, "professional")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_marketing_email(settings: Any) -> None:
    """Test the generation of a marketing email."""
    marketing_email_input_message = """
    Email for a python library which generates professional emails based on user input.

    Important input:
    1. Target Audience: University Students.
    2. Product/Service: Emailer, a Python library which can generate emails of different kinds based on user input. Developers can try out different LLMs while generating emails to see which suits best. This functionality of the library should be called BYOL (Bring Your Own LLM).
    3. Primary Goal: Let developers know about this library.
    4. Key Selling Points:
                        a. Generate email drafts in the blink of an eye.
                        b. Bring Your Own LLM.
                        c. Completely open source.
    5. Call to Action: Click here to know more.
    6. Content Length: 400 words.
    7. Desired Tone: A light and energetic tone.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(marketing_email_input_message, "marketing")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_resignation_email(settings: Any) -> None:
    """Test the generation of a resignation email."""
    resignation_input_message = """
    Please draft a formal resignation email addressed to my supervisor. I am resigning effective [date]
    and would like to express my gratitude for the opportunities provided. I am willing to help with the transition.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(resignation_input_message, "professional")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_workplace_conflict_email(settings: Any) -> None:
    """Test the generation of an email addressing a workplace conflict."""
    conflict_input_message = """
    Draft an email addressing a workplace conflict with a colleague. The email should highlight concerns
    regarding recent interactions, propose a meeting to discuss the issues, and aim for a resolution while remaining professional.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(conflict_input_message, "professional")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_bill_dispute_email(settings: Any) -> None:
    """Test the generation of an email disputing an unneeded bill."""
    bill_input_message = """
    Compose an email to dispute an unneeded bill. Include details that the bill appears to be erroneous and
    request a prompt review or cancellation of the charges.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(bill_input_message, "professional")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_baby_shower_invite_email(settings: Any) -> None:
    """Test the generation of a baby shower invitation email."""
    baby_shower_input_message = """
    Create a cheerful email invitation for a baby shower. Include details such as date, time, venue, and a welcoming message
    inviting close friends and family to join in the celebration.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(baby_shower_input_message, "personal")
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_urgent_meeting_email(settings: Any) -> None:
    """Test the generation of an urgent meeting request email."""
    urgent_meeting_input_message = """
    Draft an email to request an urgent meeting regarding unforeseen project issues that need immediate attention.
    Please include proposed meeting times and emphasize the urgency of the situation.
    """
    only_email = OnlyEmail(with_model=settings.with_model)
    generated_email = await only_email.generate_email(urgent_meeting_input_message, "professional")
    logger.debug(generated_email)
