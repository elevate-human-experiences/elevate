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

"""Test the ELI5 explanation functionality from a user perspective."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_eli5 import ELI5Config, ELI5Input, OnlyELI5


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_eli5_parent_helping_child_with_homework(settings: Any) -> None:
    """Test parent trying to help their child understand a complex topic."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(
        topic="blockchain technology",
        purpose="help my 10-year-old understand this for a school project",
        current_knowledge="I've heard the term but don't really get how it works",
        learning_style="analogies",
        audience_age=10,
    )
    eli5_result = await only_eli5.explain(input_data)

    logger.debug("ELI5 Parent-Child Scenario Output:\n%s", eli5_result.explanation)
    logger.debug("Key Takeaway: %s", eli5_result.key_takeaway)
    logger.debug("Main Concepts: %s", eli5_result.main_concepts)
    logger.debug("Real-world Examples: %s", eli5_result.real_world_examples)

    # Comprehensive validation for enhanced output
    assert eli5_result.explanation is not None
    assert len(eli5_result.explanation.strip()) > 0
    assert eli5_result.key_takeaway is not None
    assert len(eli5_result.key_takeaway.strip()) > 0
    assert isinstance(eli5_result.main_concepts, list)
    assert len(eli5_result.main_concepts) >= 1
    assert isinstance(eli5_result.real_world_examples, list)
    assert len(eli5_result.real_world_examples) >= 1
    assert eli5_result.difficulty_level in ["simple", "moderate", "advanced"]
    assert isinstance(eli5_result.next_steps, list)
    assert len(eli5_result.next_steps) >= 1
    assert isinstance(eli5_result.follow_up_questions, list)
    assert len(eli5_result.follow_up_questions) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_eli5_curious_child_nature_question(settings: Any) -> None:
    """Test explaining nature concepts to a genuinely curious child."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(
        topic="photosynthesis",
        purpose="my 6-year-old keeps asking how plants eat and I want to give a good answer",
        current_knowledge="I know plants need sunlight and water but not much more",
        learning_style="stories",
        audience_age=6,
    )
    eli5_result = await only_eli5.explain(input_data)

    logger.debug("ELI5 Curious Child Output:\n%s", eli5_result.explanation)
    logger.debug("Difficulty Level: %s", eli5_result.difficulty_level)
    logger.debug("Next Steps: %s", eli5_result.next_steps)

    # Comprehensive validation
    assert eli5_result.explanation is not None
    assert len(eli5_result.explanation.strip()) > 0
    assert eli5_result.key_takeaway is not None
    assert len(eli5_result.main_concepts) >= 1
    assert len(eli5_result.real_world_examples) >= 1
    assert eli5_result.difficulty_level in ["simple", "moderate", "advanced"]
    assert len(eli5_result.next_steps) >= 1
    assert len(eli5_result.follow_up_questions) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_eli5_professional_preparing_for_meeting(settings: Any) -> None:
    """Test professional trying to understand a concept before explaining it to others."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(
        topic="compound interest",
        purpose="explain to my team why our investment strategy makes sense",
        current_knowledge="I understand the basics but want to be really clear about it",
        learning_style="step-by-step",
        audience_age=12,
    )
    eli5_result = await only_eli5.explain(input_data)

    logger.debug("ELI5 Professional Meeting Prep Output:\n%s", eli5_result.explanation)
    logger.debug("Main Concepts: %s", eli5_result.main_concepts)

    # Comprehensive validation
    assert eli5_result.explanation is not None
    assert len(eli5_result.explanation.strip()) > 0
    assert eli5_result.key_takeaway is not None
    assert len(eli5_result.main_concepts) >= 1
    assert len(eli5_result.real_world_examples) >= 1
    assert eli5_result.difficulty_level in ["simple", "moderate", "advanced"]
    assert len(eli5_result.next_steps) >= 1
    assert len(eli5_result.follow_up_questions) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_eli5_sci_fi_fan_reality_check(settings: Any) -> None:
    """Test someone trying to separate science fiction from science fact."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(
        topic="quantum entanglement",
        purpose="figure out what's real science vs Hollywood in the movies I watch",
        current_knowledge="I've seen it in movies but don't know if it's actually possible",
        learning_style="examples",
        audience_age=12,
    )
    eli5_result = await only_eli5.explain(input_data)

    logger.debug("ELI5 Sci-Fi Reality Check Output:\n%s", eli5_result.explanation)
    logger.debug("Real-world Examples: %s", eli5_result.real_world_examples)

    # Comprehensive validation
    assert eli5_result.explanation is not None
    assert len(eli5_result.explanation.strip()) > 0
    assert eli5_result.key_takeaway is not None
    assert len(eli5_result.main_concepts) >= 1
    assert len(eli5_result.real_world_examples) >= 1
    assert eli5_result.difficulty_level in ["simple", "moderate", "advanced"]
    assert len(eli5_result.next_steps) >= 1
    assert len(eli5_result.follow_up_questions) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_eli5_student_struggling_with_complex_topic(settings: Any) -> None:
    """Test student trying to understand a challenging school subject."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(
        topic="DNA",
        purpose="understand this for my biology test next week",
        current_knowledge="complete beginner - this stuff is really confusing in my textbook",
        learning_style="analogies",
        audience_age=9,
    )
    eli5_result = await only_eli5.explain(input_data)

    logger.debug("ELI5 Student Biology Test Prep Output:\n%s", eli5_result.explanation)
    logger.debug("Next Steps for Learning: %s", eli5_result.next_steps)

    # Comprehensive validation
    assert eli5_result.explanation is not None
    assert len(eli5_result.explanation.strip()) > 0
    assert eli5_result.key_takeaway is not None
    assert len(eli5_result.main_concepts) >= 1
    assert len(eli5_result.real_world_examples) >= 1
    assert eli5_result.difficulty_level in ["simple", "moderate", "advanced"]
    assert len(eli5_result.next_steps) >= 1
    assert len(eli5_result.follow_up_questions) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_eli5_different_learning_styles_same_topic(settings: Any) -> None:
    """Test that different learning styles produce appropriately tailored explanations."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)

    # Test analogies learning style
    input_analogies = ELI5Input(
        topic="gravity",
        purpose="understand why things fall down",
        current_knowledge="I know things fall but don't know why",
        learning_style="analogies",
        audience_age=7,
    )
    result_analogies = await only_eli5.explain(input_analogies)

    # Test step-by-step learning style
    input_step_by_step = ELI5Input(
        topic="gravity",
        purpose="understand why things fall down",
        current_knowledge="I know things fall but don't know why",
        learning_style="step-by-step",
        audience_age=7,
    )
    result_step_by_step = await only_eli5.explain(input_step_by_step)

    # Both should have comprehensive outputs
    for result in [result_analogies, result_step_by_step]:
        assert result.explanation is not None
        assert result.key_takeaway is not None
        assert len(result.main_concepts) >= 1
        assert len(result.real_world_examples) >= 1
        assert result.difficulty_level in ["simple", "moderate", "advanced"]
        assert len(result.next_steps) >= 1
        assert len(result.follow_up_questions) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_eli5_pure_curiosity_minimal_context(settings: Any) -> None:
    """Test someone with pure curiosity asking about a natural phenomenon."""
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(
        topic="rainbows",
        purpose="satisfy my curiosity - I just think they're amazing",
        current_knowledge="I see them after rain but don't know how they work",
    )
    eli5_result = await only_eli5.explain(input_data)

    logger.debug("ELI5 Pure Curiosity Output:\n%s", eli5_result.explanation)

    # Should provide comprehensive explanation even with minimal context
    assert eli5_result.explanation is not None
    assert len(eli5_result.explanation.strip()) > 0
    assert eli5_result.key_takeaway is not None
    assert len(eli5_result.main_concepts) >= 1
    assert len(eli5_result.real_world_examples) >= 1
    assert eli5_result.difficulty_level in ["simple", "moderate", "advanced"]
    assert len(eli5_result.next_steps) >= 1
    assert len(eli5_result.follow_up_questions) >= 1
