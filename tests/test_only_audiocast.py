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

import os
from typing import Any

import pytest

from elevate.only_audiocast import (
    CastConfiguration,
    ListenerConfig,
    OnlyAudiocast,
    SpeakerConfig,
)


@pytest.mark.asyncio  # type: ignore
async def test_create_default_audiocast(settings: Any) -> None:
    content = "San Francisco is a city in California. It is known for the Golden Gate Bridge."
    audiocast = OnlyAudiocast(with_model=settings.with_model)
    await audiocast.cast(
        content,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )


@pytest.mark.asyncio  # type: ignore
async def test_create_two_people_podcast(settings: Any) -> None:
    content = """The standard cosmological model rests on a foundational assumption: that the universe is homogeneous and isotropic on large scales. However, this assumption has long been questioned due to observable evidence of substantial cosmic inhomogeneities—galaxy clusters, vast voids, and filamentary structures spanning billions of light-years. Such uneven distributions of matter challenge the premise that the universe expands uniformly. Post-doctorate astrophysics researchers are increasingly examining the implications of these structures, realizing that overlooking them might significantly distort our understanding of cosmic expansion.

One emerging theory gaining traction is timescape cosmology, which offers a compelling alternative to the elusive concept of dark energy. Timescape theory posits that different regions of the universe experience their own distinct "timescapes"—unique expansion histories shaped by local gravitational environments. In this model, what appears to be an accelerating universe (currently explained by invoking dark energy) is instead interpreted as an observational artifact arising from comparing clocks and rulers in regions with varying gravitational conditions. Essentially, the accelerated expansion emerges naturally from general relativity when accounting properly for gravitational inhomogeneities, eliminating the need for mysterious forms of energy.

This theory is resonating within the astrophysics community largely because of its elegant explanatory power and reduction in speculative components. Timescape cosmology aligns closely with recent astronomical observations highlighting significant cosmic structures, offering an interpretation firmly grounded in established physics rather than unknown entities. As post-doc students delve deeper into the precision cosmology era, leveraging data from advanced telescopes and gravitational-wave observatories, exploring and refining timescape models becomes a promising frontier—one that may reshape our fundamental understanding of the universe and its evolution."""

    cast_configuration = CastConfiguration(
        speakers=[
            SpeakerConfig(
                name="Professor Mitchell",
                background="Expert in astrophysics focusing on gravitational inhomogeneities",
                expertise="high",
                speaking_style="interview",
                level_of_expertise="post-doc",
                focus_aspect="timescape cosmology",
                depth="high",
            ),
            SpeakerConfig(
                name="Professor Carter",
                background="Renowned cosmologist with extensive research in timescape theory",
                expertise="high",
                speaking_style="conversational",
                level_of_expertise="post-doc",
                focus_aspect="observational cosmology",
                depth="high",
            ),
        ],
        listener=ListenerConfig(
            expertise="advanced",
            summary_of_similar_content=["Post-doctoral astrophysics discussions"],
            level_of_expertise="high",
            depth="high",
        ),
    )

    audiocast = OnlyAudiocast(with_model=settings.with_model)
    await audiocast.cast(
        content,
        cast_configuration=cast_configuration,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )
