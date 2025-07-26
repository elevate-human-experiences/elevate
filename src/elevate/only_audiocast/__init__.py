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
from jinja2 import Template
from openai import OpenAI
from pydantic import BaseModel, Field
from pydub import AudioSegment

from common import setup_logging

from ..only_json import JsonConfig, OnlyJson


logger = setup_logging(logging.INFO)


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


class AudiocastConfig(BaseModel):
    """Configuration for OnlyAudiocast class."""

    model: str = Field(default="o1", description="LLM model to use")


class AudiocastInput(BaseModel):
    """Input model for audiocast generation."""

    content: str = Field(..., description="Content to convert to audiocast")
    audio_out_path: str = Field(..., description="Output path for audio file")
    cast_configuration: CastConfiguration | None = Field(default=None, description="Cast configuration")


class AudiocastOutput(BaseModel):
    """Output model for audiocast generation."""

    filename: str = Field(..., description="Generated audio filename")
    file_path: str = Field(..., description="Full path to generated audio file")


class OnlyAudiocast:
    """Converts text into an audio file using the GPT-4o model."""

    def __init__(self, config: AudiocastConfig) -> None:
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
        self.config = config

    def _load_prompt_template(self) -> Template:
        """Load the Jinja2 template from instructions.j2 file."""
        template_path = Path(__file__).parent / "instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def _load_agent_template(self) -> Template:
        """Load the Jinja2 template for agent instructions."""
        template_path = Path(__file__).parent / "agent_instructions.j2"
        with template_path.open(encoding="utf-8") as f:
            template_content = f.read()
        return Template(template_content)

    def get_system_prompt(self, cast_configuration: CastConfiguration) -> str:
        """Generate a system prompt with cast configuration in YAML."""
        cast_config_yaml = yaml.dump(cast_configuration.model_dump())
        template = self._load_prompt_template()
        return str(template.render(cast_config_yaml=cast_config_yaml))

    def get_agent_prompt(self, speaker: SpeakerConfig) -> str:
        """Generate agent instructions prompt using template."""
        template = self._load_agent_template()
        return str(
            template.render(
                speaker_name=speaker.name, speaker_background=speaker.background, speaker_expertise=speaker.expertise
            )
        )

    async def cast(self, input_data: AudiocastInput) -> AudiocastOutput:
        """Convert text into a conversation and generate an audio file."""
        cast_config = input_data.cast_configuration or default_cast_configuration

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
        parser = OnlyJson(config=JsonConfig(model=self.config.model))
        from ..only_json import JsonInput

        conversation_obj = await parser.parse(
            JsonInput(content=input_data.content, schema=Conversation, system_prompt=system_prompt)
        )
        if not isinstance(conversation_obj, Conversation):
            raise TypeError("Expected Conversation type")

        agent_map: dict[str, str] = {}
        for sp in cast_config.speakers:
            agent_prompt = self.get_agent_prompt(sp)
            agent_result = await parser.parse(
                JsonInput(content=agent_prompt, schema=Instructions, system_prompt=agent_prompt)
            )
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

        title_model = AudiocastTitle.generate(input_data.content)
        # Use UTC timestamp for filenames
        timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")  # noqa: UP017
        filename = f"{timestamp}_{title_model.generated_title}.wav"

        audio_out_folder = input_data.audio_out_path or Path("generated_podcast") / "podcast_out"
        Path(audio_out_folder).mkdir(parents=True, exist_ok=True)
        audio_file_path = Path(audio_out_folder) / filename
        combined_audio.export(str(audio_file_path), format="wav")
        logger.debug(f"Audio file saved to {audio_file_path}")
        return AudiocastOutput(filename=filename, file_path=str(audio_file_path))
