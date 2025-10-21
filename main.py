"""
Main Orchestrator for Voice Control System
Coordinates all AI agents and manages the overall workflow
"""

import sys
import os
import yaml
import logging
from typing import Dict, Any, Optional

from agents import (
    InputAgent,
    RecognitionAgent,
    CommandParserAgent,
    SpeakerIDAgent,
    LoggingAgent
)


class VoiceControlOrchestrator:
    """Main orchestrator coordinating all agent modules"""
    
    def __init__(self, config_path: str = 'config/settings.yaml'):
        """
        Initialize the orchestrator
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = {}
        self.agents = {}
        self.running = False
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger('VoiceControlOrchestrator')
    
    def _setup_logging(self):
        """Setup system-wide logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def load_config(self) -> bool:
        """
        Load configuration from YAML file
        
        Returns:
            bool: True if successful
        """
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            self.logger.info(f"Configuration loaded from {self.config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False
    
    def initialize_agents(self) -> bool:
        """
        Initialize all agent modules
        
        Returns:
            bool: True if all agents initialized successfully
        """
        try:
            self.logger.info("Initializing agents...")
            
            # Initialize Logging Agent first
            logging_config = self.config.get('logging', {})
            self.agents['logging'] = LoggingAgent(logging_config)
            if not self.agents['logging'].initialize():
                self.logger.error("Failed to initialize logging agent")
                return False
            
            # Initialize Input Agent
            audio_config = self.config.get('audio', {})
            self.agents['input'] = InputAgent(audio_config)
            if not self.agents['input'].initialize():
                self.logger.error("Failed to initialize input agent")
                return False
            
            # Initialize Recognition Agent
            whisper_config = self.config.get('whisper', {})
            self.agents['recognition'] = RecognitionAgent(whisper_config)
            if not self.agents['recognition'].initialize():
                self.logger.error("Failed to initialize recognition agent")
                return False
            
            # Initialize Command Parser Agent
            commands_config = self.config.get('commands', {})
            commands_config['commands_file'] = 'config/commands.yaml'
            self.agents['parser'] = CommandParserAgent(commands_config)
            if not self.agents['parser'].initialize():
                self.logger.error("Failed to initialize command parser agent")
                return False
            
            # Initialize Speaker ID Agent
            speaker_config = self.config.get('speaker_id', {})
            self.agents['speaker'] = SpeakerIDAgent(speaker_config)
            if not self.agents['speaker'].initialize():
                self.logger.warning("Speaker ID agent initialization failed, continuing without it")
            
            self.logger.info("All agents initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing agents: {e}")
            return False
    
    def process_voice_command(self) -> Optional[Dict[str, Any]]:
        """
        Process a single voice command through the agent pipeline
        
        Returns:
            Dictionary containing command result, or None if failed
        """
        try:
            # Step 1: Capture audio input
            self.logger.info("--- Starting voice command processing ---")
            audio_data = self.agents['input'].process()
            
            if audio_data is None:
                self.logger.error("Failed to capture audio")
                self.agents['logging'].log_error("Audio capture failed")
                return None
            
            # Step 2: Speaker identification (if enabled)
            speaker_info = self.agents['speaker'].process(audio_data)
            if speaker_info:
                self.logger.info(f"Speaker: {speaker_info.get('speaker_id', 'unknown')}")
            
            # Step 3: Speech recognition
            transcription = self.agents['recognition'].process(audio_data)
            
            if transcription is None or not transcription.get('text'):
                self.logger.error("Failed to transcribe audio")
                self.agents['logging'].log_error("Transcription failed")
                return None
            
            # Log transcription
            self.agents['logging'].log_transcription(transcription, speaker_info)
            
            # Step 4: Command parsing
            command_result = self.agents['parser'].process(transcription)
            
            if command_result is None:
                self.logger.error("Failed to parse command")
                self.agents['logging'].log_error("Command parsing failed")
                return None
            
            # Log command
            self.agents['logging'].log_command(command_result)
            
            # Combine results
            result = {
                'transcription': transcription,
                'command': command_result,
                'speaker': speaker_info,
                'success': command_result['command'] != 'UNKNOWN'
            }
            
            self.logger.info(f"Command: {command_result['command']}")
            self.logger.info("--- Voice command processing complete ---\n")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
            self.agents['logging'].log_error(str(e))
            return None
    
    def run_interactive(self):
        """
        Run in interactive mode - continuously process voice commands
        """
        self.running = True
        self.logger.info("Starting interactive mode...")
        self.logger.info("Press Ctrl+C to stop\n")
        
        try:
            while self.running:
                input("Press Enter to start recording (or Ctrl+C to quit)...")
                result = self.process_voice_command()
                
                if result and result['success']:
                    command = result['command']['command']
                    print(f"\n✓ Command executed: {command}\n")
                else:
                    print("\n✗ No valid command recognized\n")
                    
        except KeyboardInterrupt:
            self.logger.info("\nStopping...")
            self.running = False
    
    def run_single_command(self):
        """
        Process a single voice command and exit
        """
        self.logger.info("Single command mode - recording will start automatically\n")
        result = self.process_voice_command()
        
        if result and result['success']:
            command = result['command']['command']
            print(f"\n✓ Command: {command}")
            return 0
        else:
            print("\n✗ No valid command recognized")
            return 1
    
    def shutdown(self):
        """Shutdown all agents and cleanup"""
        self.logger.info("Shutting down...")
        
        for agent_name, agent in self.agents.items():
            try:
                agent.shutdown()
                self.logger.info(f"{agent_name} agent shutdown")
            except Exception as e:
                self.logger.error(f"Error shutting down {agent_name} agent: {e}")
        
        self.logger.info("Shutdown complete")
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get status of all agents
        
        Returns:
            Dictionary containing status of all components
        """
        status = {
            'running': self.running,
            'agents': {}
        }
        
        for agent_name, agent in self.agents.items():
            status['agents'][agent_name] = agent.get_status()
        
        return status


def main():
    """Main entry point"""
    print("=" * 60)
    print("Voice Control System for Robot")
    print("Offline Speech Recognition with AI Agent Architecture")
    print("=" * 60)
    print()
    
    # Parse command line arguments
    mode = 'interactive'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--single', '-s']:
            mode = 'single'
        elif sys.argv[1] in ['--help', '-h']:
            print("Usage: python main.py [options]")
            print("\nOptions:")
            print("  --single, -s    Process single command and exit")
            print("  --help, -h      Show this help message")
            print("\nInteractive mode (default): Continuously process commands")
            return 0
    
    # Create orchestrator
    orchestrator = VoiceControlOrchestrator()
    
    try:
        # Load configuration
        if not orchestrator.load_config():
            print("ERROR: Failed to load configuration")
            return 1
        
        # Initialize agents
        if not orchestrator.initialize_agents():
            print("ERROR: Failed to initialize agents")
            return 1
        
        print("\n✓ System initialized successfully\n")
        
        # Run in selected mode
        if mode == 'single':
            exit_code = orchestrator.run_single_command()
        else:
            orchestrator.run_interactive()
            exit_code = 0
        
        return exit_code
        
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        return 1
        
    finally:
        orchestrator.shutdown()


if __name__ == '__main__':
    sys.exit(main())
