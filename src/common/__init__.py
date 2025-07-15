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

import atexit
import logging
import os
import sys
import warnings


# Set up comprehensive warning suppression for Pydantic
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning:pydantic"


# 1) suppress Pydantic warnings comprehensively
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic.*")
warnings.filterwarnings("ignore", category=FutureWarning, module="pydantic")
warnings.filterwarnings("ignore", category=FutureWarning, module="pydantic.*")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic.*")

# Suppress specific Pydantic serializer warnings by message content
warnings.filterwarnings("ignore", message=".*Pydantic serializer warnings.*")
warnings.filterwarnings("ignore", message=".*PydanticSerializationUnexpectedValue.*")
warnings.filterwarnings("ignore", message=".*Expected.*fields.*")
warnings.filterwarnings("ignore", message=".*serialized value.*")
warnings.filterwarnings("ignore", message=".*StreamingChoices.*")

# Additional catch-all for any pydantic-related warnings
warnings.filterwarnings("ignore", message=".*pydantic.*")
warnings.filterwarnings("ignore", message=".*Pydantic.*")

# Suppress warnings from pyproject.toml that were moved here
# Ignore Pydantic v2 deprecation warnings from dependencies
warnings.filterwarnings(
    "ignore", message="Support for class-based `config` is deprecated", category=DeprecationWarning, module="pydantic.*"
)
# Ignore litellm importlib deprecation warnings
warnings.filterwarnings("ignore", message="open_text is deprecated", category=DeprecationWarning, module="litellm.*")
# Ignore asyncio event loop warnings from litellm
warnings.filterwarnings(
    "ignore", message="There is no current event loop", category=DeprecationWarning, module="litellm.*"
)

# 2) suppress anything logged by Pydantic
logging.getLogger("pydantic").setLevel(logging.ERROR)

# 3) suppress anything logged by LiteLLM
logging.getLogger("LiteLLM").setLevel(logging.ERROR)

# 4) suppress anything logged by OpenAI
logging.getLogger("openai").setLevel(logging.ERROR)

# 5) suppress anything logged by httpx
logging.getLogger("httpx").setLevel(logging.ERROR)

atexit.register(logging.shutdown)


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure the root logger to output log messages to the console only."""
    # Get the root logger
    logger = logging.getLogger()
    # Set the overall logging level
    logger.setLevel(level)

    # Remove all existing handlers, if any
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)

    # Add handler to the logger
    logger.addHandler(console_handler)

    return logger
