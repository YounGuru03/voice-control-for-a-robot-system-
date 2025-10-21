"""
Logging Agent Module
Handles file logging of all system activities
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional
from .base_agent import BaseAgent


class LoggingAgent(BaseAgent):
    """Agent responsible for logging system activities to files"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Logging Agent
        
        Args:
            config: Configuration dictionary containing logging settings
        """
        super().__init__(config)
        self.enabled = config.get('enabled', True)
        self.log_dir = config.get('log_dir', 'logs')
        self.log_audio = config.get('log_audio', False)
        self.log_transcripts = config.get('log_transcripts', True)
        self.log_commands = config.get('log_commands', True)
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = None
    
    def initialize(self) -> bool:
        """
        Initialize logging system and create log files
        
        Returns:
            bool: True if successful
        """
        if not self.enabled:
            self.logger.info("Logging is disabled")
            self.initialized = True
            return True
        
        try:
            # Create logs directory if it doesn't exist
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Create session log file
            log_filename = f"session_{self.session_id}.jsonl"
            self.log_file = os.path.join(self.log_dir, log_filename)
            
            # Write session start entry
            self._write_log({
                'type': 'session_start',
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id
            })
            
            self.logger.info(f"Logging initialized: {self.log_file}")
            self.initialized = True
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize logging agent: {e}")
            self.initialized = False
            return False
    
    def process(self, log_data: Dict[str, Any]) -> bool:
        """
        Log data to file
        
        Args:
            log_data: Dictionary containing data to log
            
        Returns:
            bool: True if successful
        """
        if not self.initialized or not self.enabled:
            return False
        
        try:
            # Add timestamp if not present
            if 'timestamp' not in log_data:
                log_data['timestamp'] = datetime.now().isoformat()
            
            # Filter based on log type settings
            log_type = log_data.get('type', 'unknown')
            
            if log_type == 'transcription' and not self.log_transcripts:
                return True
            
            if log_type == 'command' and not self.log_commands:
                return True
            
            if log_type == 'audio' and not self.log_audio:
                return True
            
            # Write to log file
            self._write_log(log_data)
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging data: {e}")
            return False
    
    def _write_log(self, data: Dict[str, Any]):
        """
        Write log entry to file
        
        Args:
            data: Log data dictionary
        """
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write log: {e}")
    
    def log_transcription(self, transcription: Dict[str, Any], speaker_info: Optional[Dict[str, Any]] = None):
        """
        Log a transcription event
        
        Args:
            transcription: Transcription data
            speaker_info: Optional speaker identification data
        """
        log_entry = {
            'type': 'transcription',
            'text': transcription.get('text', ''),
            'language': transcription.get('language', 'unknown')
        }
        
        if speaker_info:
            log_entry['speaker_id'] = speaker_info.get('speaker_id', 'unknown')
            log_entry['speaker_confidence'] = speaker_info.get('confidence', 0.0)
        
        self.process(log_entry)
    
    def log_command(self, command_data: Dict[str, Any]):
        """
        Log a command event
        
        Args:
            command_data: Command parsing result
        """
        log_entry = {
            'type': 'command',
            'command': command_data.get('command', 'UNKNOWN'),
            'original_text': command_data.get('original_text', ''),
            'matched_text': command_data.get('matched_text', ''),
            'confidence': command_data.get('confidence', 0.0),
            'match_type': command_data.get('match_type', 'none')
        }
        
        self.process(log_entry)
    
    def log_error(self, error_message: str, context: Optional[Dict[str, Any]] = None):
        """
        Log an error event
        
        Args:
            error_message: Error message
            context: Optional context information
        """
        log_entry = {
            'type': 'error',
            'message': error_message
        }
        
        if context:
            log_entry['context'] = context
        
        self.process(log_entry)
    
    def log_system_event(self, event_type: str, data: Dict[str, Any]):
        """
        Log a system event
        
        Args:
            event_type: Type of system event
            data: Event data
        """
        log_entry = {
            'type': 'system_event',
            'event': event_type,
            'data': data
        }
        
        self.process(log_entry)
    
    def shutdown(self):
        """Write session end log and cleanup"""
        if self.enabled and self.initialized:
            self._write_log({
                'type': 'session_end',
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id
            })
        
        self.logger.info("Logging agent shutdown")
    
    def get_session_log_path(self) -> Optional[str]:
        """
        Get path to current session log file
        
        Returns:
            Path to log file or None
        """
        return self.log_file if self.initialized else None
