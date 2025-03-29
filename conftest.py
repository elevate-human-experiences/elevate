"""Conftest file for pytest."""

import sys
import os

# Add the "src" folder to the PYTHONPATH for pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
