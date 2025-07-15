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

"""Module to test the blog generation functionality of the OnlyVideoToBlog class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_video_to_blog import OnlyVideoToBlog


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_simple_blog_generation(settings: Any) -> None:
    """Test the generation of blog of simple text using the OnlyVideoToBlog class."""
    only_video = OnlyVideoToBlog(with_model=settings.with_model)

    transcript = """
    Welcome to our tutorial on machine learning. Today we'll be discussing the fundamentals of neural networks.
    Neural networks are computational models inspired by the human brain. They consist of interconnected nodes
    called neurons that process information. In this video, we'll explore how these networks learn from data
    and make predictions. We'll cover topics like backpropagation, gradient descent, and various network architectures.
    By the end of this session, you'll have a solid understanding of how neural networks work.
    """

    logger.debug(await only_video.generate_blog(transcript))


@pytest.mark.asyncio  # type: ignore
async def test_empty_transcript_validation(settings: Any) -> None:
    """Test that empty or whitespace-only transcripts raise ValueError."""
    only_video = OnlyVideoToBlog(with_model=settings.with_model)

    # Test completely empty string
    with pytest.raises(ValueError, match="Transcript cannot be empty or contain only whitespace"):
        await only_video.generate_blog("")

    # Test whitespace-only string
    with pytest.raises(ValueError, match="Transcript cannot be empty or contain only whitespace"):
        await only_video.generate_blog("   \n  \t  ")
