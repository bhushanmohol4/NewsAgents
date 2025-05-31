import nltk
import torch
import warnings
import numpy as np
from transformers import AutoProcessor, BarkModel
from Logging.Logger import logger

warnings.filterwarnings(
    "ignore",
    message="torch.nn.utils.weight_norm is deprecated in favor of torch.nn.utils.parametrizations.weight_norm.",
)


class BarkTTS:
    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        Initializes the TextToSpeechService class.
        Args:
            device (str, optional): The device to be used for the model, either "cuda" if a GPU is available or "cpu".
            Defaults to "cuda" if available, otherwise "cpu".
        """
        self.device = device
        self.processor = AutoProcessor.from_pretrained("suno/bark-small")
        self.model = BarkModel.from_pretrained("suno/bark-small")
        self.model.to(self.device)

    def synthesize(self, text, voice_preset):
        """
        Synthesizes audio from the given text using the specified voice preset.
        Args:
            text: The input text to be synthesized.
            voice_preset: The voice preset to be used for the synthesis. Defaults to "v2/en_speaker_1".
        Returns:
            tuple: A tuple containing the sample rate and the generated audio array.
        """
        inputs = self.processor(text, voice_preset = voice_preset, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        logger.info("Bark.py: Generating audio for chunk")
        with torch.no_grad():
            audio_array = self.model.generate(**inputs, pad_token_id=10000)

        audio_array = audio_array.cpu().numpy().squeeze()
        sample_rate = self.model.generation_config.sample_rate
        return sample_rate, audio_array

    def long_form_synthesize(self, text, voice_preset):
        """
        Synthesizes audio from the given long-form text using the specified voice preset.
        
        Args:
            text (str): The input text to be synthesized
            voice_preset (str): The voice preset to be used for the synthesis
            
        Returns:
            tuple: A tuple containing the sample rate and the generated audio array
            
        Raises:
            ValueError: If text is empty or voice_preset is invalid
        """
        logger.info("Bark.py: Starting audio synthesis")
        
        # Validate inputs
        if not text or not text.strip():
            logger.error("Bark.py: Empty text provided")
            raise ValueError("Text cannot be empty")
        
        if not voice_preset or not isinstance(voice_preset, str):
            logger.error("Bark.py: Invalid voice preset")
            raise ValueError("Invalid voice preset")
        
        try:
            pieces = []
            sentences = nltk.sent_tokenize(text)
            
            # Handle very long texts by limiting chunk size
            max_chunk_size = 10  # sentences per chunk
            chunks = []
            for i in range(0, len(sentences), max_chunk_size):
                chunk = " ".join(sentences[i:i + max_chunk_size])
                chunks.append(chunk)
            
            silence = np.zeros(int(0.25 * self.model.generation_config.sample_rate))
            
            # Process chunks with progress tracking
            total_chunks = len(chunks)
            for i, chunk in enumerate(chunks, 1):
                logger.info(f"Bark.py: Processing chunk {i}/{total_chunks}")
                sample_rate, audio_array = self.synthesize(chunk, voice_preset)
                pieces.append(audio_array)
                pieces.append(silence.copy())
            
            logger.info("Bark.py: Audio synthesis completed")
            return self.model.generation_config.sample_rate, np.concatenate(pieces)
            
        except Exception as e:
            logger.error(f"Bark.py: Error in audio synthesis: {str(e)}")
            raise Exception(f"Error in audio synthesis: {str(e)}")   