# System Architecture

## Overview

The Voice Control System uses a multi-agent architecture where each agent is responsible for a specific task in the speech recognition pipeline. This modular design ensures:

- **Separation of concerns**: Each agent has a single, well-defined responsibility
- **Testability**: Agents can be tested independently
- **Extensibility**: New agents can be added without modifying existing ones
- **Maintainability**: Clear boundaries make the codebase easier to understand

## Agent Architecture

### Base Agent

All agents inherit from `BaseAgent`, which defines the common interface:

```python
class BaseAgent(ABC):
    def initialize(self) -> bool:
        """Initialize agent resources"""
    
    def process(self, data: Any) -> Any:
        """Process input and return result"""
    
    def shutdown(self):
        """Clean up resources"""
    
    def get_status(self) -> Dict[str, Any]:
        """Return current agent status"""
```

### Agent Lifecycle

1. **Initialization**: Agent loads resources (models, config, etc.)
2. **Processing**: Agent processes data through its pipeline
3. **Shutdown**: Agent releases resources and performs cleanup

## Individual Agents

### 1. Input Agent

**Responsibility**: Audio capture from microphone

**Key Features**:
- Configurable sample rate, channels, duration
- Silence detection
- Device selection support

**Input**: None (or duration override)
**Output**: NumPy array of audio samples

### 2. Recognition Agent

**Responsibility**: Convert audio to text using OpenAI Whisper

**Key Features**:
- Offline operation (models cached locally)
- Multiple model sizes (tiny to large)
- Language detection and specification
- CPU and GPU support

**Input**: Audio data (NumPy array)
**Output**: Transcription with text, language, confidence

### 3. Command Parser Agent

**Responsibility**: Map transcribed text to actionable commands

**Key Features**:
- Exact text matching
- Fuzzy matching with configurable threshold
- Command aliases
- Dynamic command addition
- Confidence scoring

**Input**: Transcription dictionary
**Output**: Command with metadata

### 4. Speaker ID Agent

**Responsibility**: Identify who is speaking

**Key Features**:
- Speaker enrollment
- Voice feature extraction
- Speaker matching with confidence
- Can be disabled for simpler use cases

**Input**: Audio data (NumPy array)
**Output**: Speaker ID with confidence

### 5. Logging Agent

**Responsibility**: Record all system activities

**Key Features**:
- JSON Lines format for easy parsing
- Configurable log types
- Session tracking
- Timestamped entries
- Audio logging (optional)

**Input**: Log data dictionary
**Output**: Boolean success indicator

## Data Flow

```
1. User speaks → Microphone
                     ↓
2. Input Agent → Captures audio → NumPy array
                                      ↓
3. Speaker ID Agent → Identifies speaker (optional)
                     ↓
4. Recognition Agent → Transcribes → Text + metadata
                                         ↓
5. Command Parser Agent → Matches command → Action
                                                ↓
6. Logging Agent → Records everything → Log file
```

## Orchestrator Pattern

The `VoiceControlOrchestrator` coordinates all agents:

```python
class VoiceControlOrchestrator:
    def __init__(self):
        self.agents = {}
    
    def initialize_agents(self):
        """Create and initialize all agents"""
    
    def process_voice_command(self):
        """Run the complete pipeline"""
    
    def shutdown(self):
        """Cleanup all agents"""
```

### Pipeline Execution

```python
def process_voice_command(self):
    audio = self.agents['input'].process()
    speaker = self.agents['speaker'].process(audio)
    transcript = self.agents['recognition'].process(audio)
    command = self.agents['parser'].process(transcript)
    self.agents['logging'].log_command(command)
    return command
```

## Configuration Management

### YAML-based Configuration

Two main configuration files:

1. **settings.yaml**: System-wide settings
   - Audio parameters
   - Model selection
   - Agent configurations

2. **commands.yaml**: Command definitions
   - Command mappings
   - Aliases
   - Easy to extend

### Configuration Loading

```python
# Load main settings
with open('config/settings.yaml') as f:
    config = yaml.safe_load(f)

# Pass relevant sections to agents
input_agent = InputAgent(config['audio'])
recognition_agent = RecognitionAgent(config['whisper'])
```

