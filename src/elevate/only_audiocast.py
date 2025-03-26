import io
import os
import random
from datetime import datetime

from dotenv import load_dotenv
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs, VoiceSettings, Voice
from typing import Optional, List  # added import for List
from pydantic import BaseModel
from .only_json import OnlyJson  # new import for JSON parsing
import yaml  # new import for YAML handling
import difflib  # added import for matching

# Load environment variables
load_dotenv()


class SpeakerConfig(BaseModel):
    name: str
    background: str
    expertise: str
    speaking_style: str
    level_of_expertise: str
    focus_aspect: str
    depth: str


class ListenerConfig(BaseModel):
    name: str | None = None
    expertise: str
    summary_of_similar_content: list
    level_of_expertise: str
    depth: str


class CastConfiguration(BaseModel):
    speakers: list[SpeakerConfig]
    listener: ListenerConfig


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
    speaker: str
    message: str


class Conversation(BaseModel):
    entries: List[ConversationEntry]


class OnlyAudiocast:
    """Class that converts text into an audio file using ElevenLabs."""

    def __init__(self) -> None:
        """Initialize the OnlyAudiocast class."""
        # Check if ffmpeg is installed
        if not AudioSegment.ffmpeg:
            raise Exception(
                "ffmpeg is not installed. Try installing it as `brew install ffmpeg`, or whatever is appropriate for your OS."
            )

        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        # Define voice settings for speakers only
        self.speaker_voice_settings = VoiceSettings(
            stability=0.45,
            similarity_boost=0.75,
            style=0.2,
        )
        # Initialize voice configurations based on provider (using only speakers)
        self.voice_configurations = {
            "elevenlabs": {
                "9BWtsMINqrJLrRacOk9x": "Aria",
                "CwhRBWXzGAHq8TQ4Fs17": "Roger",
                "EXAVITQu4vr4xnSDxMaL": "Sarah",
                "FGY2WhTYpPnrIDTdsKH5": "Laura",
                "IKne3meq5aSn9XLyUdCD": "Charlie",
                "JBFqnCBsd6RMkjVDRZzb": "George",
                "N2lVS1w4EtoT3dr4eOWO": "Callum",
                "SAz9YHcvj6GT2YYXdXww": "River",
                "TX3LPaxmHKxFdv7VOQHJ": "Liam",
                "XB0fDUnXU5powFXDhCwa": "Charlotte",
                "Xb7hH8MSUJpSbSDYk0k2": "Alice",
                "XrExE9yKIg1WjnnlVkGX": "Matilda",
                "bIHbv24MWmeRgasZH58o": "Will",
                "cgSgspJ2msm6clMCkdW9": "Jessica",
                "cjVigY5qzO86Huf0OWal": "Eric",
                "iP95p4xoKVk53GoZ742B": "Chris",
                "nPczCjzI2devNBz1zQrb": "Brian",
                "onwK4e9ZLuTAKqWW03F9": "Daniel",
                "pFZP5JQG7iQjIQuC4Bku": "Lily",
                "pqHfZKP75CvOlQylNhV4": "Bill",
            }
        }

    def get_system_prompt(self, cast_configuration: CastConfiguration) -> dict:
        """
        Generate a system prompt with embedded cast configuration in YAML.
        """
        cast_config_yaml = yaml.dump(cast_configuration.dict())
        prompt_content = (
            "you are an experienced podcast producer.\n"
            "- Based on an article you create an engaging script for the podcast.\n"
            "- Make the conversationfully covers the content, with clear articulated speaker mono/dialogues.\n"
            "- Use short sentences that are easily used with speech synthesis.\n"
            "- The conversation should have excitement and natural filler words like 'äh'.\n"
            "- Do not mention last names.\n"
            "- Each conversation entry should be complete and coherent paragraphs.\n"
            '- Avoid lines such as: "Thanks for having me, Marina!"\n'
            "\nHere's the cast configuration including speaker and listener profiles:\n"
            + cast_config_yaml
        )
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

        # Build a mapping from speaker name to voice_id without repeating voices
        available_voice_options = dict(self.voice_configurations["elevenlabs"])
        speaker_voice_map = {}
        for speaker in cast_config.speakers:
            voice_names = list(available_voice_options.values())
            match = difflib.get_close_matches(speaker.name, voice_names, n=1, cutoff=0)
            if match:
                best_voice_name = match[0]
                for vid, vname in available_voice_options.items():
                    if vname == best_voice_name:
                        speaker_voice_map[speaker.name] = vid
                        del available_voice_options[vid]
                        break
            else:
                vid, _ = available_voice_options.popitem()
                speaker_voice_map[speaker.name] = vid

        system_prompt = self.get_system_prompt(cast_config)
        parser = OnlyJson()
        conversation_obj: Conversation = parser.parse(
            content, Conversation, system_prompt
        )

        combined_audio = AudioSegment.empty()
        for entry in conversation_obj.entries:
            if entry.speaker:
                # Use speaker_voice_map based on the entry speaker name
                voice_id = speaker_voice_map.get(entry.speaker)
                if not voice_id:
                    voice_id = random.choice(
                        list(self.voice_configurations["elevenlabs"].keys())
                    )
                settings = self.speaker_voice_settings
                text = entry.message
                speaker = entry.speaker
            else:
                continue  # Skip unrecognized entries

            # Generate audio with custom voice settings
            audio_generator = self.client.generate(
                text=text,
                voice=Voice(voice_id=voice_id, settings=settings),
                model="eleven_multilingual_v2",
            )

            # Initialize a bytes buffer and collect the audio chunks
            buffer = io.BytesIO()
            for chunk in audio_generator:
                buffer.write(chunk)
            buffer.seek(0)
            audio_segment = AudioSegment.from_file(buffer, format="mp3")
            combined_audio += audio_segment
            print(f"Audio segment added for {speaker}.")

            # Add a random delay (0.2 to 0.5 seconds)
            delay_duration = random.uniform(0.2, 0.5) * 1000  # Convert to milliseconds
            silent_segment = AudioSegment.silent(duration=delay_duration)
            combined_audio += silent_segment

        # Generate a filename with a timestamp (updated to remove guest part)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Use first speaker's name for the filename
        filename = f"{timestamp}_conversation.mp3"
        audio_out_folder = audio_out_path or os.path.join(
            "generated_podcast", "podcast_out"
        )
        os.makedirs(audio_out_folder, exist_ok=True)
        audio_file_path = os.path.join(audio_out_folder, filename)
        combined_audio.export(audio_file_path, format="mp3")
        print(f"Audio file saved to {audio_file_path}")
        return filename, audio_file_path
