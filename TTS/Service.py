import soundfile as sf
from TTS.Bark import BarkTTS
import numpy as np
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
import time
import os
import json

class TTSInput(BaseModel):
        input_file: str = Field(
            ...,
            description="Path to the JSON script file (e.g., 'output/podcast_script.json')"
        )
        output_file: str = Field(
            ...,
            description="Path to save the generated audio file (e.g., 'TTS/Recordings/podcast.wav')"
        )

class ttsService(BaseTool):
    name: str = "Text-to-Speech Tool to generate audio from text"
    description: str = "Generates a mono-speaker podcast audio file from a list of dialogues."
    args_schema: Type[BaseModel] = TTSInput

    def _run(self, input_file: str, output_file: str):
        try:
            # Ensure Recordings directory exists
            os.makedirs("TTS/Recordings", exist_ok=True)
            
            # Instantiate the TTS service
            tts = BarkTTS()

            voice_presets = {
                "host": "v2/en_speaker_6",
                "guest": "v2/en_speaker_9"
            }

            with open(input_file, 'r', encoding='utf-8') as f:
                script = json.load(f)

            # Generate audio segments
            final_audio = []
            for line in script:
                speaker = line["speaker"].lower()  # Convert to lowercase for consistency
                if speaker not in voice_presets:
                    raise ValueError(f"Unknown speaker: {speaker}. Must be one of: {list(voice_presets.keys())}")
                
                text = line["text"]
                voice = voice_presets[speaker]

                sr, audio = tts.long_form_synthesize(text, voice)
                final_audio.append(audio)

                final_audio.append(np.zeros(int(0.65 * sr)))  # silence

            # Concatenate and save final podcast audio
            podcast_audio = np.concatenate(final_audio)

            # Normalize audio to prevent clipping
            max_value = np.max(np.abs(podcast_audio))
            if max_value > 1.0:
                podcast_audio = podcast_audio / max_value

            podcast_file = "output/Recordings/podcast.wav"
            sf.write(podcast_file, podcast_audio, sr)

            if not os.path.exists(podcast_file):
                raise FileNotFoundError(f"Failed to save podcast file at {podcast_file}")

            return podcast_audio
            
        except Exception as e:
            raise Exception(f"Error in TTS service: {str(e)}")