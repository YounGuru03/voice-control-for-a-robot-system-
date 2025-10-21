"""
System Test Script
Tests individual agents without requiring audio hardware
"""

import sys
import numpy as np
from agents import (
    CommandParserAgent,
    LoggingAgent,
    RecognitionAgent
)


def test_command_parser():
    """Test command parser agent"""
    print("\n" + "="*60)
    print("Testing Command Parser Agent")
    print("="*60)
    
    config = {
        'commands_file': 'config/commands.yaml',
        'fuzzy_matching': True,
        'confidence_threshold': 0.6
    }
    
    agent = CommandParserAgent(config)
    
    if not agent.initialize():
        print("✗ Failed to initialize command parser")
        return False
    
    print("✓ Command parser initialized")
    
    # Test exact match
    test_cases = [
        {"text": "move forward"},
        {"text": "stop"},
        {"text": "turn left"},
        {"text": "move forwrd"},  # Typo - fuzzy match
        {"text": "invalid command"}
    ]
    
    for test in test_cases:
        result = agent.process(test)
        if result:
            print(f"  Input: '{test['text']}'")
            print(f"    -> Command: {result['command']}")
            print(f"    -> Confidence: {result['confidence']:.2f}")
            print(f"    -> Match type: {result['match_type']}")
    
    agent.shutdown()
    print("\n✓ Command parser test completed")
    return True


def test_logging_agent():
    """Test logging agent"""
    print("\n" + "="*60)
    print("Testing Logging Agent")
    print("="*60)
    
    config = {
        'enabled': True,
        'log_dir': 'logs',
        'log_transcripts': True,
        'log_commands': True
    }
    
    agent = LoggingAgent(config)
    
    if not agent.initialize():
        print("✗ Failed to initialize logging agent")
        return False
    
    print("✓ Logging agent initialized")
    print(f"  Log file: {agent.get_session_log_path()}")
    
    # Test logging
    agent.log_transcription({"text": "test command", "language": "en"})
    agent.log_command({
        "command": "TEST",
        "original_text": "test command",
        "confidence": 1.0
    })
    
    print("✓ Test logs written")
    
    agent.shutdown()
    print("\n✓ Logging agent test completed")
    return True


def test_configuration():
    """Test configuration files"""
    print("\n" + "="*60)
    print("Testing Configuration Files")
    print("="*60)
    
    import yaml
    import os
    
    # Test settings.yaml
    settings_path = 'config/settings.yaml'
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = yaml.safe_load(f)
        print(f"✓ Settings loaded: {len(settings)} sections")
    else:
        print(f"✗ Settings file not found: {settings_path}")
        return False
    
    # Test commands.yaml
    commands_path = 'config/commands.yaml'
    if os.path.exists(commands_path):
        with open(commands_path, 'r') as f:
            commands = yaml.safe_load(f)
        num_commands = len(commands.get('commands', {}))
        num_aliases = len(commands.get('aliases', {}))
        print(f"✓ Commands loaded: {num_commands} commands, {num_aliases} aliases")
    else:
        print(f"✗ Commands file not found: {commands_path}")
        return False
    
    print("\n✓ Configuration test completed")
    return True


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Voice Control System - Test Suite")
    print("="*60)
    
    results = []
    
    # Test configuration
    results.append(("Configuration", test_configuration()))
    
    # Test command parser
    results.append(("Command Parser", test_command_parser()))
    
    # Test logging
    results.append(("Logging Agent", test_logging_agent()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