## Error Handling

### Agent-level Error Handling

Each agent handles its own errors:

```python
def process(self, data):
    try:
        result = self._do_work(data)
        return result
    except Exception as e:
        self.logger.error(f"Error: {e}")
        return None
```

### Orchestrator-level Error Handling

The orchestrator provides fallback behavior:

```python
def process_voice_command(self):
    try:
        # Run pipeline
        ...
    except Exception as e:
        self.logger.error(f"Pipeline error: {e}")
        self.agents['logging'].log_error(str(e))
        return None
```

## Extensibility

### Adding a New Agent

1. Create agent class extending `BaseAgent`:

```python
class NewAgent(BaseAgent):
    def initialize(self) -> bool:
        # Setup code
        return True
    
    def process(self, data):
        # Processing code
        return result
    
    def shutdown(self):
        # Cleanup code
        pass
```

2. Register in orchestrator:

```python
self.agents['new'] = NewAgent(config)
self.agents['new'].initialize()
```

3. Add to pipeline:

```python
new_result = self.agents['new'].process(data)
```

### Adding New Commands

Simply edit `config/commands.yaml`:

```yaml
commands:
  "new command phrase": "NEW_ACTION"
```

No code changes required!

## Offline Operation

### Model Caching

- Whisper models downloaded once to `~/.cache/whisper/`
- Models persist between runs
- No internet required after initial download

### Dependencies

All dependencies are standard Python packages that can be bundled:

- No external API calls
- No cloud services
- Fully self-contained

## Windows Packaging

### PyInstaller Integration

The `voice_control.spec` file defines the packaging:

- Bundles Python interpreter
- Includes all dependencies
- Embeds configuration files
- Creates standalone executable

### Build Process

```
Source Code → PyInstaller → Executable Bundle
                  ↓
           Collects:
           - Python runtime
           - Libraries (torch, whisper, etc.)
           - Config files
           - Models (on first run)
```

## Performance Considerations

### Model Selection

| Model | Speed    | Accuracy | Use Case              |
|-------|----------|----------|-----------------------|
| tiny  | Fastest  | Good     | Real-time, low power  |
| base  | Fast     | Better   | Balanced (default)    |
| small | Medium   | Great    | High accuracy needed  |
| medium| Slow     | Excellent| Maximum accuracy      |

### Memory Usage

- Input Agent: ~10 MB
- Recognition Agent: 500 MB - 3 GB (model dependent)
- Other Agents: < 50 MB
- Total: ~1-4 GB depending on model

### Optimization Strategies

1. **Use smaller models** for real-time applications
2. **Adjust chunk duration** to reduce processing time
3. **Enable GPU** if available for 3-5x speedup
4. **Pre-load models** at startup to avoid delays

## Security Considerations

### Audio Privacy

- Audio processed locally only
- No data sent to external services
- Optional audio logging (disabled by default)

### Command Validation

- All commands parsed against whitelist
- Unknown commands rejected
- No arbitrary code execution

### Speaker Identification

- Optional feature
- Simple feature-based matching
- No biometric data stored long-term

## Testing Strategy

### Unit Tests

Each agent can be tested independently:

```python
def test_agent():
    agent = SomeAgent(config)
    assert agent.initialize()
    result = agent.process(test_data)
    assert result is not None
    agent.shutdown()
```

### Integration Tests

Test agent interactions:

```python
def test_pipeline():
    audio = input_agent.process()
    transcript = recognition_agent.process(audio)
    command = parser_agent.process(transcript)
    assert command['command'] != 'UNKNOWN'
```

### End-to-End Tests

Test complete system with sample audio files.

## Future Enhancements

Potential additions to the architecture:

1. **Feedback Agent**: Text-to-speech responses
2. **Context Agent**: Maintain conversation context
3. **Learning Agent**: Adapt to user's speech patterns
4. **Network Agent**: Optional remote logging/monitoring
5. **GUI Agent**: Visual interface for configuration

Each would follow the same agent pattern for consistency.
