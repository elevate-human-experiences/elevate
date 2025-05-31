"""Module for audio cast generation using GPT-4o."""

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

import difflib
import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from secrets import choice as secrets_choice

import yaml  # type: ignore
from openai import OpenAI
from pydantic import BaseModel, Field
from pydub import AudioSegment

from common import setup_logging

from .only_json import OnlyJson


logger = setup_logging(logging.DEBUG)


class SpeakerConfig(BaseModel):
    """Speaker configuration model."""

    name: str = Field(..., description="Speaker's name")
    background: str = Field(..., description="Speaker background information")
    expertise: str = Field(..., description="Expertise level of the speaker")
    speaking_style: str = Field(..., description="Style of the speaker's delivery")
    level_of_expertise: str = Field(..., description="Detailed expertise level")
    focus_aspect: str = Field(..., description="Aspect the speaker is focusing on")
    depth: str = Field(..., description="Depth of content provided by the speaker")


class ListenerConfig(BaseModel):
    """Listener configuration model."""

    name: str | None = Field(default=None, description="Listener's name (optional)")
    expertise: str = Field(..., description="Expertise level of the listener")
    summary_of_similar_content: list[str] = Field(..., description="Summaries of similar content")
    level_of_expertise: str = Field(..., description="Listener's proficiency level")
    depth: str = Field(..., description="Depth of content for the listener")


class CastConfiguration(BaseModel):
    """Cast configuration model for speakers and listener."""

    speakers: list[SpeakerConfig] = Field(..., description="List of speaker configurations")
    listener: ListenerConfig = Field(..., description="Configuration for the listener")


class Instructions(BaseModel):
    """Model for instructions to the agent."""

    instructions: str = Field(..., description="Instructions for the agent")


default_cast_configuration = CastConfiguration(
    speakers=[
        SpeakerConfig(
            name="Narrator",
            background="Technical background",
            expertise="medium",
            speaking_style="narrative",
            level_of_expertise="medium",
            focus_aspect="technical details",
            depth="medium",
        )
    ],
    listener=ListenerConfig(
        expertise="medium",
        summary_of_similar_content=["Technical podcasts overview"],
        level_of_expertise="medium",
        depth="medium",
    ),
)


class ConversationEntry(BaseModel):
    """Data model for a conversation entry."""

    pause: float = Field(
        default=0.5,
        description="Pause duration between conversation segments. In seconds. 0 means other/interrupting.",
        json_schema_extra={"minimum": 0.0, "maximum": 2.0},
    )
    speaker: str = Field(..., description="Name of the conversation speaker")
    message: str = Field(..., description="Message content of the entry")


class Conversation(BaseModel):
    """Data model for a conversation consisting of multiple entries."""

    entries: list[ConversationEntry] = Field(..., description="List of conversation entries")


class AudiocastTitle(BaseModel):
    """Model to generate an audiocast title from conversation content."""

    generated_title: str = Field(..., description="Title derived from the conversation content")

    @classmethod
    def generate(cls, content: str) -> "AudiocastTitle":
        """Generate a title using the first 10 words of content."""
        words = content.split()[:10]
        title = " ".join(words) if words else "Audiocast"
        title_snippet = title.replace(" ", "_")[:30]
        return cls(generated_title=title_snippet)


class AudiocastFFmpegNotInstalledError(Exception):
    """Raised when ffmpeg is not installed for audio processing."""


