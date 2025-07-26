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

from typing import Any

import pytest
from pydantic import BaseModel, Field

from elevate.only_judge_llms import JudgeLLMsConfig, JudgeLLMsInput, JudgeLLMsOutput, OnlyJudgeLLMs


@pytest.mark.asyncio  # type: ignore
async def test_important_client_email(settings: Any) -> None:
    class EmailCriteria(BaseModel):
        professionalism: int = Field(..., description="How professional does this sound? (1-5)")
        clarity: int = Field(..., description="How clear and easy to understand? (1-5)")

    sample_content = (
        "Hi Sarah, I wanted to follow up on our conversation last week about the project timeline. "
        "Unfortunately, we're running into some technical issues that might push back our delivery date. "
        "I know this isn't ideal, but I wanted to be transparent about where we stand. "
        "Can we schedule a call this week to discuss next steps? Thanks for your understanding."
    )

    config = JudgeLLMsConfig(model="gpt-4o-mini")
    judge = OnlyJudgeLLMs(config=config)
    input_data = JudgeLLMsInput(
        content=sample_content,
        context="important client email about project delays",
        purpose="need to maintain good relationship while delivering bad news",
        criteria=EmailCriteria,
    )
    result: JudgeLLMsOutput = await judge.evaluate(input_data)

    # This email is professional and clear, though delivering bad news
    assert isinstance(result.scores, EmailCriteria)
    assert 1 <= result.scores.professionalism <= 5
    assert 1 <= result.scores.clarity <= 5

    # Check enhanced output fields exist
    assert isinstance(result.summary, str)
    assert len(result.summary) > 0
    assert isinstance(result.key_insights, list)
    assert isinstance(result.recommendations, list)


@pytest.mark.asyncio  # type: ignore
async def test_social_media_post(settings: Any) -> None:
    class SocialMediaCriteria(BaseModel):
        engagement: int = Field(..., description="How likely is this to get likes and comments? (1-5)")
        authenticity: int = Field(..., description="Does this sound genuine and personal? (1-5)")

    sample_content = (
        "🌟 Just finished setting up our new coffee corner at the shop! "
        "There's nothing quite like the smell of fresh beans in the morning. "
        "What's your go-to coffee order? Drop it in the comments!"
    )

    config = JudgeLLMsConfig(model="gpt-4o-mini")
    judge = OnlyJudgeLLMs(config=config)
    input_data = JudgeLLMsInput(
        content=sample_content, context="Instagram post for my small coffee shop", criteria=SocialMediaCriteria
    )
    result: JudgeLLMsOutput = await judge.evaluate(input_data)

    # Basic validation of structure
    assert isinstance(result.scores, SocialMediaCriteria)
    assert 1 <= result.scores.engagement <= 5
    assert 1 <= result.scores.authenticity <= 5

    # Verify enhanced fields exist
    assert isinstance(result.summary, str)
    assert isinstance(result.key_insights, list)
    assert isinstance(result.recommendations, list)


@pytest.mark.asyncio  # type: ignore
async def test_job_application_cover_letter(settings: Any) -> None:
    class CoverLetterCriteria(BaseModel):
        enthusiasm: int = Field(..., description="How enthusiastic and motivated do I sound? (1-5)")
        relevance: int = Field(..., description="How well do I connect my experience to the role? (1-5)")
        professionalism: int = Field(..., description="Is this appropriately professional? (1-5)")

    sample_content = (
        "Dear Hiring Manager, I'm excited to apply for the Marketing Coordinator position at your company. "
        "In my previous role at a tech startup, I managed social media campaigns that increased engagement by 40%. "
        "I'm particularly drawn to your company's mission of sustainable innovation, which aligns perfectly with my values. "
        "I believe my combination of creativity and analytical skills would be a great fit for your marketing team. "
        "Thank you for considering my application. I look forward to hearing from you."
    )

    config = JudgeLLMsConfig(model="gpt-4o-mini")
    judge = OnlyJudgeLLMs(config=config)
    input_data = JudgeLLMsInput(
        content=sample_content,
        context="cover letter for marketing coordinator job",
        purpose="need to stand out from other candidates and get an interview",
        criteria=CoverLetterCriteria,
    )
    result: JudgeLLMsOutput = await judge.evaluate(input_data)

    # Basic validation of structure
    assert isinstance(result.scores, CoverLetterCriteria)
    assert 1 <= result.scores.enthusiasm <= 5
    assert 1 <= result.scores.relevance <= 5
    assert 1 <= result.scores.professionalism <= 5

    # Should provide enhanced output
    assert isinstance(result.next_steps, list)


@pytest.mark.asyncio  # type: ignore
async def test_team_announcement(settings: Any) -> None:
    class AnnouncementCriteria(BaseModel):
        clarity: int = Field(..., description="Is the message clear and easy to understand? (1-5)")
        motivation: int = Field(..., description="Will this motivate and inspire the team? (1-5)")
        completeness: int = Field(..., description="Does it include all necessary information? (1-5)")

    sample_content = (
        "Hi everyone, I wanted to share some exciting news about our Q4 goals. "
        "We're launching a new project that should help streamline our workflow. "
        "I'll need everyone to be flexible with deadlines over the next few weeks. "
        "Let me know if you have questions. Thanks for all your hard work!"
    )

    config = JudgeLLMsConfig(model="gpt-4o-mini")
    judge = OnlyJudgeLLMs(config=config)
    input_data = JudgeLLMsInput(
        content=sample_content,
        context="team announcement to 12 people about upcoming project changes",
        purpose="need to prepare team for busy period while keeping morale high",
        criteria=AnnouncementCriteria,
    )
    result: JudgeLLMsOutput = await judge.evaluate(input_data)

    # Basic validation of structure
    assert isinstance(result.scores, AnnouncementCriteria)
    assert 1 <= result.scores.clarity <= 5
    assert 1 <= result.scores.motivation <= 5
    assert 1 <= result.scores.completeness <= 5

    # Should provide enhanced output
    assert isinstance(result.recommendations, list)


@pytest.mark.asyncio  # type: ignore
async def test_thank_you_note_to_mentor(settings: Any) -> None:
    class ThankYouCriteria(BaseModel):
        sincerity: int = Field(..., description="How genuine and heartfelt does this sound? (1-5)")
        specificity: int = Field(..., description="Do I mention specific ways they helped me? (1-5)")
        gratitude: int = Field(..., description="Does this clearly express my appreciation? (1-5)")

    sample_content = (
        "Dear Dr. Martinez, I wanted to reach out and thank you for all the guidance you've provided "
        "during my internship this summer. Your advice about approaching client presentations with "
        "confidence really transformed how I communicate. The feedback you gave me on my research "
        "project helped me see new perspectives I hadn't considered. I'm grateful to have had you "
        "as a mentor, and I hope to stay in touch as I continue my career. Thank you again for "
        "believing in me and pushing me to grow."
    )

    config = JudgeLLMsConfig(model="gpt-4o-mini")
    judge = OnlyJudgeLLMs(config=config)
    input_data = JudgeLLMsInput(
        content=sample_content,
        context="thank you note to my internship mentor before I graduate",
        purpose="want to express genuine gratitude and maintain professional relationship",
        criteria=ThankYouCriteria,
    )
    result: JudgeLLMsOutput = await judge.evaluate(input_data)

    # Basic validation of structure
    assert isinstance(result.scores, ThankYouCriteria)
    assert 1 <= result.scores.sincerity <= 5
    assert 1 <= result.scores.specificity <= 5
    assert 1 <= result.scores.gratitude <= 5

    # Should provide enhanced output
    assert isinstance(result.summary, str)
    assert isinstance(result.key_insights, list)
