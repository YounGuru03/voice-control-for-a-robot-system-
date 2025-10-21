"""
Speaker Identification Agent Module
Handles speaker identification and verification
"""

import numpy as np
from typing import Any, Dict, Optional
import hashlib
from .base_agent import BaseAgent


class SpeakerIDAgent(BaseAgent):
    """Agent responsible for speaker identification"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Speaker ID Agent
        
        Args:
            config: Configuration dictionary containing speaker ID settings
        """
        super().__init__(config)
        self.enabled = config.get('enabled', True)
        self.model_name = config.get('model', 'speechbrain/spkrec-ecapa-voxceleb')
        self.threshold = config.get('threshold', 0.75)
        self.enrolled_speakers = {}
        self.model = None
    
    def initialize(self) -> bool:
        """
        Initialize speaker identification model
        
        Returns:
            bool: True if successful
        """
        if not self.enabled:
            self.logger.info("Speaker identification is disabled")
            self.initialized = True
            return True
        
        try:
            # For offline operation, we'll use a simple feature-based approach
            # In production, you would use SpeechBrain or similar
            self.logger.info("Speaker ID agent initialized (simple mode)")
            self.initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize speaker ID agent: {e}")
            self.initialized = False
            return False
    
    def process(self, audio_data: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Identify or verify speaker from audio
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Dictionary containing speaker identification results
        """
        if not self.initialized:
            self.logger.error("Speaker ID agent not initialized")
            return None
        
        if not self.enabled:
            return {
                'speaker_id': 'unknown',
                'confidence': 0.0,
                'verified': False,
                'message': 'Speaker identification disabled'
            }
        
        if audio_data is None or len(audio_data) == 0:
            self.logger.error("Invalid audio data")
            return None
        
        try:
            # Extract simple audio features for demonstration
            # In production, use proper speaker embeddings
            features = self._extract_features(audio_data)
            
            # Check against enrolled speakers
            if len(self.enrolled_speakers) == 0:
                speaker_id = 'speaker_1'
                self.logger.info("No enrolled speakers, assigning default ID")
            else:
                speaker_id, confidence = self._match_speaker(features)
                self.logger.info(f"Matched speaker: {speaker_id} (confidence: {confidence:.2f})")
            
            return {
                'speaker_id': speaker_id,
                'confidence': 1.0 if len(self.enrolled_speakers) == 0 else confidence,
                'verified': True,
                'features': features
            }
            
        except Exception as e:
            self.logger.error(f"Error during speaker identification: {e}")
            return {
                'speaker_id': 'unknown',
                'confidence': 0.0,
                'verified': False,
                'error': str(e)
            }
    
    def _extract_features(self, audio_data: np.ndarray) -> Dict[str, float]:
        """
        Extract simple audio features for speaker identification
        
        Args:
            audio_data: Audio data
            
        Returns:
            Dictionary of features
        """
        # Simple features for demonstration
        # In production, use MFCC, embeddings, etc.
        features = {
            'mean': float(np.mean(audio_data)),
            'std': float(np.std(audio_data)),
            'energy': float(np.sum(audio_data ** 2)),
            'zero_crossing_rate': float(np.sum(np.abs(np.diff(np.sign(audio_data)))) / (2 * len(audio_data)))
        }
        return features
    
    def _match_speaker(self, features: Dict[str, float]) -> tuple:
        """
        Match features against enrolled speakers
        
        Args:
            features: Extracted audio features
            
        Returns:
            Tuple of (speaker_id, confidence)
        """
        if not self.enrolled_speakers:
            return 'unknown', 0.0
        
        best_match = None
        best_score = 0.0
        
        for speaker_id, enrolled_features in self.enrolled_speakers.items():
            # Simple Euclidean distance in feature space
            distance = sum((features[k] - enrolled_features[k]) ** 2 
                          for k in features.keys()) ** 0.5
            score = max(0, 1 - distance)
            
            if score > best_score:
                best_score = score
                best_match = speaker_id
        
        return best_match or 'unknown', best_score
    
    def enroll_speaker(self, speaker_id: str, audio_data: np.ndarray) -> bool:
        """
        Enroll a new speaker
        
        Args:
            speaker_id: Unique identifier for the speaker
            audio_data: Audio sample from the speaker
            
        Returns:
            bool: True if successful
        """
        try:
            features = self._extract_features(audio_data)
            self.enrolled_speakers[speaker_id] = features
            self.logger.info(f"Enrolled speaker: {speaker_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to enroll speaker: {e}")
            return False
    
    def shutdown(self):
        """Cleanup resources"""
        self.enrolled_speakers = {}
        self.model = None
        self.logger.info("Speaker ID agent shutdown")
