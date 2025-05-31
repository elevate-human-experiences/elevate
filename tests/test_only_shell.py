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

"""Module to test the text rephrasing functionalities of the OnlyShell class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_shell import OnlyShell


logger = setup_logging(logging.DEBUG)


@pytest.mark.asyncio  # type: ignore
async def test_simple_shell_command(settings: Any) -> None:
    """
    Tests the generation of a simple shell command from a natural language description using the `OnlyShell` class.

    This function creates an `OnlyShell` instance, provides it with a textual description
    of the desired shell command (listing files in a directory), generates the corresponding
    shell command, and prints the generated command to the console.  It serves as a basic
    example of how to use the `OnlyShell` class to translate natural language into shell commands.
    """
    input_message = """
    Command to list all files in directory.
    """
    only_shell = OnlyShell(with_model=settings.with_model)
    shell_command = await only_shell.generate_shell_command(input_message)
    logger.debug("Shell command:\n%s", shell_command)
