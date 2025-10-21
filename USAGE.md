# Usage Guide

## Quick Start

### 1. First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# This will automatically download the Whisper model on first run
python main.py
```

### 2. Running the System

**Interactive Mode (Recommended for testing)**:
```bash
python main.py
```

The system will:
1. Initialize all agents (may take 30-60 seconds first time)
2. Wait for you to press Enter
3. Record audio for 5 seconds
4. Process the audio through the pipeline
5. Display the recognized command

**Single Command Mode (For scripting)**:
```bash
python main.py --single
```

Processes one command automatically and exits.

## Understanding the Output

### Successful Command

```
--- Starting voice command processing ---
Recording audio for 5 seconds...
Audio captured: (80000,), level: 0.0234
Transcribing audio...
Transcription: 'move forward'
Speaker: speaker_1
Command: MOVE_FORWARD
--- Voice command processing complete ---

✓ Command executed: MOVE_FORWARD
```

### Unknown Command

```
--- Starting voice command processing ---
Recording audio for 5 seconds...
Audio captured: (80000,), level: 0.0189
Transcribing audio...
Transcription: 'do a backflip'
No command match for: 'do a backflip'
Command: UNKNOWN
--- Voice command processing complete ---

✗ No valid command recognized
```

## Command Examples

Try speaking these commands clearly into your microphone:

### Movement Commands
- "move forward"
- "move backward"
- "turn left"
- "turn right"
- "stop"
- "halt"

### Navigation Commands
- "go to kitchen"
- "go to bedroom"
- "return home"

### Action Commands
- "pick up"
- "put down"
- "open gripper"
- "close gripper"

### System Commands
- "status"
- "battery level"

## Tips for Best Recognition

1. **Speak clearly** and at a normal pace
2. **Reduce background noise** as much as possible
3. **Position microphone** 6-12 inches from your mouth
4. **Wait for the recording** to start before speaking
5. **Speak during** the 5-second recording window

## Customizing Recording Duration

Edit `config/settings.yaml`:

```yaml
audio:
  chunk_duration: 5  # Change to 3 for shorter, 10 for longer
```

## Adding Your Own Commands

1. Open `config/commands.yaml`
2. Add your command under the `commands` section:

```yaml
commands:
  "your custom phrase": "YOUR_ACTION_NAME"
```

3. Restart the application
4. Test your new command

## Viewing Logs

Logs are saved in `logs/session_YYYYMMDD_HHMMSS.jsonl`

View with any text editor or use:

```bash
# View the latest log
cat logs/session_*.jsonl | tail -20

# Pretty print JSON logs
python -m json.tool logs/session_*.jsonl
```

## Troubleshooting

### "Failed to initialize input agent"

**Problem**: No microphone detected or access denied

**Solution**:
1. Check Windows Sound settings
2. Ensure microphone is plugged in and enabled
3. Grant microphone permissions to Python/Terminal
4. Try selecting a specific device in `config/settings.yaml`:
   ```yaml
   audio:
     device: 0  # Try 0, 1, 2, etc.
   ```

### "Audio level too low, possibly silence"

**Problem**: Microphone volume too low or incorrect device

**Solution**:
1. Increase microphone volume in Windows
2. Speak louder
3. Move closer to microphone
4. Adjust threshold:
   ```yaml
   audio:
     silence_threshold: 0.005  # Lower = more sensitive
   ```

### Slow transcription

**Problem**: Whisper model too large for your hardware

**Solution**: Use a smaller model in `config/settings.yaml`:
```yaml
whisper:
  model_size: "tiny"  # Fastest, less accurate
  # or "base" - Good balance (default)
  # or "small" - Better accuracy, slower
```

### Commands not recognized

**Problem**: Exact text doesn't match

**Solution**: Enable fuzzy matching in `config/settings.yaml`:
```yaml
commands:
  fuzzy_matching: true
  confidence_threshold: 0.5  # Lower = more lenient
```

## Advanced Usage

### Using Different Languages

Edit `config/settings.yaml`:

```yaml
whisper:
  language: "es"  # Spanish
  # Other options: "fr", "de", "it", "ja", "ko", etc.
  # Use null for automatic detection
```

### Speaker Identification

Enable speaker ID to track who gave each command:

```yaml
speaker_id:
  enabled: true
  threshold: 0.75
```

### Logging Control

```yaml
logging:
  enabled: true
  log_transcripts: true  # Log all transcriptions
  log_commands: true     # Log all commands
  log_audio: false       # Save audio files (requires much space)
```

## Integration with Robot Systems

The system outputs structured command data that can be integrated with robot control systems:

```python
result = orchestrator.process_voice_command()
if result and result['success']:
    command = result['command']['command']
    
    # Your robot control code here
    if command == 'MOVE_FORWARD':
        robot.move_forward()
    elif command == 'TURN_LEFT':
        robot.turn_left()
    # ... etc
```

## Performance Expectations

| Model | Typical Speed | Accuracy | RAM Usage |
|-------|---------------|----------|-----------|
| tiny  | 1-2 sec       | Good     | ~1 GB     |
| base  | 2-4 sec       | Better   | ~1.5 GB   |
| small | 4-8 sec       | Great    | ~2 GB     |
| medium| 8-15 sec      | Excellent| ~4 GB     |

*Speeds based on modern CPU without GPU acceleration*

## Building Windows Executable

```bash
# Build executable
pyinstaller voice_control.spec

# Test it
cd dist/VoiceControl
VoiceControl.exe --help
```

The executable will be in `dist/VoiceControl/` and can be distributed to other Windows machines without requiring Python installation.
