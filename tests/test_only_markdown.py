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

"""Real-world user scenarios for testing the OnlyMarkdown class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_markdown import MarkdownConfig, MarkdownInput, OnlyMarkdown


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_project_manager_meeting_notes(settings: Any) -> None:
    """A project manager wants to format their meeting notes for the team wiki."""
    content = (
        "Weekly Project Standup - Jan 15th  "
        "Attendees: Sarah (PM), Mike (Dev), Lisa (QA), Tom (Design)  "
        "Discussion Points:  "
        "- Sprint 3 progress: 80% complete, on track for Friday delivery  "
        "- Bug fixes: 15 resolved, 3 remaining (all low priority)  "
        "- New feature requests from client: dark mode toggle, export functionality  "
        "Action Items:  "
        "Mike: Finish authentication module by Wednesday  "
        "Lisa: Complete final testing on payment flow  "
        "Tom: Provide mockups for dark mode by Thursday  "
        "Next meeting: January 22nd, 2:00 PM EST"
    )

    config = MarkdownConfig(model=settings.with_model)
    markdown_converter = OnlyMarkdown(config=config)

    input_data = MarkdownInput(
        content=content,
        context="for our team wiki to share with stakeholders",
        purpose="make meeting notes more professional and easier to follow",
    )

    result = await markdown_converter.convert_to_markdown(input_data)

    # Verify we get enhanced output
    assert result.markdown
    assert isinstance(result.formatting_improvements, list)
    assert result.summary
    assert isinstance(result.next_steps, list)

    logger.debug("Project Manager Meeting Notes Result:\n%s", result.markdown)
    logger.debug("Improvements: %s", result.formatting_improvements)


@pytest.mark.asyncio  # type: ignore
async def test_developer_api_documentation(settings: Any) -> None:
    """A developer wants to format API endpoint documentation for GitHub README."""
    content = (
        "User Authentication Endpoints  "
        "POST /api/auth/login  "
        "Request: { username: string, password: string }  "
        "Response: { token: string, user: { id: number, name: string, email: string } }  "
        "Status codes: 200 (success), 401 (invalid credentials), 500 (server error)  "
        "GET /api/auth/profile  "
        "Headers: Authorization: Bearer <token>  "
        "Response: { user: { id: number, name: string, email: string, created_at: timestamp } }  "
        "Status codes: 200 (success), 401 (unauthorized), 404 (user not found)  "
        "Example usage:  "
        'curl -X POST http://localhost:3000/api/auth/login -H \'Content-Type: application/json\' -d \'{"username":"john","password":"secret"}\''  # pragma: allowlist secret
    )

    config = MarkdownConfig(model=settings.with_model)
    markdown_converter = OnlyMarkdown(config=config)

    input_data = MarkdownInput(
        content=content,
        context="for our GitHub repository README",
        purpose="help other developers understand our API endpoints",
    )

    result = await markdown_converter.convert_to_markdown(input_data)

    assert result.markdown
    assert len(result.formatting_improvements) > 0
    assert result.summary
    assert "API" in result.summary or "endpoint" in result.summary.lower()

    logger.debug("Developer API Documentation Result:\n%s", result.markdown)


@pytest.mark.asyncio  # type: ignore
async def test_student_study_notes(settings: Any) -> None:
    """A student wants to format their class notes for better studying."""
    content = (
        "Chapter 5: Machine Learning Fundamentals  "
        "Key Concepts:  "
        "Supervised learning: uses labeled training data, examples include classification and regression  "
        "Unsupervised learning: finds patterns in unlabeled data, examples include clustering and dimensionality reduction  "
        "Important Algorithms:  "
        "Linear Regression: y = mx + b, used for predicting continuous values  "
        "Decision Trees: tree-like model of decisions, good for classification  "
        "K-Means Clustering: partitions data into k clusters  "
        "Formulas to remember:  "
        "Mean Squared Error: MSE = (1/n) * Σ(yi - ŷi)²  "
        "Accuracy: (TP + TN) / (TP + TN + FP + FN)  "
        "Study tip: practice with real datasets from Kaggle"
    )

    config = MarkdownConfig(model=settings.with_model)
    markdown_converter = OnlyMarkdown(config=config)

    input_data = MarkdownInput(content=content, purpose="organize my study notes for better memorization")

    result = await markdown_converter.convert_to_markdown(input_data)

    assert result.markdown
    assert len(result.formatting_improvements) > 0
    # Since no context provided, next_steps might be empty

    logger.debug("Student Study Notes Result:\n%s", result.markdown)


@pytest.mark.asyncio  # type: ignore
async def test_blogger_article_draft(settings: Any) -> None:
    """A blogger wants to format their article draft for publication."""
    content = (
        "5 Tips for Remote Work Success  "
        "Working from home has become the new normal, but it comes with unique challenges. Here are my top recommendations after 3 years of remote work.  "
        "1. Create a dedicated workspace  "
        "Having a specific area for work helps your brain switch into 'work mode'. Even if it's just a corner of your bedroom, make it yours.  "
        "2. Stick to a routine  "
        "Wake up at the same time, get dressed (yes, even if no one will see you), and start work at a consistent hour.  "
        "3. Take real breaks  "
        "Step away from your computer. Go for a walk, do some stretches, or just look out the window for 5 minutes.  "
        "4. Over-communicate with your team  "
        "When you can't tap someone on the shoulder, you need to be more intentional about communication. Use Slack, schedule regular check-ins, share updates proactively.  "
        "5. Set boundaries  "
        "Just because you work from home doesn't mean you're always available. Set clear start and end times for your workday.  "
        "What works for you? Let me know in the comments!"
    )

    config = MarkdownConfig(model=settings.with_model)
    markdown_converter = OnlyMarkdown(config=config)

    input_data = MarkdownInput(
        content=content,
        context="for publishing on my personal blog",
        purpose="make the article more engaging and readable",
    )

    result = await markdown_converter.convert_to_markdown(input_data)

    assert result.markdown
    assert len(result.formatting_improvements) > 0
    assert result.summary
    assert len(result.next_steps) > 0

    logger.debug("Blogger Article Draft Result:\n%s", result.markdown)


@pytest.mark.asyncio  # type: ignore
async def test_manager_team_announcement(settings: Any) -> None:
    """A manager needs to format an important team announcement for email and Slack."""
    content = (
        "Important Update: Q1 2025 Reorganization  "
        "Team, I wanted to share some exciting news about changes coming in Q1.  "
        "What's changing:  "
        "We're expanding the engineering team from 8 to 12 people  "
        "Sarah Thompson will be joining as our new Senior Frontend Developer (starts Feb 1st)  "
        "The design team will be embedded more closely with engineering for faster iteration  "
        "New process: weekly cross-functional stand-ups starting January 20th  "
        "Why we're making these changes:  "
        "Client feedback showed need for faster feature delivery  "
        "Current team is at capacity with existing roadmap  "
        "Better collaboration between design and eng will reduce back-and-forth  "
        "Timeline:  "
        "Jan 15: Team introductions and role clarifications  "
        "Jan 20: First cross-functional standup  "
        "Feb 1: Sarah's first day  "
        "Feb 15: Process retrospective and adjustments  "
        "Questions? Feel free to reach out to me directly or we can discuss in our next 1:1."
    )

    config = MarkdownConfig(model=settings.with_model)
    markdown_converter = OnlyMarkdown(config=config)

    input_data = MarkdownInput(
        content=content,
        context="for sending to my team via email and posting in Slack",
        purpose="communicate changes clearly and professionally",
    )

    result = await markdown_converter.convert_to_markdown(input_data)

    assert result.markdown
    assert len(result.formatting_improvements) > 0
    assert result.summary
    assert "reorganization" in result.summary.lower() or "team" in result.summary.lower()
    assert len(result.next_steps) > 0

    logger.debug("Manager Team Announcement Result:\n%s", result.markdown)


@pytest.mark.asyncio  # type: ignore
async def test_copywriter_product_features(settings: Any) -> None:
    """A copywriter wants to format product feature descriptions for a website."""
    content = (
        "TaskMaster Pro: Advanced Project Management Features  "
        "Real-time Collaboration: Work together seamlessly with your team. See updates instantly, comment on tasks, and get notifications when things change. No more endless email chains or missed deadlines.  "
        "Smart Scheduling: Our AI-powered scheduling suggests the best times for meetings based on everyone's availability and timezone. It even considers your productivity patterns and suggests focus time blocks.  "
        "Advanced Analytics: Get insights into your team's productivity with detailed reports. Track time spent on different types of tasks, identify bottlenecks, and see which projects are most profitable.  "
        "Custom Workflows: Every team is different. Build workflows that match how you actually work. Set up approval processes, automate repetitive tasks, and create templates for common projects.  "
        "Integrations: Connect with the tools you already use. Slack, Google Workspace, GitHub, Figma, and 50+ other integrations available. Data syncs automatically so you never have to duplicate work.  "
        "Mobile App: Full-featured mobile app for iOS and Android. Manage projects, approve tasks, and stay connected with your team from anywhere. Offline mode ensures you can work even without internet."
    )

    config = MarkdownConfig(model=settings.with_model)
    markdown_converter = OnlyMarkdown(config=config)

    input_data = MarkdownInput(
        content=content,
        context="for our product landing page",
        purpose="highlight key features in a scannable, compelling format",
    )

    result = await markdown_converter.convert_to_markdown(input_data)

    assert result.markdown
    assert len(result.formatting_improvements) > 0
    assert result.summary
    assert len(result.next_steps) > 0

    logger.debug("Copywriter Product Features Result:\n%s", result.markdown)
