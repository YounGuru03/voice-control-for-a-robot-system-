"""
Input Agent Module
Handles audio input capture from microphone
"""

import numpy as np
import sounddevice as sd
from typing import Any, Dict, Optional
from .base_agent import BaseAgent


class InputAgent(BaseAgent):
    """Agent responsible for capturing audio input"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Input Agent
        
        Args:
            config: Configuration dictionary containing audio settings
        """
        super().__init__(config)
        self.sample_rate = config.get('sample_rate', 16000)
        self.channels = config.get('channels', 1)
        self.device = config.get('device', None)
        self.chunk_duration = config.get('chunk_duration', 5)
        self.silence_threshold = config.get('silence_threshold', 0.01)
        self.recording = False
    
    def initialize(self) -> bool:
        """
        Initialize audio input device
        
        Returns:
            bool: True if successful
        """
        try:
            # Test if the audio device is available
            devices = sd.query_devices()
            self.logger.info(f"Available audio devices: {len(devices)}")
            
            if self.device is None:
                self.device = sd.default.device[0]
                self.logger.info(f"Using default input device: {self.device}")
            
            # Test recording
            test_duration = 0.1
            test_audio = sd.rec(
                int(test_duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device
            )
            sd.wait()
            
            self.initialized = True
            self.logger.info("Input agent initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize input agent: {e}")
            self.initialized = False
            return False
    
    def process(self, data: Any = None) -> Optional[np.ndarray]:
        """
        Capture audio input
        
        Args:
            data: Optional duration override in seconds
            
        Returns:
            numpy array containing audio data, or None if failed
        """
        if not self.initialized:
            self.logger.error("Input agent not initialized")
            return None
        
        try:
            duration = data if data is not None else self.chunk_duration
            
            self.logger.info(f"Recording audio for {duration} seconds...")
            self.recording = True
            
            # Record audio
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device,
                dtype='float32'
            )
            sd.wait()
            
            self.recording = False
            
            # Check if audio contains actual sound (not just silence)
            audio_level = np.abs(audio_data).mean()
            if audio_level < self.silence_threshold:
                self.logger.warning("Audio level too low, possibly silence")
            
            self.logger.info(f"Audio captured: {audio_data.shape}, level: {audio_level:.4f}")
            
            # Flatten if multi-channel
            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()
            
            return audio_data
            
        except Exception as e:
            self.logger.error(f"Error capturing audio: {e}")
            self.recording = False
            return None
    
    def shutdown(self):
        """Stop recording and cleanup"""
        self.recording = False
        self.logger.info("Input agent shutdown")
    
    def list_devices(self) -> list:
        """
        List available audio input devices
        
        Returns:
            List of device information
        """
        try:
            devices = sd.query_devices()
            return [d for i, d in enumerate(devices) if d['max_input_channels'] > 0]
        except Exception as e:
            self.logger.error(f"Error listing devices: {e}")
            return []
