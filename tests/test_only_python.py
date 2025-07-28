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

"""Test the Python code generation functionality from a user perspective."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_python import OnlyPython, PythonConfig, PythonInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_python_beginner_learning_basics(settings: Any) -> None:
    """Test beginner trying to learn Python fundamentals through a simple task."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)
    input_data = PythonInput(
        task="create a simple calculator that adds two numbers",
        purpose="I'm learning Python and want to understand functions and user input",
        experience_level="beginner",
        output_format="display",
    )
    python_result = await only_python.create_code(input_data)

    logger.debug("Python Beginner Learning Output:\n%s", python_result.code)
    logger.debug("Key Concepts: %s", python_result.key_concepts)
    logger.debug("Learning Notes: %s", python_result.learning_notes)

    # Comprehensive validation for enhanced output
    assert python_result.code is not None
    assert len(python_result.code.strip()) > 0
    assert python_result.explanation is not None
    assert len(python_result.explanation.strip()) > 0
    assert isinstance(python_result.key_concepts, list)
    assert len(python_result.key_concepts) >= 1
    assert isinstance(python_result.dependencies, list)
    assert python_result.usage_instructions is not None
    assert isinstance(python_result.learning_notes, list)
    assert len(python_result.learning_notes) >= 1
    assert isinstance(python_result.next_improvements, list)
    assert len(python_result.next_improvements) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_python_data_analyst_api_scraping(settings: Any) -> None:
    """Test data analyst needing to fetch data from an API for their reports."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)
    input_data = PythonInput(
        task="fetch weather data from an API and save it to a CSV file",
        purpose="I need to collect daily weather data for my monthly climate analysis report",
        experience_level="intermediate",
        preferred_libraries="requests, pandas",
        output_format="save_file",
    )
    python_result = await only_python.create_code(input_data)

    logger.debug("Python Data Analyst API Output:\n%s", python_result.code)
    logger.debug("Dependencies: %s", python_result.dependencies)
    logger.debug("Usage Instructions: %s", python_result.usage_instructions)

    # Comprehensive validation
    assert python_result.code is not None
    assert len(python_result.code.strip()) > 0
    assert python_result.explanation is not None
    assert len(python_result.key_concepts) >= 1
    assert isinstance(python_result.dependencies, list)
    assert python_result.usage_instructions is not None
    assert len(python_result.learning_notes) >= 1
    assert len(python_result.next_improvements) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_python_student_automating_homework(settings: Any) -> None:
    """Test student trying to automate file processing for a school project."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)
    input_data = PythonInput(
        task="read a text file and count how many times each word appears",
        purpose="I have a book report assignment and need to analyze word frequency",
        experience_level="beginner",
        data_source="a text file with my book content",
        output_format="display",
    )
    python_result = await only_python.create_code(input_data)

    logger.debug("Python Student Homework Automation Output:\n%s", python_result.code)
    logger.debug("Learning Notes: %s", python_result.learning_notes)

    # Comprehensive validation
    assert python_result.code is not None
    assert len(python_result.code.strip()) > 0
    assert python_result.explanation is not None
    assert len(python_result.key_concepts) >= 1
    assert isinstance(python_result.dependencies, list)
    assert python_result.usage_instructions is not None
    assert len(python_result.learning_notes) >= 1
    assert len(python_result.next_improvements) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_python_professional_automating_workflow(settings: Any) -> None:
    """Test professional trying to automate repetitive work tasks."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)
    input_data = PythonInput(
        task="organize files in a folder by their extension and creation date",
        purpose="I waste too much time manually sorting downloaded files every week",
        experience_level="intermediate",
        data_source="my Downloads folder with mixed file types",
        output_format="save_file",
    )
    python_result = await only_python.create_code(input_data)

    logger.debug("Python Professional Workflow Automation Output:\n%s", python_result.code)
    logger.debug("Next Improvements: %s", python_result.next_improvements)

    # Comprehensive validation
    assert python_result.code is not None
    assert len(python_result.code.strip()) > 0
    assert python_result.explanation is not None
    assert len(python_result.key_concepts) >= 1
    assert isinstance(python_result.dependencies, list)
    assert python_result.usage_instructions is not None
    assert len(python_result.learning_notes) >= 1
    assert len(python_result.next_improvements) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_python_researcher_data_visualization(settings: Any) -> None:
    """Test researcher needing to create charts for their presentation."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)
    input_data = PythonInput(
        task="create a bar chart showing monthly sales data",
        purpose="I need to present quarterly results to my team next week",
        experience_level="intermediate",
        preferred_libraries="matplotlib, pandas",
        data_source="CSV file with sales data by month",
        output_format="create_chart",
    )
    python_result = await only_python.create_code(input_data)

    logger.debug("Python Researcher Data Visualization Output:\n%s", python_result.code)
    logger.debug("Example Output: %s", python_result.example_output)

    # Comprehensive validation
    assert python_result.code is not None
    assert len(python_result.code.strip()) > 0
    assert python_result.explanation is not None
    assert len(python_result.key_concepts) >= 1
    assert isinstance(python_result.dependencies, list)
    assert python_result.usage_instructions is not None
    assert len(python_result.learning_notes) >= 1
    assert len(python_result.next_improvements) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_python_different_experience_levels_same_task(settings: Any) -> None:
    """Test that different experience levels produce appropriately tailored solutions."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)

    # Test beginner level
    input_beginner = PythonInput(
        task="read a CSV file and calculate the average of one column",
        purpose="understand how to work with data files in Python",
        experience_level="beginner",
        output_format="display",
    )
    result_beginner = await only_python.create_code(input_beginner)

    # Test advanced level
    input_advanced = PythonInput(
        task="read a CSV file and calculate the average of one column",
        purpose="build this into a larger data processing pipeline",
        experience_level="advanced",
        output_format="return_data",
    )
    result_advanced = await only_python.create_code(input_advanced)

    # Both should have comprehensive outputs but different complexity
    for result in [result_beginner, result_advanced]:
        assert result.code is not None
        assert result.explanation is not None
        assert len(result.key_concepts) >= 1
        assert isinstance(result.dependencies, list)
        assert result.usage_instructions is not None
        assert len(result.learning_notes) >= 1
        assert len(result.next_improvements) >= 1


@pytest.mark.asyncio  # type: ignore
async def test_python_building_on_existing_code(settings: Any) -> None:
    """Test someone wanting to extend or modify existing code."""
    config = PythonConfig(model=settings.with_model)
    only_python = OnlyPython(config=config)
    input_data = PythonInput(
        task="add error handling and logging to my file processing script",
        purpose="make my script more robust for production use",
        experience_level="intermediate",
        existing_code="def process_file(filename):\n    with open(filename, 'r') as f:\n        return f.read().upper()",
        output_format="return_data",
    )
    python_result = await only_python.create_code(input_data)

    logger.debug("Python Code Enhancement Output:\n%s", python_result.code)

    # Should provide comprehensive solution even when building on existing code
    assert python_result.code is not None
    assert len(python_result.code.strip()) > 0
    assert python_result.explanation is not None
    assert len(python_result.key_concepts) >= 1
    assert isinstance(python_result.dependencies, list)
    assert python_result.usage_instructions is not None
    assert len(python_result.learning_notes) >= 1
    assert len(python_result.next_improvements) >= 1
