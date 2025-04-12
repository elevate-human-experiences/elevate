"""Conftest file for pytest."""

import sys
from pathlib import Path

# Add the "src" folder to the PYTHONPATH for pytest
sys.path.insert(0, Path(__file__).resolve().parent.parent.joinpath("src").as_posix())
