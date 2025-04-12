import io
import os
import random
from datetime import datetime

from dotenv import load_dotenv
from pydub import AudioSegment
from openai import OpenAI  # new import for GPT-4o
from pathlib import Path  # new import for file path management
import tempfile  # to create temporary files for audio
from typing import Optional, List  # added import for List
from pydantic import BaseModel, Field  # modified to include Field
from .only_json import OnlyJson  # new import for JSON parsing
import yaml  # new import for YAML handling
import difflib  # added import for matching

# Load environment variables
load_dotenv()


class SpeakerConfig(BaseModel):
    name: str = Field(..., description="Speaker's name")
    background: str = Field(..., description="Speaker background information")
    expertise: str = Field(..., description="Expertise level of the speaker")
    speaking_style: str = Field(..., description="Style of the speaker's delivery")
    level_of_expertise: str = Field(..., description="Detailed expertise level")
    focus_aspect: str = Field(..., description="Aspect the speaker is focusing on")
    depth: str = Field(..., description="Depth of content provided by the speaker")


class ListenerConfig(BaseModel):
    name: str | None = Field(default=None, description="Listener's name (optional)")
    expertise: str = Field(..., description="Expertise level of the listener")
    summary_of_similar_content: list = Field(
        ..., description="Summaries of similar content"
    )
    level_of_expertise: str = Field(..., description="Listener's proficiency level")
    depth: str = Field(..., description="Depth of content for the listener")


class CastConfiguration(BaseModel):
    speakers: list[SpeakerConfig] = Field(
        ..., description="List of speaker configurations"
    )
    listener: ListenerConfig = Field(..., description="Configuration for the listener")


class Instructions(BaseModel):
    instructions: str = Field(..., description="Instructions for the agent")


# Default configuration for a single narrator technical podcast
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
    pause: float = Field(
        default=0.5,
        description="Pause duration between conversation segments. In seconds. 0 means other/interrupting.",
        json_schema_extra={"minimum": 0.0, "maximum": 2.0},
    )
    speaker: str = Field(..., description="Name of the conversation speaker")
    message: str = Field(..., description="Message content of the entry")


class Conversation(BaseModel):
    entries: List[ConversationEntry] = Field(
        ..., description="List of conversation entries"
    )


# New Pydantic class to generate an audiocast title based on content
class AudiocastTitle(BaseModel):
    generated_title: str = Field(
        ..., description="Title derived from the conversation content"
    )

    @classmethod
    def generate(cls, content: str) -> "AudiocastTitle":
        # Generate a simple title by taking the first 10 words from the provided content
        words = content.split()[:10]
        title = " ".join(words) if words else "Audiocast"
        # Clean title by replacing spaces with underscores and limit length
        title_snippet = title.replace(" ", "_")[:30]
        return cls(generated_title=title_snippet)