class OnlyAudiocast:
    """Converts text into an audio file using the GPT-4o model."""

    def __init__(self, with_model: str = "o1") -> None:
        """Initialize OnlyAudiocast and verify ffmpeg installation."""
        if not AudioSegment.ffmpeg:
            raise AudiocastFFmpegNotInstalledError(
                "ffmpeg is not installed. Try installing it as `brew install ffmpeg`, or whatever is appropriate for your OS."
            )
        self.client = OpenAI()
        self.available_voices = [
            "alloy",
            "fable",
            "onyx",
            "nova",
            "shimmer",
        ]
        self.with_model = with_model

    def get_system_prompt(self, cast_configuration: CastConfiguration) -> str:
        """Generate a system prompt with cast configuration in YAML."""
        cast_config_yaml = yaml.dump(cast_configuration.model_dump())
        prompt_content = f"""ROLE:
You are an experienced dialogue writer creating a natural-sounding conversation based on the provided article. The listener should feel as if they're casually dropping into an ongoing exchange.

GOAL:
Craft a conversation that:
1. Accurately covers all key points from the article, presented organically as part of the ongoing discussion.
2. Takes ample time to explore each point in depth as described by the article, without introducing new information.
3. Flows naturally, giving the listener a sense of entering mid-conversation.
4. Includes subtle contextual clues to orient the listener without explicit introductions, greetings, or farewells.
5. Ensures each speaker`s dialogue is distinct, engaging, and authentic to their character profile.

REQUIREMENTS:
- Use short, conversational sentences suitable for speech synthesis.
- Exclude all last names for privacy.
- Do not add speakers beyond those specified in the cast configuration.
- Avoid segments that directly address the listener or acknowledge their presence explicitly.
- Do not include information outside what is explicitly mentioned in the article.
- Include natural speech patterns and filler sounds (e.g., um, ah, (pause), (breath)) to enhance realism (but don't make it forced).
- Present each speaker`s dialogue in complete, coherent paragraphs.
- Maintain an engaging, informative, and seamless dialogue experience.
- DO NOT INCLUDE A SEGMENT FOR THE LISTENER.

CAST CONFIGURATION:
Use the following schema to define speaker and listener profiles:
- Speaker:
- name: Name of the speaker
- background: Background information relevant to the speaker
- expertise: General expertise area
- speaking_style: Description of their speaking style
- level_of_expertise: Detailed expertise level
- focus_aspect: Specific aspect or angle the speaker emphasizes
- depth: Depth of content provided
- Listener:
- name: Optional name of the listener
- expertise: General expertise area of the listener
- summary_of_similar_content: List summarizing similar content known to the listener
- level_of_expertise: Listener's proficiency level
- depth: Desired depth of content for the listener

EXAMPLE (Style Reference):
Imagine dropping into a casual yet intellectually rich conversation between Joe Rogan and Neil deGrasse Tyson discussing space exploration:

Joe:
"So, Neil, you`re telling me we've got satellites out there, right now, literally mapping planets?"

Neil:
"(laughs) Yeah, exactly. (pause) It`s mind-blowing. These satellites send back detailed images, data on atmospheric conditions—everything scientists need to understand these worlds remotely."

Joe:
"Wow. (breath) And they're just floating out there, doing their thing?"

Neil:
"Precisely. And here`s the fascinating part—some missions even search for signs of life. It completely changes how we see ourselves in the universe."

Here's the cast configuration provided for this conversation:
{cast_config_yaml}
"""

        return str(prompt_content)

    async def cast(
        self,
        content: str,
        audio_out_path: str,
        cast_configuration: CastConfiguration | None = None,
    ) -> tuple[str, str]:
        """Convert text into a conversation and generate an audio file."""
        cast_config = cast_configuration or default_cast_configuration

        available_voice_options = self.available_voices.copy()
        speaker_voice_map: dict[str, str] = {}
        for speaker in cast_config.speakers:
            voice_match = difflib.get_close_matches(speaker.name, available_voice_options, n=1, cutoff=0)
            if voice_match:
                selected_voice = voice_match[0]
                available_voice_options.remove(selected_voice)
                speaker_voice_map[speaker.name] = selected_voice
            else:
                selected_voice = secrets_choice(available_voice_options)
                available_voice_options.remove(selected_voice)
                speaker_voice_map[speaker.name] = selected_voice

        system_prompt = self.get_system_prompt(cast_config)
        parser = OnlyJson(with_model=self.with_model)
        conversation_obj = await parser.parse(content, Conversation, system_prompt)
        if not isinstance(conversation_obj, Conversation):
            raise TypeError("Expected Conversation type")

        agent_map: dict[str, str] = {}
        for sp in cast_config.speakers:
            agent_prompt = f"""You are a producer/director of a podcast.
Generate a short paragraph of instructions for the speaker {sp.name} for their persona and how they should speak.
They have the background: {sp.background}. Their expertise {sp.expertise}.
Start it with 'You are ...' and include how the speaker should read and pronounce the words, pace, etc.

Here's an example:
```
You are an experienced art instructor with a warm and refined tone who specializes in post-modernist impressionism.
Accent/Affect: Warm, refined, and gently instructive, reminiscent of a friendly art instructor.
Tone: Calm, encouraging, and articulate, clearly describing each step with patience.
Pacing: Slow and deliberate, pausing often to allow the listener to follow instructions comfortably.
```
"""
            agent_result = await parser.parse(agent_prompt, Instructions, agent_prompt)
            if not isinstance(agent_result, Instructions):
                raise TypeError("Expected Instructions type")

            logger.debug(f"Agent instructions generated for {sp.name}: {agent_result.instructions}")
            agent_map[sp.name] = agent_result.instructions

        combined_audio = AudioSegment.empty()

        for entry in list(conversation_obj.entries):
            delay_duration = entry.pause * 1000
            silent_segment = AudioSegment.silent(duration=int(delay_duration))
            combined_audio += silent_segment

            if entry.speaker:
                voice = speaker_voice_map.get(entry.speaker, secrets_choice(self.available_voices))
                text = entry.message
                instructions = agent_map.get(entry.speaker, "")
            else:
                continue

            response = self.client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
                instructions=instructions,
            )
            with tempfile.NamedTemporaryFile(suffix=".mp3") as tmp_file:
                temp_filename = tmp_file.name
                response.write_to_file(temp_filename)
                audio_segment = AudioSegment.from_file(temp_filename, format="mp3")
            combined_audio += audio_segment
            logger.debug(f"Audio segment added for {entry.speaker}.")

        title_model = AudiocastTitle.generate(content)
        # Use UTC timestamp for filenames
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")  # noqa: UP017
        filename = f"{timestamp}_{title_model.generated_title}.wav"

        audio_out_folder = audio_out_path or Path("generated_podcast") / "podcast_out"
        Path(audio_out_folder).mkdir(parents=True, exist_ok=True)
        audio_file_path = Path(audio_out_folder) / filename
        combined_audio.export(str(audio_file_path), format="wav")
        logger.debug(f"Audio file saved to {audio_file_path}")
        return filename, str(audio_file_path)
