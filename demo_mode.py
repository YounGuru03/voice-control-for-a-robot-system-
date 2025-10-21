"""
Demo Mode - Run voice control system without audio hardware
Perfect for testing in GitHub Codespaces or environments without microphone
"""

import sys
import yaml

# Import only the agents we need to avoid dependency issues in demo mode
sys.path.insert(0, '.')
from agents.command_parser_agent import CommandParserAgent
from agents.logging_agent import LoggingAgent


def demo_command_recognition():
    """Demonstrate command recognition with text input"""
    print("=" * 60)
    print("Voice Control System - Demo Mode")
    print("=" * 60)
    print("\nRunning without audio hardware - text input simulation\n")
    
    # Load configuration
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize agents
    print("Initializing agents...")
    
    # Command parser
    parser_config = config.get('commands', {})
    parser_config['commands_file'] = 'config/commands.yaml'
    parser = CommandParserAgent(parser_config)
    
    if not parser.initialize():
        print("✗ Failed to initialize command parser")
        return 1
    
    # Logging agent
    logging_config = config.get('logging', {})
    logger = LoggingAgent(logging_config)
    
    if not logger.initialize():
        print("✗ Failed to initialize logging agent")
        return 1
    
    print("✓ Agents initialized\n")
    
    # Show available commands
    print("Available commands:")
    commands = parser.get_available_commands()
    for i, cmd in enumerate(sorted(commands)[:10], 1):
        print(f"  {i}. {cmd}")
    if len(commands) > 10:
        print(f"  ... and {len(commands) - 10} more")
    print()
    
    # Demo loop
    print("Enter text commands (or 'quit' to exit):")
    print("-" * 60)
    
    try:
        while True:
            user_input = input("\nCommand> ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Exiting demo mode...")
                break
            
            # Simulate transcription
            transcription = {
                'text': user_input,
                'language': 'en'
            }
            
            # Parse command
            result = parser.process(transcription)
            
            if result:
                command = result['command']
                confidence = result['confidence']
                match_type = result['match_type']
                
                # Log the command
                logger.log_command(result)
                
                # Display result
                if command != 'UNKNOWN':
                    print(f"  ✓ Recognized: {command}")
                    print(f"    Confidence: {confidence:.2%}")
                    print(f"    Match: {match_type}")
                else:
                    print(f"  ✗ Unknown command")
                    print(f"    Try: {commands[0]}")
            else:
                print("  ✗ Failed to parse command")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        # Cleanup
        parser.shutdown()
        logger.shutdown()
        
        log_file = logger.get_session_log_path()
        if log_file:
            print(f"\n✓ Session log: {log_file}")
    
    print("\n✓ Demo complete")
    return 0


def demo_fuzzy_matching():
    """Demonstrate fuzzy command matching"""
    print("\n" + "=" * 60)
    print("Fuzzy Matching Demo")
    print("=" * 60)
    print()
    
    # Initialize parser with fuzzy matching
    config = {
        'commands_file': 'config/commands.yaml',
        'fuzzy_matching': True,
        'confidence_threshold': 0.6
    }
    
    parser = CommandParserAgent(config)
    parser.initialize()
    
    # Test cases with typos and variations
    test_cases = [
        "move forward",      # Exact match
        "move forwrd",       # Typo
        "mov forward",       # Typo
        "move forword",      # Typo
        "go forward",        # Alias
        "turn left",         # Exact
        "turn lft",          # Typo
        "invalid command",   # No match
    ]
    
    print("Testing fuzzy matching with typos and variations:\n")
    
    for test_input in test_cases:
        transcription = {'text': test_input}
        result = parser.process(transcription)
        
        if result:
            command = result['command']
            confidence = result['confidence']
            match_type = result['match_type']
            
            status = "✓" if command != 'UNKNOWN' else "✗"
            print(f"{status} '{test_input}'")
            print(f"   → {command} ({confidence:.2%}, {match_type})")
        print()
    
    parser.shutdown()


def main():
    """Run demo mode"""
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--fuzzy':
        return demo_fuzzy_matching()
    else:
        return demo_command_recognition()


if __name__ == '__main__':
    sys.exit(main())
