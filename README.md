# AI False Memory Demonstration

This project explores how AI chat applications handle memory through two different implementations: a traditional chat with persistent memory and an experimental chat where memories can be manipulated in real-time.

## Overview

- `memory-chat`: A traditional chat application with persistent memory storage
- `false-memory-chat`: An experimental chat where memory can be altered during conversations

## Quick Start

### GitHub Codespaces

This project is optimized for GitHub Codespaces, providing a pre-configured environment with all necessary dependencies.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)]([https://github.com](https://codespaces.new/mor10/false-memory?quickstart=1))

### Manual installation

1. Clone the repository

2. Install Python dependencies
   ```sh
   pip install
   ```

## API Integration

This project integrates with [GitHub Models](https://github.com/marketplace/models), making it immediately usable for GitHub users:
- No API key required
- Authentication handled through GitHub
- Automatic endpoint configuration

## False Memory Chat

The `false-memory-chat` demonstrates how AI memory can be manipulated in real-time, allowing for exploration of how context affects AI responses.

### Running the False Memory Chat

```sh
python false_memory_chat.py
```

### Real-time Memory Manipulation

1. Start the chat application
2. Open `chat_memory.json` in your preferred editor
3. Modify the conversation history:
   ```json
   [
     {"role": "user", "content": "What's your favorite color?"},
     {"role": "assistant", "content": "I love blue!"},
     // Add or modify messages while chat is running
   ]
   ```
4. Changes take effect in the next interaction

### Available Commands
- `history`: Display current chat history
- `count`: Show number of messages in memory
- `exit`: Close the application

## Traditional Memory Chat

The `memory-chat` demonstrates conventional chat memory implementation where conversation history is maintained internally during the session.

### Running the Memory Chat

```sh
python memory_chat.py
```

## Technical Details

### API Configuration
```python
base_url = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
```

## Contributing

Contributions are welcome! Feel free to:
- Submit bug reports
- Propose new features
- Create pull requests

## License

This project is open source and available under the GNU GPL 3.0 License.
