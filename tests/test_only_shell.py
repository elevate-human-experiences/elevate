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

"""Module to test the shell command generation functionalities of the OnlyShell class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_shell import OnlyShell, ShellConfig, ShellInput


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_developer_debugging_scenario(settings: Any) -> None:
    """
    Test scenario: A developer trying to debug a failing build by finding error logs.

    Real user situation: Developer notices their CI/CD pipeline failed and needs to quickly
    find recent error logs to understand what went wrong.
    """
    config = ShellConfig(model=settings.with_model)
    only_shell = OnlyShell(config=config)

    input_data = ShellInput(
        task_description="find all error logs from the last hour",
        context="my build is failing and I need to debug what went wrong",
        environment="linux",
        skill_level="intermediate",
    )

    result = await only_shell.generate_shell_command(input_data)

    # Verify we get a complete response with all expected fields
    assert result.command
    assert result.explanation
    assert "error" in result.explanation.lower() or "log" in result.explanation.lower()
    logger.info("Developer scenario - Command: %s", result.command)
    logger.info("Developer scenario - Explanation: %s", result.explanation)


@pytest.mark.asyncio  # type: ignore
async def test_sysadmin_server_management(settings: Any) -> None:
    """
    Test scenario: System administrator monitoring server disk usage during high traffic.

    Real user situation: Sysadmin gets alerts about disk space and needs to quickly identify
    which directories are consuming the most space.
    """
    config = ShellConfig(model=settings.with_model)
    only_shell = OnlyShell(config=config)

    input_data = ShellInput(
        task_description="show me which directories are using the most disk space",
        context="getting disk space alerts and need to free up space quickly",
        environment="linux",
        skill_level="advanced",
    )

    result = await only_shell.generate_shell_command(input_data)

    assert result.command
    assert result.explanation
    assert result.safety_notes is not None  # Should warn about disk operations
    logger.info("Sysadmin scenario - Command: %s", result.command)
    logger.info("Sysadmin scenario - Safety notes: %s", result.safety_notes)


@pytest.mark.asyncio  # type: ignore
async def test_data_scientist_file_processing(settings: Any) -> None:
    """
    Test scenario: Data scientist needs to process CSV files for analysis.

    Real user situation: Data scientist received a folder of CSV files from different sources
    and needs to combine them for analysis while handling potential formatting issues.
    """
    config = ShellConfig(model=settings.with_model)
    only_shell = OnlyShell(config=config)

    input_data = ShellInput(
        task_description="combine all CSV files in a folder into one file",
        context="preparing data for analysis and the files have different sources",
        environment="macos",
        skill_level="beginner",
    )

    result = await only_shell.generate_shell_command(input_data)

    assert result.command
    assert result.explanation
    assert result.next_steps  # Should suggest what to do after combining files
    assert len(result.related_commands) > 0  # Should suggest related commands
    logger.info("Data scientist scenario - Command: %s", result.command)
    logger.info("Data scientist scenario - Next steps: %s", result.next_steps)


@pytest.mark.asyncio  # type: ignore
async def test_devops_deployment_prep(settings: Any) -> None:
    """
    Test scenario: DevOps engineer preparing for deployment by checking running processes.

    Real user situation: Before deploying a new version, engineer needs to see what services
    are currently running and their resource usage to plan the deployment.
    """
    config = ShellConfig(model=settings.with_model)
    only_shell = OnlyShell(config=config)

    input_data = ShellInput(
        task_description="show me all running processes sorted by memory usage",
        context="preparing for deployment and need to check current system resources",
        environment="linux",
        skill_level="intermediate",
    )

    result = await only_shell.generate_shell_command(input_data)

    assert result.command
    assert result.explanation
    assert result.example_output  # Should show what the output looks like
    logger.info("DevOps scenario - Command: %s", result.command)
    logger.info("DevOps scenario - Example output: %s", result.example_output)
