import soundfile as sf
from TTS.Bark import BarkTTS
import numpy as np
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
import time

# Sample script
script = [
        {"speaker": "host", "text": "Welcome to our podcast. I'm your host, Sarah."},
        {"speaker": "guest", "text": "Thank you for having me, Sarah. It's great to be here."},
        {"speaker": "host", "text": "Let’s dive into today’s topic."}
    ]

class TextToSpeechToolInput(BaseModel):
    """Input schema for TextToSpeechTool."""
    script: List[str] = Field(
        ...,
        description="List of dialogues (strings) for text-to-speech conversion."
    )

class ttsService(BaseTool):
    name: str = "Text-to-Speech Tool to generate audio from text"
    description: str = "Generates a mono-speaker podcast audio file from a list of dialogues."
    args_schema: Type[BaseModel] = TextToSpeechToolInput

    def _run(self, script: List[str] = script):
        # Instantiate the TTS service
        tts = BarkTTS()

        voice_presets = {
            "host": "v2/en_speaker_6",
            "guest": "v2/en_speaker_9"
        }

        # Generate audio segments
        final_audio = []
        for line in script:
            speaker = line["speaker"]
            text = line["text"]
            voice = voice_presets[speaker]

            sr, audio = tts.long_form_synthesize(text, voice)
            final_audio.append(audio)

            final_audio.append(np.zeros(int(0.65 * sr)))  # silence

        # Concatenate and save final podcast audio
        podcast_audio = np.concatenate(final_audio)
        podcast_file = f"TTS/Recordings/podcast.wav"
        sf.write("Recordings/podcast.wav", podcast_audio, sr)

        return podcast_file