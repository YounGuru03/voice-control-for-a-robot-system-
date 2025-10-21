"""
AI Agent Architecture for Voice Control System
Multi-agent modules for modular speech recognition system
"""

from .base_agent import BaseAgent
from .input_agent import InputAgent
from .recognition_agent import RecognitionAgent
from .command_parser_agent import CommandParserAgent
from .speaker_id_agent import SpeakerIDAgent
from .logging_agent import LoggingAgent

__all__ = [
    'BaseAgent',
    'InputAgent',
    'RecognitionAgent',
    'CommandParserAgent',
    'SpeakerIDAgent',
    'LoggingAgent'
]
