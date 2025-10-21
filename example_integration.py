"""
Example Integration Script
Demonstrates how to integrate the voice control system with a robot
"""

import sys
from main import VoiceControlOrchestrator


class RobotController:
    """Mock robot controller for demonstration"""
    
    def __init__(self):
        self.position = [0, 0]
        self.heading = 0
        
    def move_forward(self):
        print("🤖 Robot moving forward...")
        self.position[0] += 1
        
    def move_backward(self):
        print("🤖 Robot moving backward...")
        self.position[0] -= 1
        
    def turn_left(self):
        print("🤖 Robot turning left...")
        self.heading = (self.heading - 90) % 360
        
    def turn_right(self):
        print("🤖 Robot turning right...")
        self.heading = (self.heading + 90) % 360
        
    def stop(self):
        print("🤖 Robot stopped")
        
    def get_status(self):
        print(f"🤖 Position: {self.position}, Heading: {self.heading}°")
        return {
            'position': self.position,
            'heading': self.heading
        }
        
    def get_battery(self):
        print("🤖 Battery: 87%")
        return 87
        
    def shutdown(self):
        print("🤖 Robot shutting down...")


def execute_robot_command(command: str, robot: RobotController):
    """
    Execute robot command based on voice control output
    
    Args:
        command: Command action name
        robot: Robot controller instance
    """
    command_map = {
        'MOVE_FORWARD': robot.move_forward,
        'MOVE_BACKWARD': robot.move_backward,
        'TURN_LEFT': robot.turn_left,
        'TURN_RIGHT': robot.turn_right,
        'STOP': robot.stop,
        'GET_STATUS': robot.get_status,
        'GET_BATTERY': robot.get_battery,
        'SHUTDOWN': robot.shutdown,
    }
    
    if command in command_map:
        command_map[command]()
        return True
    else:
        print(f"⚠ Unknown command: {command}")
        return False


def main():
    """Main integration example"""
    print("=" * 60)
    print("Voice Control System - Robot Integration Example")
    print("=" * 60)
    print()
    
    # Initialize robot controller
    robot = RobotController()
    print("✓ Robot controller initialized\n")
    
    # Initialize voice control system
    orchestrator = VoiceControlOrchestrator()
    
    try:
        # Load configuration
        if not orchestrator.load_config():
            print("ERROR: Failed to load configuration")
            return 1
        
        # Initialize agents
        print("\nInitializing voice control system...")
        print("(This may take 30-60 seconds on first run)\n")
        
        if not orchestrator.initialize_agents():
            print("ERROR: Failed to initialize voice control system")
            return 1
        
        print("\n✓ Voice control system initialized\n")
        print("=" * 60)
        print("System Ready")
        print("=" * 60)
        print("\nSpeak commands to control the robot.")
        print("Press Enter to record, or Ctrl+C to quit.\n")
        
        # Main control loop
        while True:
            input("Press Enter to record command...")
            
            # Process voice command
            result = orchestrator.process_voice_command()
            
            if result and result['success']:
                command = result['command']['command']
                print(f"\n✓ Command recognized: {command}")
                
                # Execute robot command
                success = execute_robot_command(command, robot)
                
                if success:
                    print("✓ Command executed successfully\n")
                else:
                    print("✗ Failed to execute command\n")
                
                # Check if shutdown requested
                if command == 'SHUTDOWN':
                    print("Shutdown requested, exiting...")
                    break
            else:
                print("\n✗ No valid command recognized\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 0
        
    except Exception as e:
        print(f"\nERROR: {e}")
        return 1
        
    finally:
        # Cleanup
        print("\nShutting down...")
        orchestrator.shutdown()
        print("✓ Voice control system shutdown")


if __name__ == '__main__':
    sys.exit(main())
