"""
Recognition Agent Module
Handles speech-to-text using OpenAI Whisper (offline)
"""

import whisper
import numpy as np
from typing import Any, Dict, Optional
from .base_agent import BaseAgent


class RecognitionAgent(BaseAgent):
    """Agent responsible for speech recognition using Whisper"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Recognition Agent
        
        Args:
            config: Configuration dictionary containing Whisper settings
        """
        super().__init__(config)
        self.model_size = config.get('model_size', 'base')
        self.device = config.get('device', 'cpu')
        self.language = config.get('language', 'en')
        self.model = None
    
    def initialize(self) -> bool:
        """
        Initialize Whisper model (downloads if needed)
        
        Returns:
            bool: True if successful
        """
        try:
            self.logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size, device=self.device)
            self.initialized = True
            self.logger.info("Recognition agent initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize recognition agent: {e}")
            self.initialized = False
            return False
    
    def process(self, audio_data: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Transcribe audio to text using Whisper
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Dictionary containing transcription results, or None if failed
        """
        if not self.initialized or self.model is None:
            self.logger.error("Recognition agent not initialized")
            return None
        
        if audio_data is None or len(audio_data) == 0:
            self.logger.error("Invalid audio data")
            return None
        
        try:
            # Ensure audio is float32 and normalized
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Whisper expects audio between -1 and 1
            max_val = np.abs(audio_data).max()
            if max_val > 1.0:
                audio_data = audio_data / max_val
            
            self.logger.info("Transcribing audio...")
            
            # Transcribe
            result = self.model.transcribe(
                audio_data,
                language=self.language if self.language else None,
                fp16=False  # Use fp32 for CPU compatibility
            )
            
            text = result['text'].strip()
            self.logger.info(f"Transcription: '{text}'")
            
            return {
                'text': text,
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', []),
                'raw_result': result
            }
            
        except Exception as e:
            self.logger.error(f"Error during transcription: {e}")
            return None
    
    def shutdown(self):
        """Cleanup model resources"""
        if self.model is not None:
            del self.model
            self.model = None
        self.logger.info("Recognition agent shutdown")
    
    def get_available_models(self) -> list:
        """
        Get list of available Whisper models
        
        Returns:
            List of model names
        """
        return ['tiny', 'base', 'small', 'medium', 'large']
