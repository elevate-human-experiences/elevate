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
from elevate.only_email import Email, EmailInput, OnlyEmail


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_personal_email(settings: Any) -> None:
    """Test sending birthday wishes to a close friend."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Send birthday wishes and catch up",
        recipient="my close friend John",
        email_type="personal",
        context="We haven't talked in a few months but we're good friends from college",
        tone="warm and friendly",
        key_details="His birthday is today, we used to study together, I miss our conversations",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_professional_email(settings: Any) -> None:
    """Test requesting sick leave from manager."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Request sick leave due to flu symptoms",
        recipient="my manager Sarah",
        email_type="professional",
        context="I've been feeling unwell since yesterday and don't want to spread illness to the team",
        tone="professional and apologetic",
        key_details="Need 3 days off starting tomorrow, will check emails periodically, can work from home Friday if feeling better",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_marketing_email(settings: Any) -> None:
    """Test promoting a new developer tool to university students."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Announce our new AI email writing tool for developers",
        recipient="university computer science students",
        email_type="marketing",
        context="Students often struggle with professional communication and could benefit from AI assistance",
        tone="energetic and student-friendly",
        key_details="Free for students, works with any LLM, generates emails instantly, completely open source, perfect for internship applications and networking",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_resignation_email(settings: Any) -> None:
    """Test writing a respectful resignation letter to supervisor."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Formally resign from my position with gratitude",
        recipient="my direct supervisor Linda",
        email_type="professional",
        context="I've accepted a new opportunity that aligns better with my career goals, but I've really valued my time here",
        tone="grateful and professional",
        key_details="Last day will be in 2 weeks, happy to train replacement, want to finish current projects, grateful for mentorship and growth opportunities",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_workplace_conflict_email(settings: Any) -> None:
    """Test addressing a communication issue with a colleague diplomatically."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Address communication challenges and find a solution",
        recipient="my colleague Mark from the design team",
        email_type="professional",
        context="We've had some misunderstandings on the last few projects that have caused delays and frustration",
        tone="diplomatic and solution-focused",
        key_details="Want to schedule a private conversation, focus on improving collaboration, acknowledge both perspectives, suggest better communication processes",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_bill_dispute_email(settings: Any) -> None:
    """Test disputing an incorrect charge with customer service."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Dispute an incorrect charge on my account",
        recipient="customer service team at my internet provider",
        email_type="professional",
        context="I was charged for premium services I never signed up for and have been a loyal customer for 3 years",
        tone="firm but respectful",
        key_details="Account #12345, charged $89.99 for premium package on Jan 15th, never requested this service, want immediate refund and removal from account",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_baby_shower_invite_email(settings: Any) -> None:
    """Test inviting loved ones to celebrate an upcoming baby."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Invite family and friends to my sister's baby shower",
        recipient="our close family and friends",
        email_type="personal",
        context="My sister Emily is expecting her first baby and we want to celebrate with everyone who loves her",
        tone="joyful and welcoming",
        key_details="Saturday March 15th at 2pm, my mom's house on Oak Street, registry at Target and Amazon, RSVP by March 1st, it's a girl!",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_urgent_meeting_email(settings: Any) -> None:
    """Test requesting an urgent team meeting about project issues."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Schedule urgent meeting about critical project roadblocks",
        recipient="my project team and manager",
        email_type="professional",
        context="We've discovered some major technical issues that could delay our product launch by weeks if not addressed immediately",
        tone="urgent but not panicked",
        key_details="Available today 3-5pm or tomorrow 9-11am, need all key stakeholders present, issues affect database integration and user authentication",
    )
    generated_email = await only_email.generate_email(email_input)
    logger.debug(generated_email)


@pytest.mark.asyncio  # type: ignore
async def test_structured_personal_email(settings: Any) -> None:
    """Test generating structured birthday wishes with AI insights."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Send heartfelt birthday wishes",
        recipient="my childhood friend Alex",
        email_type="personal",
        context="We grew up together but now live in different cities, haven't seen each other in a year",
        tone="nostalgic and warm",
        key_details="30th birthday, we used to play video games together, hope to visit soon",
    )
    structured_email = await only_email.generate_structured_email(email_input)
    logger.debug(f"Structured Personal Email: {structured_email}")

    # Validate that we got an Email object with all required fields
    assert isinstance(structured_email, Email)
    assert structured_email.subject
    assert structured_email.salutation
    assert structured_email.body
    assert structured_email.closing
    assert structured_email.signature


@pytest.mark.asyncio  # type: ignore
async def test_structured_professional_email(settings: Any) -> None:
    """Test generating structured sick leave request with professional insights."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Request sick leave for flu recovery",
        recipient="my manager Jennifer",
        email_type="professional",
        context="I rarely take sick days and always give proper notice, but this flu hit me hard",
        tone="apologetic but matter-of-fact",
        key_details="Need Wednesday through Friday off, will monitor email for urgent matters, team knows about my current projects",
    )
    structured_email = await only_email.generate_structured_email(email_input)
    logger.debug(f"Structured Professional Email: {structured_email}")

    # Validate that we got an Email object with all required fields
    assert isinstance(structured_email, Email)
    assert structured_email.subject
    assert structured_email.salutation
    assert structured_email.body
    assert structured_email.closing
    assert structured_email.signature


@pytest.mark.asyncio  # type: ignore
async def test_structured_marketing_email(settings: Any) -> None:
    """Test generating structured marketing email with strategic insights."""
    only_email = OnlyEmail(with_model=settings.with_model)
    email_input = EmailInput(
        purpose="Launch announcement for our AI email writing tool",
        recipient="computer science students and young developers",
        email_type="marketing",
        context="Students are often intimidated by professional communication but need these skills for internships and job applications",
        tone="encouraging and energetic",
        key_details="Free for students, works with any AI model, saves hours of writing time, perfect for cover letters and networking emails, completely open source",
    )
    structured_email = await only_email.generate_structured_email(email_input)
    logger.debug(f"Structured Marketing Email: {structured_email}")

    # Validate that we got an Email object with all required fields
    assert isinstance(structured_email, Email)
    assert structured_email.subject
    assert structured_email.salutation
    assert structured_email.body
    assert structured_email.closing
    assert structured_email.signature
