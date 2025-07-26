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
    AudiocastConfig,
    AudiocastInput,
    CastConfiguration,
    ListenerConfig,
    OnlyAudiocast,
    SpeakerConfig,
)


@pytest.mark.asyncio  # type: ignore
async def test_create_travel_recommendation_audiocast(settings: Any) -> None:
    """Test creating an audiocast for travel planning - realistic user scenario."""
    content = """I'm planning a trip to San Francisco next month and want to make the most of my 3-day visit. San Francisco is known for its iconic Golden Gate Bridge, which offers stunning views especially at sunrise and sunset. The city's famous cable cars provide a unique way to navigate the steep hills while taking in the sights. Fisherman's Wharf is a popular tourist destination with fresh seafood, street performers, and sea lions at Pier 39. For a more local experience, explore the Mission District for amazing Mexican food and colorful murals. Don't miss Lombard Street, known as the "crookedest street in the world," and consider taking a ferry to Alcatraz Island for a fascinating historical tour."""

    config = AudiocastConfig(model=settings.with_model)
    audiocast = OnlyAudiocast(config=config)
    input_data = AudiocastInput(
        topic="San Francisco Travel Guide",
        content=content,
        context="planning my first trip to San Francisco",
        purpose="travel planning and preparation",
        target_audience="first-time visitors",
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )
    result = await audiocast.cast(input_data)

    # Verify enhanced output fields are populated
    assert result.duration_minutes > 0
    assert result.summary
    assert "San Francisco" in result.summary
    assert len(result.speakers_used) >= 1
    assert len(result.next_steps) > 0
    assert len(result.related_topics) > 0


@pytest.mark.asyncio  # type: ignore
async def test_create_team_training_audiocast(settings: Any) -> None:
    """Test creating an audiocast for team training - realistic workplace scenario."""
    content = """Remote work has fundamentally changed how we communicate and collaborate in the workplace. With teams spread across different time zones, traditional meeting structures don't always work effectively. Successful remote teams have learned to prioritize asynchronous communication - using tools like shared documents, recorded video updates, and detailed written summaries. This allows team members to contribute when they're most productive, rather than forcing everyone into the same meeting slots.

Clear documentation becomes critical when you can't just tap someone on the shoulder for a quick question. Teams that excel at remote work create comprehensive project briefs, maintain updated status dashboards, and use collaborative tools that track decisions and changes. Regular check-ins are still important, but they focus on outcomes and obstacles rather than just status updates. Many companies find that rotating meeting times helps ensure all team members can participate in real-time discussions occasionally.

The key is establishing rhythm and predictability. When everyone knows when updates are expected, which tools to use for different types of communication, and how decisions get made, remote teams can actually move faster than traditional in-office teams. The elimination of impromptu interruptions and the ability to work during peak energy hours often leads to higher productivity and better work quality."""

    cast_configuration = CastConfiguration(
        speakers=[
            SpeakerConfig(
                name="Sarah",
                background="Team lead with 5 years remote work experience",
                expertise="medium",
                speaking_style="conversational",
                level_of_expertise="experienced",
                focus_aspect="practical implementation",
                depth="medium",
            ),
            SpeakerConfig(
                name="Marcus",
                background="HR specialist focusing on remote team dynamics",
                expertise="medium",
                speaking_style="analytical",
                level_of_expertise="experienced",
                focus_aspect="team communication",
                depth="medium",
            ),
        ],
        listener=ListenerConfig(
            expertise="beginner",
            summary_of_similar_content=["Basic remote work tips"],
            level_of_expertise="new to remote work",
            depth="medium",
        ),
    )

    config = AudiocastConfig(model=settings.with_model)
    audiocast = OnlyAudiocast(config=config)
    input_data = AudiocastInput(
        topic="Remote Work Best Practices",
        content=content,
        context="training my team on effective remote work",
        purpose="team training and skill development",
        target_audience="team members new to remote work",
        cast_configuration=cast_configuration,
        audio_out_path=f"{os.environ['HOME']}/Downloads/",
    )
    result = await audiocast.cast(input_data)

    # Verify the enhanced output provides value for team training
    assert result.duration_minutes > 0
    assert "Remote Work" in result.summary
    assert "training" in result.summary.lower()
    assert len(result.speakers_used) == 2
    assert "Sarah" in result.speakers_used
    assert "Marcus" in result.speakers_used
    assert any("team" in step.lower() for step in result.next_steps)
    assert len(result.key_insights) > 0
