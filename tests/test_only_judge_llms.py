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

from elevate.only_judge_llms import OnlyJudgeLLMs


@pytest.mark.asyncio  # type: ignore
async def test_summary_evaluation(settings: Any) -> None:
    class SummaryCriteria(BaseModel):
        coherence: int = Field(..., description="Coherence of the summary (1-5)")
        fluency: int = Field(..., description="Fluency of the language (1-5)")
        factual_consistency: int = Field(..., description="Factual consistency (1-5)")

    sample_text = (
        "The Q3 report indicates a 12% increase in revenue driven by new market strategies, "
        "cost-saving initiatives, and improved operational efficiency, though challenges remain in emerging markets."
    )
    judge = OnlyJudgeLLMs(with_model=settings.with_model)
    result: Any = await judge.evaluate(sample_text, SummaryCriteria)

    # This text is coherent and factually consistent, so we expect mid-to-high scores
    assert 4 <= result.coherence <= 5
    assert 3 <= result.fluency <= 5
    assert 4 <= result.factual_consistency <= 5


# --- Test 2: Evaluation of a conversational reply ---
# Updated to reflect a less relevant/helpful response.
@pytest.mark.asyncio  # type: ignore
async def test_conversational_evaluation(settings: Any) -> None:
    class ConversationCriteria(BaseModel):
        relevance: int = Field(..., description="How relevant is the reply? (1-5)")
        helpfulness: int = Field(..., description="How helpful is the response? (1-5)")
        conciseness: int = Field(..., description="How concise is the answer? (1-5)")

    # This reply doesn't provide useful info about a product launch, so we expect lower scores for relevance/helpfulness.
    sample_text = (
        "Thanks for reaching out. Honestly, I don't have any details about the product launch right now. "
        "It's a beautiful day, though. How have you been?"
    )
    judge = OnlyJudgeLLMs(with_model=settings.with_model)
    result: Any = await judge.evaluate(sample_text, ConversationCriteria)

    # Relevance should be lower because it doesn't address the product launch well
    assert 1 <= result.relevance <= 3
    # Helpfulness is also low
    assert 1 <= result.helpfulness <= 3
    # The response is relatively short (though not extremely concise)
    assert 2 <= result.conciseness <= 5


# --- Test 3: Evaluation of creative writing ---
# Leveraging metrics such as creativity, narrative flow, and imagery.
@pytest.mark.asyncio  # type: ignore
async def test_creative_writing_evaluation(settings: Any) -> None:
    class CreativeCriteria(BaseModel):
        creativity: int = Field(..., description="How creative is the composition? (1-5)")
        narrative_flow: int = Field(..., description="Flow of the narrative (1-5)")
        imagery: int = Field(..., description="Quality of imagery evoked (1-5)")

    sample_text = (
        "Amidst the twilight of a fading day, the vibrant hues of an impressionist sky dissolve into whispers of lost dreams. "
        "The city pulses with poetic intensity, each corner revealing a story etched in light and shadow."
    )
    judge = OnlyJudgeLLMs(with_model=settings.with_model)
    result: Any = await judge.evaluate(sample_text, CreativeCriteria)

    # Quite imaginative; likely high creativity
    assert 4 <= result.creativity <= 5
    # Narrative flow might vary
    assert 3 <= result.narrative_flow <= 5
    # Strong imagery
    assert 4 <= result.imagery <= 5


# --- Test 4: Evaluation of an instructional response ---
# Updated to reflect a less complete/accurate set of instructions.
@pytest.mark.asyncio  # type: ignore
async def test_instructional_evaluation(settings: Any) -> None:
    class InstructionCriteria(BaseModel):
        clarity: int = Field(..., description="Clarity of the instructions (1-5)")
        accuracy: int = Field(..., description="Accuracy of the details provided (1-5)")
        completeness: int = Field(..., description="Completeness of the explanation (1-5)")

    # This is intentionally vague and incomplete for installation instructions.
    sample_text = (
        "To install the package, first you open your terminal. Then do something with pip. I'm not entirely sure."
    )
    judge = OnlyJudgeLLMs(with_model=settings.with_model)
    result: Any = await judge.evaluate(sample_text, InstructionCriteria)

    # The instructions aren't very clear
    assert 1 <= result.clarity <= 3
    # Accuracy is also low
    assert 1 <= result.accuracy <= 3
    # Not very comprehensive
    assert 1 <= result.completeness <= 3


# --- Test 5: Evaluation of poetic text ---
# Focusing on metrics like elegance, metaphorical depth, and rhythm.
@pytest.mark.asyncio  # type: ignore
async def test_poetic_evaluation(settings: Any) -> None:
    class PoeticCriteria(BaseModel):
        elegance: int = Field(..., description="Elegance of the phrasing (1-5)")
        metaphorical_depth: int = Field(..., description="Depth of metaphorical expression (1-5)")
        rhythm: int = Field(..., description="Rhythmic quality of the verse (1-5)")

    sample_text = (
        "In the gentle embrace of dusk, silver threads of moonlight weave ancient tales; "
        "the cadence of nature whispers secrets where dreams and reality converge into a poetic reverie."
    )
    judge = OnlyJudgeLLMs(with_model=settings.with_model)
    result: Any = await judge.evaluate(sample_text, PoeticCriteria)

    # The text is fairly elegant, though we allow some variation
    assert 3 <= result.elegance <= 5
    # Strong metaphors here
    assert 4 <= result.metaphorical_depth <= 5
    # Decent rhythm
    assert 3 <= result.rhythm <= 5
