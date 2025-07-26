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

"""Module to test the ELI5 explanation functionality of the OnlyELI5 class."""

import logging
from typing import Any

import pytest

from common import setup_logging
from elevate.only_eli5 import ELI5Config, ELI5Input, OnlyELI5


logger = setup_logging(logging.INFO)


@pytest.mark.asyncio  # type: ignore
async def test_eli5_complex_technology(settings: Any) -> None:
    """Test ELI5 explanation of complex technology concepts."""
    input_text = (
        "Blockchain Technology: "
        "A blockchain is a distributed ledger technology that maintains a continuously growing list of records, "
        "called blocks, which are linked and secured using cryptography. Each block contains a cryptographic hash "
        "of the previous block, a timestamp, and transaction data. By design, a blockchain is resistant to "
        "modification of data and operates without a central authority through a distributed consensus mechanism."
    )
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(input_text=input_text)
    eli5_result = await only_eli5.explain(input_data)
    eli5_output = eli5_result.explanation
    logger.debug("ELI5 Technology Output:\n%s", eli5_output)

    # Basic validation
    assert eli5_output is not None
    assert len(eli5_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_eli5_scientific_concept(settings: Any) -> None:
    """Test ELI5 explanation of scientific concepts."""
    input_text = (
        "Photosynthesis: "
        "Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize "
        "foods from carbon dioxide and water. The process generally involves the green pigment chlorophyll and "
        "generates oxygen as a byproduct. The chemical energy produced is stored in carbohydrate molecules, "
        "such as sugars, which are synthesized from carbon dioxide and water."
    )
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(input_text=input_text)
    eli5_result = await only_eli5.explain(input_data)
    eli5_output = eli5_result.explanation
    logger.debug("ELI5 Science Output:\n%s", eli5_output)

    # Basic validation
    assert eli5_output is not None
    assert len(eli5_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_eli5_financial_concept(settings: Any) -> None:
    """Test ELI5 explanation of financial concepts."""
    input_text = (
        "Compound Interest: "
        "Compound interest is the addition of interest to the principal sum of a loan or deposit, or in other words, "
        "interest on interest. It is the result of reinvesting interest, rather than paying it out, so that interest "
        "in the next period is then earned on the principal sum plus previously accumulated interest. The frequency "
        "of compounding affects the total amount of interest earned."
    )
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(input_text=input_text)
    eli5_result = await only_eli5.explain(input_data)
    eli5_output = eli5_result.explanation
    logger.debug("ELI5 Finance Output:\n%s", eli5_output)

    # Basic validation
    assert eli5_output is not None
    assert len(eli5_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_eli5_physics_concept(settings: Any) -> None:
    """Test ELI5 explanation of physics concepts."""
    input_text = (
        "Quantum Entanglement: "
        "Quantum entanglement is a phenomenon where pairs or groups of particles are generated, interact, or share "
        "spatial proximity in ways such that the quantum state of each particle cannot be described independently "
        "of the state of the others, even when the particles are separated by a large distance. When a measurement "
        "is performed on one particle, it instantaneously affects the state of the entangled partner."
    )
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(input_text=input_text)
    eli5_result = await only_eli5.explain(input_data)
    eli5_output = eli5_result.explanation
    logger.debug("ELI5 Physics Output:\n%s", eli5_output)

    # Basic validation
    assert eli5_output is not None
    assert len(eli5_output.strip()) > 0


@pytest.mark.asyncio  # type: ignore
async def test_eli5_medical_concept(settings: Any) -> None:
    """Test ELI5 explanation of medical concepts."""
    input_text = (
        "DNA: "
        "Deoxyribonucleic acid (DNA) is a molecule composed of two polynucleotide chains that coil around each other "
        "to form a double helix carrying genetic instructions for the development, functioning, growth and reproduction "
        "of all known living organisms and many viruses. DNA and ribonucleic acid (RNA) are nucleic acids. The four "
        "bases found in DNA are adenine (A), cytosine (C), guanine (G) and thymine (T)."
    )
    config = ELI5Config(model=settings.with_model)
    only_eli5 = OnlyELI5(config=config)
    input_data = ELI5Input(input_text=input_text)
    eli5_result = await only_eli5.explain(input_data)
    eli5_output = eli5_result.explanation
    logger.debug("ELI5 Medical Output:\n%s", eli5_output)

    # Basic validation
    assert eli5_output is not None
    assert len(eli5_output.strip()) > 0
