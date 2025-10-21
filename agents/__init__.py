"""
AI Agent Architecture for Voice Control System
Multi-agent modules for modular speech recognition system
"""

from .base_agent import BaseAgent

# Import agents individually to avoid loading unnecessary dependencies
# This allows using some agents without installing all dependencies
__all__ = [
    'BaseAgent',
    'InputAgent',
    'RecognitionAgent',
    'CommandParserAgent',
    'SpeakerIDAgent',
    'LoggingAgent'
]

def __getattr__(name):
    """Lazy import of agents to avoid loading all dependencies"""
    if name == 'InputAgent':
        from .input_agent import InputAgent
        return InputAgent
    elif name == 'RecognitionAgent':
        from .recognition_agent import RecognitionAgent
        return RecognitionAgent
    elif name == 'CommandParserAgent':
        from .command_parser_agent import CommandParserAgent
        return CommandParserAgent
    elif name == 'SpeakerIDAgent':
        from .speaker_id_agent import SpeakerIDAgent
        return SpeakerIDAgent
    elif name == 'LoggingAgent':
        from .logging_agent import LoggingAgent
        return LoggingAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
