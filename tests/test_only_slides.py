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
from elevate.only_slides import OnlySlides


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_pitch_deck_generation(settings: Any) -> None:
    """Test generation of a pitch deck from product documentation."""
    input_text = (
        "Product: EcoTracker - Sustainable Living App\n"
        "EcoTracker helps users monitor and reduce their environmental impact through daily activity tracking. "
        "The app tracks carbon footprint from transportation, energy usage, and consumption habits. "
        "Key features: real-time tracking, personalized recommendations, goal setting, community challenges, "
        "and detailed analytics. Target market: environmentally conscious millennials and Gen Z. "
        "Business model: freemium with premium analytics and advanced features. "
        "Competitive advantage: AI-powered recommendations and gamification elements."
    )
    only_slides = OnlySlides(with_model=settings.with_model)
    slides_output = await only_slides.generate_slides(input_text, "pitch deck", 5)
    logger.debug("Pitch Deck Slides Output:\n%s", slides_output)

    # Basic validation
    assert slides_output is not None
    assert len(slides_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_product_presentation_generation(settings: Any) -> None:
    """Test generation of a product presentation from technical specs."""
    input_text = (
        "Product: CloudSync Pro - Enterprise File Synchronization\n"
        "Technical specifications: 256-bit AES encryption, real-time sync across unlimited devices, "
        "API integrations with 50+ business tools, automated backup schedules, version control, "
        "collaborative workspaces, admin controls, compliance with SOC 2 Type II, GDPR, and HIPAA. "
        "Infrastructure: AWS-based with 99.9% uptime SLA, global CDN, and disaster recovery. "
        "Pricing: Enterprise plans starting at $10/user/month with volume discounts available."
    )
    only_slides = OnlySlides(with_model=settings.with_model)
    slides_output = await only_slides.generate_slides(input_text, "product presentation", 6)
    logger.debug("Product Presentation Slides Output:\n%s", slides_output)

    # Basic validation
    assert slides_output is not None
    assert len(slides_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_sales_deck_generation(settings: Any) -> None:
    """Test generation of a sales deck from company information."""
    input_text = (
        "Company: TechFlow Solutions - B2B Automation Platform\n"
        "Problem: Businesses waste 40% of time on repetitive manual tasks. "
        "Solution: TechFlow automates workflows across departments with no-code solutions. "
        "Benefits: 60% reduction in processing time, 90% fewer errors, $50K average annual savings per client. "
        "Customer testimonials: 'TechFlow transformed our operations' - Fortune 500 client. "
        "Market size: $8B workflow automation market growing 20% annually. "
        "Competitive landscape: Zapier, Microsoft Power Automate, but we offer enterprise-grade security."
    )
    only_slides = OnlySlides(with_model=settings.with_model)
    slides_output = await only_slides.generate_slides(input_text, "sales deck", 8)
    logger.debug("Sales Deck Slides Output:\n%s", slides_output)

    # Basic validation
    assert slides_output is not None
    assert len(slides_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_investor_presentation_generation(settings: Any) -> None:
    """Test generation of an investor presentation from startup information."""
    input_text = (
        "Startup: GreenTech Innovations - Renewable Energy Management\n"
        "Market opportunity: $150B renewable energy market with 15% CAGR. "
        "Product: AI-powered energy optimization platform for commercial buildings. "
        "Traction: $2M ARR, 150+ enterprise customers, 40% month-over-month growth. "
        "Team: Former Tesla, Google, and McKinsey executives with 20+ years combined experience. "
        "Funding: Seeking $10M Series A to expand sales team and accelerate product development. "
        "Financial projections: $20M ARR by year 3, path to profitability by year 4."
    )
    only_slides = OnlySlides(with_model=settings.with_model)
    slides_output = await only_slides.generate_slides(input_text, "investor presentation", 10)
    logger.debug("Investor Presentation Slides Output:\n%s", slides_output)

    # Basic validation
    assert slides_output is not None
    assert len(slides_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_training_slides_generation(settings: Any) -> None:
    """Test generation of training slides from educational content."""
    input_text = (
        "Training Topic: Cybersecurity Best Practices for Remote Workers\n"
        "Learning objectives: Identify common security threats, implement strong password policies, "
        "recognize phishing attempts, secure home Wi-Fi networks, use VPN properly. "
        "Key concepts: Multi-factor authentication, zero-trust security model, social engineering, "
        "data encryption, incident response procedures. "
        "Interactive elements: Security assessment quiz, password strength checker demo, "
        "phishing email examples, case studies of security breaches."
    )
    only_slides = OnlySlides(with_model=settings.with_model)
    slides_output = await only_slides.generate_slides(input_text, "training presentation", 7)
    logger.debug("Training Slides Output:\n%s", slides_output)

    # Basic validation
    assert slides_output is not None
    assert len(slides_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_minimal_input_slides(settings: Any) -> None:
    """Test slide generation with minimal input content."""
    input_text = "Product: Simple Todo App. Features: task creation, due dates, reminders."
    only_slides = OnlySlides(with_model=settings.with_model)
    slides_output = await only_slides.generate_slides(input_text, "product overview", 3)
    logger.debug("Minimal Input Slides Output:\n%s", slides_output)

    # Basic validation
    assert slides_output is not None
    assert len(slides_output.strip()) > 0
