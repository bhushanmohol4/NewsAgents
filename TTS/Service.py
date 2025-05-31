import soundfile as sf
from TTS.Bark import BarkTTS
import numpy as np
import json
import os
from Logging.Logger import logger

class TTSService:
    def __init__(self):
        self.tts = BarkTTS()
        self.voice_presets = {
            "host": "v2/en_speaker_6",
            "guest": "v2/en_speaker_9"
        }
        self.temp_dir = "TTS/temp"
        os.makedirs(self.temp_dir, exist_ok=True)

    def _cleanup_temp_files(self):
        """Clean up temporary audio files."""
        try:
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
        except Exception as e:
            logger.warning(f"Service.py: Failed to cleanup temp files: {str(e)}")

    def generate_audio(self, input_file: str, output_file: str) -> str:
        """
        Generate audio from a podcast script JSON file.
        
        Args:
            input_file (str): Path to the JSON script file
            output_file (str): Path to save the generated audio file
            
        Returns:
            str: Path to the generated audio file
            
        Raises:
            ValueError: If script format is invalid
            FileNotFoundError: If input file doesn't exist
            Exception: For other errors
        """
        try:
            logger.info("Service.py: Starting TTS Service")
            
            # Validate input file
            if not os.path.exists(input_file):
                logger.error(f"Service.py: Input file not found: {input_file}")
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Read and validate script
            with open(input_file, 'r', encoding='utf-8') as f:
                script = json.load(f)
                
            if not script or not isinstance(script, list):
                logger.error("Service.py: Invalid script format")
                raise ValueError("Invalid script format")
            
            # Generate audio segments
            final_audio = []
            total_lines = len(script)
            
            for i, line in enumerate(script, 1):
                logger.info(f"Service.py: Processing line {i}/{total_lines}")
                
                speaker = line["speaker"].lower()
                if speaker not in self.voice_presets:
                    logger.error(f"Service.py: Unknown speaker: {speaker}")
                    raise ValueError(f"Unknown speaker: {speaker}")
                
                text = line["text"]
                if not text or not text.strip():
                    logger.warning(f"Service.py: Empty text for speaker {speaker}, skipping")
                    continue
                
                voice = self.voice_presets[speaker]
                sr, audio = self.tts.long_form_synthesize(text, voice)
                final_audio.append(audio)
                final_audio.append(np.zeros(int(0.65 * sr)))

            if not final_audio:
                logger.error("Service.py: No valid audio segments generated")
                raise ValueError("No valid audio segments generated")

            # Combine and normalize audio
            podcast_audio = np.concatenate(final_audio)
            max_value = np.max(np.abs(podcast_audio))
            if max_value > 1.0:
                podcast_audio = podcast_audio / max_value

            # Save the audio file
            sf.write(output_file, podcast_audio, sr)
            logger.info(f"Service.py: Audio saved to: {output_file}")
            
            # Cleanup
            self._cleanup_temp_files()
            
            return output_file
            
        except Exception as e:
            logger.error(f"Service.py: Error in TTS service: {str(e)}")
            self._cleanup_temp_files()  # Cleanup on error
            raise Exception(f"Error in TTS service: {str(e)}")