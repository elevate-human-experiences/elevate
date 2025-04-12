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

from elevate.only_summary import OnlySummary


def test_simple_text_summarization() -> None:
    """
    Tests the summarization of simple text using the OnlySummary class.
    """
    content = """
Effective communication is vital in both personal and professional contexts.
This short text emphasizes the importance of clarity and brevity in conveying ideas.
A clear message can make a significant difference in how it is received.
"""
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(content)
    print("Simple Text Summary:\n", summary_output)


def test_news_article_summary() -> None:
    """
    Tests the summarization of a news article using the OnlySummary class.
    """
    news_text = """
    In a historic move this morning, government officials announced a groundbreaking policy aimed at reducing carbon emissions across the country.
    The policy outlines specific targets to achieve renewable energy milestones by 2030, with strict regulations and incentives for industries.
    Environmental groups have praised the decision, though some critics argue that the measures may burden local businesses and require significant changes to current operations.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(news_text)
    print("News Article Summary:\n", summary_output)


def test_research_paper_summary() -> None:
    """
    Tests the summarization of a research paper abstract using the OnlySummary class.
    """
    research_text = """
    This paper explores the complex interactions between quantum mechanics and general relativity by proposing a unified framework.
    The authors present a series of experiments and theoretical models that suggest a potential path towards reconciling inconsistencies between the two pillars of modern physics.
    Preliminary results demonstrate promising directions for future research and indicate possible implications for our understanding of the universe.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(
        research_text
    )
    print("Research Paper Summary:\n", summary_output)


def test_technical_manual_summary() -> None:
    """
    Tests the summarization of technical documentation using the OnlySummary class.
    """
    technical_manual_text = """
    User Manual for the XYZ Smartphone: This document provides detailed instructions on setting up the smartphone, including battery installation, initial configuration, and establishing a mobile network connection.
    It includes troubleshooting tips, frequently asked questions, and safety precautions. The manual also explains features such as the high-resolution camera, touch screen, and voice assistant.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(
        technical_manual_text
    )
    print("Technical Manual Summary:\n", summary_output)


def test_business_report_summary() -> None:
    """
    Tests the summarization of a business report using the OnlySummary class.
    """
    business_report_text = """
    Q3 Business Report: The company experienced steady growth in the third quarter, with a 15% increase in revenue compared to the previous quarter.
    Expansion into new markets and the launch of innovative product lines were significant contributors to this growth.
    The report details market trends, financial performance, and strategic initiatives expected to drive continued progress in the upcoming months.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(
        business_report_text
    )
    print("Business Report Summary:\n", summary_output)


def test_legal_document_summary() -> None:
    """
    Tests the summarization of a legal document using the OnlySummary class.
    """
    legal_document_text = """
    Contract Agreement Overview: This section of the contract outlines the terms and conditions of the service provided.
    It specifies the responsibilities of both the service provider and the client, including deliverables, payment terms, confidentiality obligations, and dispute resolution procedures.
    The document is legally binding and subject to the jurisdiction of applicable laws.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(
        legal_document_text
    )
    print("Legal Document Summary:\n", summary_output)


def test_blog_post_summary() -> None:
    """
    Tests the summarization of a blog post using the OnlySummary class.
    """
    blog_post_text = """
    Travel Blog Entry: Last summer, I embarked on a journey across the Mediterranean, experiencing diverse cultures, breathtaking landscapes, and unforgettable culinary delights.
    In this post, I share personal anecdotes, local encounters, and reflective insights from the road, hoping to inspire fellow travelers to explore new destinations with curiosity and an open heart.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(
        blog_post_text
    )
    print("Blog Post Summary:\n", summary_output)


def test_fiction_excerpt_summary() -> None:
    """
    Tests the summarization of a fiction excerpt using the OnlySummary class.
    """
    fiction_excerpt_text = """
    Fiction Excerpt: In the midst of a dark, enchanted forest, young adventurer Elara discovered an ancient, forgotten path that wound through towering trees and whispering shadows.
    As she journeyed along this mysterious trail, she encountered mystical creatures and uncovered secrets that challenged her understanding of the world and her destiny.
    This excerpt sets the stage for an epic tale of magic, self-discovery, and adventure.
    """
    only_summary_instance = OnlySummary()
    summary_output = only_summary_instance.summarize_and_convert_to_markdown(
        fiction_excerpt_text
    )
    print("Fiction Excerpt Summary:\n", summary_output)
