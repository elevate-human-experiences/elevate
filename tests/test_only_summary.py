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

"""Module to test the text summarization functionality of the OnlySummary class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_summary import OnlySummary


logger = setup_logging(logging.DEBUG)


@pytest.mark.asyncio  # type: ignore
async def test_simple_text_summary(settings: Any) -> None:
    """Test simple text summary generation using the chosen model."""
    content = """
Effective communication is vital in both personal and professional contexts.
This short text emphasizes the importance of clarity and brevity in conveying ideas.
A clear message can make a significant difference in how it is received.
"""
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(content)
    logger.debug("Simple Text Summary (%s):\n%s", settings.with_model, summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_news_article_summary(settings: Any) -> None:
    """Test news article summary generation."""
    news_text = """
    In a historic move this morning, government officials announced a groundbreaking policy aimed at reducing carbon emissions across the country.
    The policy outlines specific targets to achieve renewable energy milestones by 2030, with strict regulations and incentives for industries.
    Environmental groups have praised the decision, though some critics argue that the measures may burden local businesses and require significant changes to current operations.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(news_text)
    logger.debug("News Article Summary (%s):\n%s", settings.with_model, summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_research_paper_summary(settings: Any) -> None:
    """Test research paper summary generation."""
    research_text = """
    This paper explores the complex interactions between quantum mechanics and general relativity by proposing a unified framework.
    The authors present a series of experiments and theoretical models that suggest a potential path towards reconciling inconsistencies between the
    Preliminary results demonstrate promising directions for future research and indicate possible implications for our understanding of the universe.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(research_text)
    logger.debug("Research Paper Summary:\n%s", summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_technical_manual_summary(settings: Any) -> None:
    """Test technical manual summary generation."""
    technical_manual_text = """
    User Manual for the XYZ Smartphone: This document provides detailed instructions on setting up the smartphone, including battery installation, initial configuration, and establishing a mobile network connection.
    It includes troubleshooting tips, frequently asked questions, and safety precautions. The manual also explains features such as the high-resolution camera, touch screen, and voice assistant.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(technical_manual_text)
    logger.debug("Technical Manual Summary:\n%s", summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_business_report_summary(settings: Any) -> None:
    """Test business report summary generation."""
    business_report_text = """
    Q3 Business Report: The company experienced steady growth in the third quarter, with a 15% increase in revenue compared to the previous quarter.
    Expansion into new markets and the launch of innovative product lines were significant contributors to this growth.
    The report details market trends, financial performance, and strategic initiatives expected to drive continued progress in the upcoming months.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(business_report_text)
    logger.debug("Business Report Summary:\n%s", summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_legal_document_summary(settings: Any) -> None:
    """Test legal document summary generation."""
    legal_document_text = """
    Contract Agreement Overview: This section of the contract outlines the terms and conditions of the service provided.
    It specifies the responsibilities of both the service provider and the client, including deliverables, payment terms, confidentiality obligations, and dispute resolution procedures.
    The document is legally binding and subject to the jurisdiction of applicable laws.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(legal_document_text)
    logger.debug("Legal Document Summary:\n%s", summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_blog_post_summary(settings: Any) -> None:
    """Test blog post summary generation."""
    blog_post_text = """
    Travel Blog Entry: Last summer, I embarked on a journey across the Mediterranean, experiencing diverse cultures, breathtaking landscapes, and unforgettable culinary delights.
    In this post, I share personal anecdotes, local encounters, and reflective insights from the road, hoping to inspire fellow travelers to explore new destinations with curiosity and an open heart.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(blog_post_text)
    logger.debug("Blog Post Summary:\n%s", summary_output)


@pytest.mark.asyncio  # type: ignore
async def test_fiction_excerpt_summary(settings: Any) -> None:
    """Test fiction excerpt summary generation."""
    fiction_excerpt_text = """
    Fiction Excerpt: In the midst of a dark, enchanted forest, young adventurer Elara discovered an ancient, forgotten path that wound through towering trees and whispering shadows.
    As she journeyed along this mysterious trail, she encountered mystical creatures and uncovered secrets that challenged her understanding of the world and her destiny.
    This excerpt sets the stage for an epic tale of magic, self-discovery, and adventure.
    """
    only_summary_instance = OnlySummary(with_model=settings.with_model)
    summary_output = await only_summary_instance.summarize_and_convert_to_markdown(fiction_excerpt_text)
    logger.debug("Fiction Excerpt Summary:\n%s", summary_output)