class OnlyAudiocast:
    """Class that converts text into an audio file using GPT-4o model."""

    def __init__(self) -> None:
        """Initialize the OnlyAudiocast class."""
        # Check if ffmpeg is installed
        if not AudioSegment.ffmpeg:
            raise Exception(
                "ffmpeg is not installed. Try installing it as `brew install ffmpeg`, or whatever is appropriate for your OS."
            )

        # Initialize OpenAI client
        self.client = OpenAI()
        # Define available voices for GPT-4o
        self.available_voices = [
            "alloy",
            "fable",
            "onyx",
            "nova",
            "shimmer",
        ]

    def get_system_prompt(self, cast_configuration: CastConfiguration) -> dict:
        """
        Generate a system prompt with embedded cast configuration in YAML.
        """
        cast_config_yaml = yaml.dump(cast_configuration.model_dump())
        prompt_content = f"""ROLE:
You are an experienced dialogue writer creating a natural-sounding conversation based on the provided article. The listener should feel as if they're casually dropping into an ongoing exchange.

GOAL:
Craft a conversation that:
1. Accurately covers all key points from the article, presented organically as part of the ongoing discussion.
2. Takes ample time to explore each point in depth as described by the article, without introducing new information.
3. Flows naturally, giving the listener a sense of entering mid-conversation.
4. Includes subtle contextual clues to orient the listener without explicit introductions, greetings, or farewells.
5. Ensures each speaker’s dialogue is distinct, engaging, and authentic to their character profile.

REQUIREMENTS:
- Use short, conversational sentences suitable for speech synthesis.
- Exclude all last names for privacy.
- Do not add speakers beyond those specified in the cast configuration.
- Avoid segments that directly address the listener or acknowledge their presence explicitly.
- Do not include information outside what is explicitly mentioned in the article.
- Include natural speech patterns and filler sounds (e.g., um, ah, (pause), (breath)) to enhance realism (but don't make it forced).
- Present each speaker’s dialogue in complete, coherent paragraphs.
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
"So, Neil, you’re telling me we've got satellites out there, right now, literally mapping planets?"

Neil:
"(laughs) Yeah, exactly. (pause) It’s mind-blowing. These satellites send back detailed images, data on atmospheric conditions—everything scientists need to understand these worlds remotely."

Joe:
"Wow. (breath) And they're just floating out there, doing their thing?"

Neil:
"Precisely. And here’s the fascinating part—some missions even search for signs of life. It completely changes how we see ourselves in the universe."

Here's the cast configuration provided for this conversation:
{cast_config_yaml}
"""

        return prompt_content

    def cast(
        self,
        content: str,
        audio_out_path: str,
        cast_configuration: Optional[CastConfiguration] = None,
    ) -> tuple:
        """
        Convert the provided content text into a conversation using JSON schema validation,
        then convert the conversation into an audio file.
        """
        # Use provided or default cast configuration
        cast_config = cast_configuration or default_cast_configuration

        # Build a mapping from speaker name to voice without repetition
        available_voice_options = self.available_voices.copy()
        speaker_voice_map = {}
        for speaker in cast_config.speakers:
            voice_match = difflib.get_close_matches(
                speaker.name, available_voice_options, n=1, cutoff=0
            )
            if voice_match:
                selected_voice = voice_match[0]
                available_voice_options.remove(selected_voice)
                speaker_voice_map[speaker.name] = selected_voice
            else:
                selected_voice = random.choice(available_voice_options)
                available_voice_options.remove(selected_voice)
                speaker_voice_map[speaker.name] = selected_voice

        system_prompt = self.get_system_prompt(cast_config)
        parser = OnlyJson(with_model="o1")
        conversation_obj: Conversation = parser.parse(
            content, Conversation, system_prompt
        )

        # Compute agent for each speaker using OnlyJson
        agent_map = {}
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
            agent_result: Instructions = parser.parse(
                agent_prompt, Instructions, agent_prompt
            )
            print(
                f"Agent instructions generated for {sp.name}: {agent_result.instructions}"
            )
            agent_map[sp.name] = agent_result.instructions

        combined_audio = AudioSegment.empty()

        for entry in conversation_obj.entries:
            delay_duration = entry.pause * 1000  # milliseconds
            silent_segment = AudioSegment.silent(duration=delay_duration)
            combined_audio += silent_segment

            if entry.speaker:
                voice = speaker_voice_map.get(
                    entry.speaker, random.choice(self.available_voices)
                )
                text = entry.message
                instructions = agent_map.get(entry.speaker, "")
            else:
                continue  # Skip unrecognized entries

            # Generate audio using GPT-4o (simulate streaming by writing to a temp file)
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
            print(f"Audio segment added for {entry.speaker}.")

        # Generate title from provided content using the AudiocastTitle model
        title_model = AudiocastTitle.generate(content)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use the generated title snippet in the filename
        filename = f"{timestamp}_{title_model.generated_title}.wav"

        audio_out_folder = audio_out_path or os.path.join(
            "generated_podcast", "podcast_out"
        )
        os.makedirs(audio_out_folder, exist_ok=True)
        audio_file_path = os.path.join(audio_out_folder, filename)
        combined_audio.export(audio_file_path, format="wav")
        print(f"Audio file saved to {audio_file_path}")
        return filename, audio_file_path
