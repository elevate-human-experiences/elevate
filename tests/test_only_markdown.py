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

"""Module to test the markdown conversion functionality of the OnlyMarkdown class with hastily copied inputs."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_markdown import OnlyMarkdown


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_hastily_copied_html_conversion(settings: Any) -> None:
    """Simulate a conversion where a user has copy-pasted HTML content that lost its formatting."""
    input_text = (
        "<h1>Repo for Learning - A Repository for Exploration</h1>"
        "<div>This repository is designed to be a learning resource. It covers a variety of topics to help you expand your knowledge. "
        "It includes some code like: <pre>def greet(name): print(f'Hello, {name}!') greet('Learner')</pre>"
        "See <a href='https://www.wikipedia.org/'>link</a> for more information. "
        "<blockquote>This is a block quote that may not be formatted correctly.</blockquote>"
        "Project Structure: <table border='1'><tr><th>File/Directory</th><th>Description</th></tr>"
        "<tr><td>README.txt</td><td>This file.</td></tr><tr><td>/examples</td><td>Code examples.</td></tr></table>"
        "End of README."
    )
    only_markdown = OnlyMarkdown(with_model=settings.with_model)
    markdown_output = await only_markdown.convert_to_markdown(input_text)
    logger.debug("HTML Copy-Paste Conversion:\n%s", markdown_output)


@pytest.mark.asyncio  # type: ignore
async def test_hastily_copied_word_doc_conversion(settings: Any) -> None:
    """Simulate a conversion of text that was copy-pasted from a Word document."""
    input_text = (
        "Repo for Learning - A Repository for Exploration  "
        "This repository is designed to be a learning resource. It covers a variety of topics to help you expand your knowledge. "
        "It includes some code like: def greet(name): print('Hello, ' + name)  "
        "For more, see link:https://www.wikipedia.org/ more info.  "
        ">> Quote: This is a block quote that might not format well.  "
        "Project Structure:  File/Directory  Description  "
        "README.txt  This file.   /examples  Code examples.  "
        "End of document."
    )
    only_markdown = OnlyMarkdown(with_model=settings.with_model)
    markdown_output = await only_markdown.convert_to_markdown(input_text)
    logger.debug("Word Doc Copy-Paste Conversion:\n%s", markdown_output)


@pytest.mark.asyncio  # type: ignore
async def test_hastily_copied_db_output_conversion(settings: Any) -> None:
    """Simulate a conversion where tabular data from a database is copy-pasted as plain text."""
    input_text = "Name    Age    Occupation\nAlice   30     Engineer\nBob     25     Designer\nCharlie 35     Manager\n"
    only_markdown = OnlyMarkdown(with_model=settings.with_model)
    markdown_output = await only_markdown.convert_to_markdown(input_text)
    logger.debug("DB Output Copy-Paste Conversion:\n%s", markdown_output)


@pytest.mark.asyncio  # type: ignore
async def test_hastily_copied_blog_post_conversion(settings: Any) -> None:
    """Simulate a conversion of a blog post that was copied from a web page or document and lost its formatting."""
    input_text = (
        "Blog Post: Journey Through Code   Author: Jane Doe   Date: 2025-04-10  "
        "Welcome to my coding journey! Over the years, I have learned a great deal about programming.  "
        "Introduction  Starting with basic scripts and moving to complex systems, the evolution of my skills has been remarkable.  "
        "My Experience  I began coding in college and since then the landscape of technology has never ceased to amaze me.  "
        "Stay tuned for more updates.  Happy coding and keep exploring!"
    )
    only_markdown = OnlyMarkdown(with_model=settings.with_model)
    markdown_output = await only_markdown.convert_to_markdown(input_text)
    logger.debug("Blog Post Copy-Paste Conversion:\n%s", markdown_output)


@pytest.mark.asyncio  # type: ignore
async def test_hastily_copied_complex_unformatted_conversion(settings: Any) -> None:
    """
    Simulate a conversion of a complex document where various elements (titles, lists, code, and links)
    are mashed together due to hasty copy-paste, resulting in lost formatting.
    """
    input_text = (
        "Title: Complex Document Example  "
        "This document showcases various elements.  "
        "Bullet List: - Primary Item 1, with a sub list: Sub-item with inline code: greet('World').  "
        "- Primary Item 2, Sub-item with emphasis: *important* note.  "
        'Block Quote: "This is a block quote that lost its formatting."  '
        "Code: def example(): return 'Hello, Markdown!'  "
        "More info: Visit https://example.com for further details."
    )
    only_markdown = OnlyMarkdown(with_model=settings.with_model)
    markdown_output = await only_markdown.convert_to_markdown(input_text)
    logger.debug("Complex Unformatted Copy-Paste Conversion:\n%s", markdown_output)
