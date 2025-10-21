"""
Command Parser Agent Module
Handles parsing transcribed text into actionable commands
"""

import yaml
from typing import Any, Dict, Optional, List
from difflib import SequenceMatcher
from .base_agent import BaseAgent


class CommandParserAgent(BaseAgent):
    """Agent responsible for parsing text into commands"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Command Parser Agent
        
        Args:
            config: Configuration dictionary containing parser settings
        """
        super().__init__(config)
        self.commands_file = config.get('commands_file', 'config/commands.yaml')
        self.fuzzy_matching = config.get('fuzzy_matching', True)
        self.confidence_threshold = config.get('confidence_threshold', 0.6)
        self.commands = {}
        self.aliases = {}
    
    def initialize(self) -> bool:
        """
        Load command definitions from YAML file
        
        Returns:
            bool: True if successful
        """
        try:
            with open(self.commands_file, 'r') as f:
                data = yaml.safe_load(f)
            
            self.commands = data.get('commands', {})
            self.aliases = data.get('aliases', {})
            
            self.logger.info(f"Loaded {len(self.commands)} commands and {len(self.aliases)} aliases")
            self.initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load commands: {e}")
            self.initialized = False
            return False
    
    def process(self, transcription: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse transcription into command
        
        Args:
            transcription: Dictionary containing 'text' key with transcribed text
            
        Returns:
            Dictionary containing parsed command info, or None if no match
        """
        if not self.initialized:
            self.logger.error("Command parser not initialized")
            return None
        
        if not transcription or 'text' not in transcription:
            self.logger.error("Invalid transcription data")
            return None
        
        text = transcription['text'].lower().strip()
        self.logger.info(f"Parsing command from: '{text}'")
        
        # Check aliases first
        if text in self.aliases:
            text = self.aliases[text]
            self.logger.info(f"Alias resolved to: '{text}'")
        
        # Exact match
        if text in self.commands:
            command = self.commands[text]
            self.logger.info(f"Exact match found: {command}")
            return {
                'command': command,
                'original_text': transcription['text'],
                'matched_text': text,
                'confidence': 1.0,
                'match_type': 'exact'
            }
        
        # Fuzzy matching
        if self.fuzzy_matching:
            best_match, confidence = self._fuzzy_match(text)
            
            if best_match and confidence >= self.confidence_threshold:
                command = self.commands[best_match]
                self.logger.info(f"Fuzzy match found: {command} (confidence: {confidence:.2f})")
                return {
                    'command': command,
                    'original_text': transcription['text'],
                    'matched_text': best_match,
                    'confidence': confidence,
                    'match_type': 'fuzzy'
                }
            else:
                self.logger.warning(f"No match found above threshold (best: {confidence:.2f})")
        
        # No match found
        self.logger.warning(f"No command match for: '{text}'")
        return {
            'command': 'UNKNOWN',
            'original_text': transcription['text'],
            'matched_text': None,
            'confidence': 0.0,
            'match_type': 'none'
        }
    
    def _fuzzy_match(self, text: str) -> tuple:
        """
        Find best fuzzy match for text
        
        Args:
            text: Text to match
            
        Returns:
            Tuple of (best_match, confidence)
        """
        best_match = None
        best_ratio = 0.0
        
        for command_text in self.commands.keys():
            ratio = SequenceMatcher(None, text, command_text).ratio()
            
            # Also check if command text is contained in input
            if command_text in text or text in command_text:
                ratio = max(ratio, 0.8)
            
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = command_text
        
        return best_match, best_ratio
    
    def shutdown(self):
        """Cleanup resources"""
        self.commands = {}
        self.aliases = {}
        self.logger.info("Command parser agent shutdown")
    
    def get_available_commands(self) -> List[str]:
        """
        Get list of available commands
        
        Returns:
            List of command text strings
        """
        return list(self.commands.keys())
    
    def add_command(self, text: str, action: str):
        """
        Add a new command at runtime
        
        Args:
            text: Command text trigger
            action: Command action name
        """
        self.commands[text.lower()] = action
        self.logger.info(f"Added command: '{text}' -> {action}")
