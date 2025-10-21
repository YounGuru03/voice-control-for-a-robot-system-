# Contributing to Voice Control System

Thank you for considering contributing to this project! This document provides guidelines and information for contributors.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Keep discussions professional

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Relevant logs from `logs/` directory

### Suggesting Features

1. Check if the feature has been suggested
2. Create an issue describing:
   - The problem it solves
   - How it would work
   - Example use cases
   - Any implementation ideas

### Contributing Code

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/voice-control-for-a-robot-system-.git
cd voice-control-for-a-robot-system-

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8
```

#### Making Changes

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes**: Follow the coding standards below
3. **Test your changes**: Ensure tests pass
4. **Commit**: Use clear commit messages
5. **Push**: `git push origin feature/your-feature-name`
6. **Create Pull Request**: Describe your changes

#### Coding Standards

**Python Style**:
- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and small

**Example**:
```python
def process_audio(audio_data: np.ndarray, sample_rate: int = 16000) -> Dict[str, Any]:
    """
    Process audio data through the pipeline.
    
    Args:
        audio_data: Audio samples as numpy array
        sample_rate: Sample rate in Hz
        
    Returns:
        Dictionary containing processed results
    """
    # Implementation
    pass
```

**Agent Development**:
- Extend `BaseAgent` for new agents
- Implement all abstract methods
- Add comprehensive error handling
- Include logging for debugging

**Example**:
```python
from agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def initialize(self) -> bool:
        try:
            # Setup code
            self.initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize: {e}")
            return False
    
    def process(self, data):
        if not self.initialized:
            return None
        # Processing logic
        return result
    
    def shutdown(self):
        # Cleanup
        pass
```

#### Testing

**Run Tests**:
```bash
# Basic system test
python test_system.py

# Run pytest if available
pytest tests/
```

**Add Tests** for new features:
```python
def test_new_feature():
    """Test description"""
    # Setup
    agent = NewAgent(config)
    assert agent.initialize()
    
    # Test
    result = agent.process(test_data)
    
    # Verify
    assert result is not None
    assert result['expected_field'] == expected_value
    
    # Cleanup
    agent.shutdown()
```

#### Documentation

- Update README.md if adding user-facing features
- Update ARCHITECTURE.md for architectural changes
- Update USAGE.md for usage changes
- Add docstrings to new code
- Comment complex logic

### Adding New Commands

This is the easiest way to contribute!

1. Edit `config/commands.yaml`:
```yaml
commands:
  "your new command": "YOUR_ACTION"
```

2. Test it:
```bash
python main.py
# Speak: "your new command"
```

3. Create a Pull Request with:
   - Description of the command
   - Example use case
   - Any special considerations

### Improving Documentation

Documentation improvements are always welcome:
- Fix typos or unclear explanations
- Add examples
- Improve tutorials
- Translate documentation

## Project Structure

```
voice-control-for-a-robot-system-/
├── agents/              # Agent modules
│   ├── base_agent.py   # Base class
│   └── *_agent.py      # Specific agents
├── config/              # Configuration files
├── logs/               # Generated logs
├── .github/workflows/  # CI/CD
├── main.py             # Main orchestrator
├── test_system.py      # Tests
└── docs/               # Documentation
```

## Git Commit Messages

Use clear, descriptive commit messages:

**Good**:
- `Add fuzzy matching to command parser`
- `Fix audio capture on Windows 11`
- `Update README with installation instructions`

**Bad**:
- `fix bug`
- `update`
- `wip`

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** if applicable
5. **Request review** from maintainers
6. **Address feedback** promptly

## Development Tips

### Testing Without Microphone

Use simulated audio:
```python
# In your test
import numpy as np
fake_audio = np.random.randn(16000 * 5).astype(np.float32)
result = recognition_agent.process(fake_audio)
```

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Quick Iteration

Use single command mode for faster testing:
```bash
python main.py --single
```

## Areas Needing Contribution

Current priorities:

1. **Testing**: More unit and integration tests
2. **Documentation**: More examples and tutorials
3. **Commands**: Expand default command set
4. **Performance**: Optimization for faster processing
5. **Features**: GUI, additional agents, multi-language support

## Recognition

Contributors will be:
- Listed in AUTHORS.md
- Credited in release notes
- Acknowledged in the README

## Questions?

- Open an issue for questions
- Tag issues with `question` label
- Check existing issues first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

Thank you for contributing to making voice control more accessible!
