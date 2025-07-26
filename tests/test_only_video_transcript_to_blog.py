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

"""Test the video transcript to blog functionality from a user perspective."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_video_transcript_to_blog import BlogConfig, BlogInput, OnlyVideoToBlog


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_blog_content_marketer_webinar_repurpose(settings: Any) -> None:
    """Test content marketer transforming webinar transcript into thought leadership blog."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    webinar_transcript = """
    Welcome everyone to today's webinar on digital transformation. I'm Sarah Mitchell, and I've been helping companies
    navigate digital change for over 15 years. Today I want to share three critical lessons I've learned.

    First, digital transformation isn't about technology - it's about people. I worked with a manufacturing company
    last year that spent millions on new systems, but employees were still using spreadsheets because no one taught
    them why the change mattered. We had to go back and focus on the human element first.

    Second, start small but think big. Don't try to transform everything at once. Pick one process, perfect it,
    then scale. And third, measure what matters. Track user adoption, not just technical metrics.

    The key insight here is that successful digital transformation requires a people-first approach combined with
    strategic execution. Companies that get this right see 40% better outcomes.
    """

    input_data = BlogInput(
        transcript=webinar_transcript,
        purpose="create thought leadership content for our company blog",
        audience="business executives and decision makers",
        tone="executive",
        context="recorded from our monthly webinar series on digital innovation",
    )

    blog_result = await blog_creator.create_blog_post(input_data)

    logger.debug("Blog Content Marketer Output:\n%s", blog_result.blog_post)
    logger.debug("Key Insights: %s", blog_result.key_insights)
    logger.debug("Suggested Title: %s", blog_result.suggested_title)
    logger.debug("Tags: %s", blog_result.tags)

    # Comprehensive validation for enhanced output
    assert blog_result.blog_post is not None
    assert len(blog_result.blog_post.strip()) > 0
    assert blog_result.summary is not None
    assert len(blog_result.summary.strip()) > 0
    assert blog_result.suggested_title is not None
    assert len(blog_result.suggested_title.strip()) > 0
    assert isinstance(blog_result.key_insights, list)
    assert len(blog_result.key_insights) >= 1
    assert isinstance(blog_result.tags, list)
    assert len(blog_result.tags) >= 1
    assert isinstance(blog_result.next_steps, list)
    assert len(blog_result.next_steps) >= 1
    assert isinstance(blog_result.target_keywords, list)
    assert len(blog_result.target_keywords) >= 1
    assert blog_result.reading_time is not None


@pytest.mark.asyncio  # type: ignore
async def test_blog_executive_keynote_speech(settings: Any) -> None:
    """Test executive turning keynote speech into thought leadership article."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    keynote_transcript = """
    Good morning everyone. As CEO of TechFlow, I've watched our industry evolve dramatically.
    But here's what hasn't changed - the importance of building trust with your customers.

    Let me tell you about Maria, one of our long-time clients. When she first came to us, her company
    was struggling with customer retention. Traditional approaches weren't working. We realized the
    problem wasn't the product - it was trust. Customers didn't believe the company truly understood their needs.

    So we implemented a radical transparency program. We showed customers exactly how we solve their problems,
    shared our decision-making process, and admitted when we made mistakes. Six months later, Maria's retention
    rate increased by 60%. Why? Because trust is the foundation of all lasting business relationships.

    In today's market, customers have infinite choices. The companies that win are the ones that earn trust
    through consistent, transparent action. That's not just good business - it's the only sustainable way forward.
    """

    input_data = BlogInput(
        transcript=keynote_transcript,
        purpose="establish thought leadership in our industry",
        audience="fellow executives and business leaders",
        tone="executive",
        context="keynote speech from the annual TechFlow conference",
        word_count=800,
    )

    blog_result = await blog_creator.create_blog_post(input_data)

    logger.debug("Executive Keynote Blog Output:\n%s", blog_result.blog_post)
    logger.debug("Summary: %s", blog_result.summary)
    logger.debug("Next Steps: %s", blog_result.next_steps)

    # Comprehensive validation
    assert blog_result.blog_post is not None
    assert len(blog_result.blog_post.strip()) > 0
    assert blog_result.summary is not None
    assert blog_result.suggested_title is not None
    assert len(blog_result.key_insights) >= 1
    assert len(blog_result.tags) >= 1
    assert len(blog_result.next_steps) >= 1
    assert len(blog_result.target_keywords) >= 1
    assert blog_result.reading_time is not None


@pytest.mark.asyncio  # type: ignore
async def test_blog_educator_course_content(settings: Any) -> None:
    """Test educator creating written resources from recorded lecture."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    lecture_transcript = """
    Today we're exploring the concept of compound growth, and I want you to understand not just the math,
    but why this principle can transform how you think about improvement in any area of life.

    Imagine you're trying to get 1% better at something every day. Seems small, right? But here's the magic -
    if you improve by just 1% every day for a year, you'll be 37 times better by the end. That's the power
    of compound growth.

    I saw this firsthand when working with a struggling student named Alex. He was failing calculus and felt hopeless.
    Instead of trying to master everything at once, we focused on improving one small concept each day.
    Understanding derivatives led to better integration skills, which improved problem-solving confidence.

    Six months later, Alex wasn't just passing - he was tutoring other students. That's compound growth in action.
    Small, consistent improvements create exponential results over time. The key is consistency and patience with the process.
    """

    input_data = BlogInput(
        transcript=lecture_transcript,
        purpose="create supplementary reading material for my students",
        audience="college students and lifelong learners",
        tone="educational",
        context="recorded from my principles of growth course",
    )

    blog_result = await blog_creator.create_blog_post(input_data)

    logger.debug("Educator Course Content Output:\n%s", blog_result.blog_post)
    logger.debug("Target Keywords: %s", blog_result.target_keywords)

    # Comprehensive validation
    assert blog_result.blog_post is not None
    assert len(blog_result.blog_post.strip()) > 0
    assert blog_result.summary is not None
    assert blog_result.suggested_title is not None
    assert len(blog_result.key_insights) >= 1
    assert len(blog_result.tags) >= 1
    assert len(blog_result.next_steps) >= 1
    assert len(blog_result.target_keywords) >= 1
    assert blog_result.reading_time is not None


@pytest.mark.asyncio  # type: ignore
async def test_blog_podcaster_expanding_reach(settings: Any) -> None:
    """Test podcaster creating written content to expand audience reach."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    podcast_transcript = """
    Hey everyone, welcome back to Startup Stories. I'm your host Jake, and today I'm sharing something personal -
    the biggest mistake I made in my first startup and how it taught me everything about resilience.

    Picture this: It's 2019, I've just launched my dream app, and I'm convinced I'll be the next unicorn.
    I spent months building the perfect product in isolation, ignoring user feedback because I was sure I knew better.
    Launch day comes, and... crickets. Barely anyone downloaded it.

    I was devastated. But my mentor Lisa told me something that changed everything: "Failure isn't the opposite of success -
    it's a stepping stone to it." She made me realize I wasn't listening to my users. So I pivoted.

    Instead of building what I thought people wanted, I started building what they actually needed.
    I interviewed 100 potential users, rebuilt the app based on their feedback, and launched again.
    This time it worked. We hit 10,000 users in the first month.

    The lesson? Resilience isn't about bouncing back - it's about bouncing forward. Every failure teaches you something
    that makes your next attempt stronger.
    """

    input_data = BlogInput(
        transcript=podcast_transcript,
        purpose="reach people who prefer reading over listening to podcasts",
        audience="entrepreneurs and startup founders",
        tone="conversational",
        context="episode from my weekly podcast about startup lessons",
    )

    blog_result = await blog_creator.create_blog_post(input_data)

    logger.debug("Podcaster Content Expansion Output:\n%s", blog_result.blog_post)
    logger.debug("Reading Time: %s", blog_result.reading_time)

    # Comprehensive validation
    assert blog_result.blog_post is not None
    assert len(blog_result.blog_post.strip()) > 0
    assert blog_result.summary is not None
    assert blog_result.suggested_title is not None
    assert len(blog_result.key_insights) >= 1
    assert len(blog_result.tags) >= 1
    assert len(blog_result.next_steps) >= 1
    assert len(blog_result.target_keywords) >= 1
    assert blog_result.reading_time is not None


@pytest.mark.asyncio  # type: ignore
async def test_blog_sales_team_customer_interview(settings: Any) -> None:
    """Test sales team converting customer interview insights into case study."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    interview_transcript = """
    Thanks for joining us today, Jennifer. As the VP of Operations at MegaCorp, can you tell us about
    your experience with our automation platform?

    Jennifer: Absolutely. When we first implemented your solution, we were drowning in manual processes.
    Our team was spending 20 hours a week on data entry alone. The frustration was real - people were
    working late just to keep up with basic tasks.

    What was the turning point?

    Jennifer: The automation workflows you helped us set up changed everything. What used to take our team
    a full day now happens in 2 hours. But more importantly, our employees can focus on strategic work instead
    of repetitive tasks. Morale has improved dramatically.

    We've saved over $200,000 in operational costs this year, but the real value is in employee satisfaction.
    People are excited about their work again. That's something you can't put a price on.

    Any advice for other companies considering automation?

    Jennifer: Start with your biggest pain points. Don't try to automate everything at once.
    Pick one process, do it well, then expand. And involve your team in the process - they know
    the workflows better than anyone.
    """

    input_data = BlogInput(
        transcript=interview_transcript,
        purpose="create a customer success story for our sales materials",
        audience="potential customers and prospects",
        tone="professional",
        context="customer interview for case study development",
    )

    blog_result = await blog_creator.create_blog_post(input_data)

    logger.debug("Sales Team Case Study Output:\n%s", blog_result.blog_post)
    logger.debug("Key Insights: %s", blog_result.key_insights)

    # Comprehensive validation
    assert blog_result.blog_post is not None
    assert len(blog_result.blog_post.strip()) > 0
    assert blog_result.summary is not None
    assert blog_result.suggested_title is not None
    assert len(blog_result.key_insights) >= 1
    assert len(blog_result.tags) >= 1
    assert len(blog_result.next_steps) >= 1
    assert len(blog_result.target_keywords) >= 1
    assert blog_result.reading_time is not None


@pytest.mark.asyncio  # type: ignore
async def test_blog_different_tones_same_content(settings: Any) -> None:
    """Test that different tones produce appropriately tailored blog posts."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    base_transcript = """
    The future of remote work is here, and it's changing how we think about productivity.
    Companies that adapt will thrive, while those that don't will struggle to attract top talent.
    """

    # Test executive tone
    executive_input = BlogInput(
        transcript=base_transcript,
        purpose="thought leadership for executives",
        audience="business leaders",
        tone="executive",
        context="Executive leadership discussion",
    )
    executive_result = await blog_creator.create_blog_post(executive_input)

    # Test conversational tone
    conversational_input = BlogInput(
        transcript=base_transcript,
        purpose="engage general audience",
        audience="remote workers",
        tone="conversational",
        context="Remote work discussion",
    )
    conversational_result = await blog_creator.create_blog_post(conversational_input)

    # Both should have comprehensive outputs
    for result in [executive_result, conversational_result]:
        assert result.blog_post is not None
        assert result.summary is not None
        assert result.suggested_title is not None
        assert len(result.key_insights) >= 1
        assert len(result.tags) >= 1
        assert len(result.next_steps) >= 1
        assert len(result.target_keywords) >= 1
        assert result.reading_time is not None


@pytest.mark.asyncio  # type: ignore
async def test_blog_minimal_context_high_value(settings: Any) -> None:
    """Test creating blog post with minimal context but high-value content."""
    config = BlogConfig(model=settings.with_model)
    blog_creator = OnlyVideoToBlog(config=config)

    simple_transcript = """
    Innovation doesn't happen in isolation. The best ideas come from diverse teams working together,
    challenging each other's assumptions, and building on each other's strengths. When you create
    an environment where people feel safe to share wild ideas, magic happens.
    """

    input_data = BlogInput(
        transcript=simple_transcript,
        purpose="inspire our team",
        audience="team members",
        tone="inspiring",
        context="Team inspiration content",
    )

    blog_result = await blog_creator.create_blog_post(input_data)

    logger.debug("Minimal Context High Value Output:\n%s", blog_result.blog_post)

    # Should provide comprehensive blog post even with minimal context
    assert blog_result.blog_post is not None
    assert len(blog_result.blog_post.strip()) > 0
    assert blog_result.summary is not None
    assert blog_result.suggested_title is not None
    assert len(blog_result.key_insights) >= 1
    assert len(blog_result.tags) >= 1
    assert len(blog_result.next_steps) >= 1
    assert len(blog_result.target_keywords) >= 1
    assert blog_result.reading_time is not None
