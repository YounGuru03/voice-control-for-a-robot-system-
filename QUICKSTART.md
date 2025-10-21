# Quick Start Guide

Get started with the Voice Control System in under 5 minutes!

## Prerequisites

- **Windows 10 or later** (for full system)
- **Python 3.8+** (for development/source)
- **Microphone** (for actual voice control)

## Option 1: Use Pre-built Executable (Easiest)

1. Download the latest release from [Releases](../../releases)
2. Extract `VoiceControl-Windows.zip`
3. Double-click `VoiceControl.exe`
4. Press Enter and speak a command!

## Option 2: Run from Source (Development)

### Windows

```cmd
# Clone or download the repository
git clone https://github.com/YounGuru03/voice-control-for-a-robot-system-.git
cd voice-control-for-a-robot-system-

# Run the installation script
install.bat

# Start the system
python main.py
```

### Linux/Mac

```bash
# Clone or download the repository
git clone https://github.com/YounGuru03/voice-control-for-a-robot-system-.git
cd voice-control-for-a-robot-system-

# Run the installation script
chmod +x install.sh
./install.sh

# Start the system
python main.py
```

## First Time Use

1. **Wait for initialization** (30-60 seconds on first run)
   - Whisper model will be downloaded (~150MB)
   - All agents will initialize

2. **Test your microphone**
   - Ensure your microphone is connected
   - Set as default input device in system settings
   - Grant microphone permissions if prompted

3. **Speak a command**
   - Press Enter when prompted
   - Speak clearly: "move forward"
   - Wait for recognition (2-5 seconds)

## Try These Commands

Speak these phrases clearly:

- "move forward"
- "turn left"
- "turn right"
- "stop"
- "go to kitchen"
- "status"

## Testing Without Microphone

If you're in GitHub Codespaces or don't have a microphone:

```bash
# Run demo mode with text input
python demo_mode.py

# Then type commands like:
# move forward
# turn left
# stop
```

## Troubleshooting

### "No module named 'numpy'"
**Solution**: Run the installation script or `pip install -r requirements.txt`

### "Failed to initialize input agent"
**Solution**: 
1. Check microphone is connected
2. Grant microphone permissions
3. Try demo mode instead: `python demo_mode.py`

### "Audio level too low"
**Solution**:
1. Increase microphone volume
2. Speak louder or closer to mic
3. Adjust `silence_threshold` in `config/settings.yaml`

### Slow transcription
**Solution**: Use smaller Whisper model in `config/settings.yaml`:
```yaml
whisper:
  model_size: "tiny"  # Faster, less accurate
```

## Customization

### Add Your Own Commands

Edit `config/commands.yaml`:

```yaml
commands:
  "do something": "MY_CUSTOM_ACTION"
```

Restart the application and speak "do something"!

### Change Recording Duration

Edit `config/settings.yaml`:

```yaml
audio:
  chunk_duration: 3  # Record for 3 seconds instead of 5
```

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed usage instructions
- See [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to add features
- View [example_integration.py](example_integration.py) for robot integration

## Help

- **Issues?** Open an issue on GitHub
- **Questions?** Check existing issues first
- **Ideas?** We welcome contributions!

## Summary

```bash
# Quick commands cheat sheet:
python main.py              # Interactive mode
python main.py --single     # Single command mode
python main.py --help       # Show help
python demo_mode.py         # Demo without microphone
python test_system.py       # Run tests
```

That's it! You're ready to control robots with your voice! 🎤🤖
