# Voice Control System for Robot

Windows-based offline speech recognition system using AI Agent architecture and OpenAI Whisper for voice-to-text conversion.

## Features

- **Offline Operation**: Runs completely offline using local Whisper models
- **Multi-Agent Architecture**: Modular design with specialized agents:
  - Input Agent: Audio capture
  - Recognition Agent: Speech-to-text using OpenAI Whisper
  - Command Parser Agent: Intelligent command matching
  - Speaker ID Agent: Speaker identification
  - Logging Agent: Comprehensive file logging
- **Extendable Commands**: Easy-to-configure command system via YAML
- **Windows Compatible**: Built specifically for Windows 10+
- **Automated Build**: GitHub Actions workflow to build Windows .exe

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│          Voice Control Orchestrator                 │
└─────────────────────────────────────────────────────┘
           │
           ├─► Input Agent (Audio Capture)
           │        │
           │        ▼
           ├─► Recognition Agent (Whisper STT)
           │        │
           │        ▼
           ├─► Command Parser Agent (Command Matching)
           │        │
           │        ▼
           ├─► Speaker ID Agent (Speaker Identification)
           │        │
           │        ▼
           └─► Logging Agent (File Logging)
```

## Installation

### From Source (Development)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YounGuru03/voice-control-for-a-robot-system-.git
   cd voice-control-for-a-robot-system-
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the system**:
   ```bash
   python main.py
   ```

### From Pre-built Executable (Windows)

1. Download the latest release from the [Releases](../../releases) page
2. Extract `VoiceControl-Windows.zip`
3. Run `VoiceControl.exe`

## Usage

### Interactive Mode (Default)

```bash
python main.py
```

Continuously listens for voice commands. Press Enter to start recording.

### Single Command Mode

```bash
python main.py --single
```

Processes one command and exits.

### Help

```bash
python main.py --help
```

## Configuration

### Audio Settings (`config/settings.yaml`)

```yaml
audio:
  sample_rate: 16000      # Sample rate for audio capture
  channels: 1             # Mono audio
  chunk_duration: 5       # Recording duration in seconds
  silence_threshold: 0.01 # Silence detection threshold
```

### Whisper Model Settings

```yaml
whisper:
  model_size: "base"  # Options: tiny, base, small, medium, large
  device: "cpu"       # Use "cuda" for GPU acceleration
  language: "en"      # Language code or null for auto-detection
```

### Command Configuration (`config/commands.yaml`)

Add or modify commands:

```yaml
commands:
  "move forward": "MOVE_FORWARD"
  "stop": "STOP"
  "turn left": "TURN_LEFT"
  # Add your custom commands here
```

## Building Windows Executable

### Locally

```bash
pyinstaller voice_control.spec
```

The executable will be in `dist/VoiceControl/VoiceControl.exe`

### GitHub Actions

The system automatically builds a Windows executable when you:
- Push to `main` or `develop` branch
- Create a pull request
- Manually trigger the workflow

The built executable is available as an artifact in the Actions tab.

## Project Structure

```
voice-control-for-a-robot-system-/
├── agents/                  # AI Agent modules
│   ├── __init__.py
│   ├── base_agent.py       # Base agent class
│   ├── input_agent.py      # Audio input
│   ├── recognition_agent.py # Whisper STT
│   ├── command_parser_agent.py # Command parsing
│   ├── speaker_id_agent.py # Speaker identification
│   └── logging_agent.py    # File logging
├── config/                  # Configuration files
│   ├── settings.yaml       # System settings
│   └── commands.yaml       # Command definitions
├── logs/                    # Log files (auto-generated)
├── .github/workflows/       # CI/CD workflows
│   └── build-windows-exe.yml
├── main.py                  # Main orchestrator
├── requirements.txt         # Python dependencies
├── voice_control.spec       # PyInstaller spec
└── README.md               # This file
```

## Log Files

Logs are stored in `logs/` directory with the format `session_YYYYMMDD_HHMMSS.jsonl`:

```json
{"type": "session_start", "timestamp": "2024-01-01T10:00:00"}
{"type": "transcription", "text": "move forward", "language": "en"}
{"type": "command", "command": "MOVE_FORWARD", "confidence": 1.0}
```

## Requirements

### Software
- Python 3.8+ (for development)
- Windows 10 or later (for executable)
- Microphone

### Hardware
- CPU: Modern multi-core processor
- RAM: 4GB minimum, 8GB recommended
- Storage: 2GB for models and application

## Troubleshooting

### No audio detected
- Check microphone permissions in Windows settings
- Verify microphone is selected as default input device
- Adjust `silence_threshold` in `config/settings.yaml`

### Slow transcription
- Use a smaller Whisper model (e.g., "tiny" or "base")
- Reduce `chunk_duration` for shorter audio clips

### Command not recognized
- Check command definitions in `config/commands.yaml`
- Enable fuzzy matching: `fuzzy_matching: true`
- Lower confidence threshold: `confidence_threshold: 0.5`

## Extending the System

### Adding New Commands

Edit `config/commands.yaml`:

```yaml
commands:
  "your new command": "YOUR_ACTION"
```

### Adding Command Aliases

```yaml
aliases:
  "alternative phrase": "your new command"
```

### Custom Agent Development

Create a new agent by extending `BaseAgent`:

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def initialize(self) -> bool:
        # Your initialization code
        pass
    
    def process(self, data):
        # Your processing logic
        pass
    
    def shutdown(self):
        # Cleanup code
        pass
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## GitHub Codespaces Support

This project is designed to work in GitHub Codespaces. The system will work with simulated audio input in environments without microphone access.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [PyInstaller](https://www.pyinstaller.org/) for executable packaging