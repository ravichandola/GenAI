# GenAI - AI Development Project

This repository contains a collection of AI-powered applications and utilities, focusing on interactions with OpenAI's GPT models and other AI-related functionalities.

## Project Structure

```
.
├── hello-AI/
│   ├── chat-cot-03.py      # Main chat implementation with Chain of Thought
│   ├── chat.py             # Basic chat functionality
│   └── prompts.py          # System prompts and templates
├── Introduction/
│   └── tokenizer.py        # Tokenization utilities
├── Pipfile                 # Dependencies management
├── Pipfile.lock
└── .gitignore             # Git ignore configurations
```

## Setup and Installation

### Prerequisites

- Python 3.13
- Pipenv (for dependency management)

### Installation Steps

1. Clone the repository
2. Install dependencies using Pipenv:
   ```bash
   pipenv install
   ```
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo  # or your preferred model
   ```

## Features

### 1. Chat with Chain of Thought (CoT)

Located in `hello-AI/chat-cot-03.py`, this implementation includes:

- Interactive chat interface with GPT models
- Chain of Thought reasoning
- JSON-structured responses
- Error handling for API responses

### 2. Tokenization Utilities

Located in `Introduction/tokenizer.py`, provides tokenization functionality for text processing.

## Dependencies

- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests library

### Development Dependencies

- `pytest` - Testing framework

## Environment Variables

The project uses the following environment variables (to be set in `.env`):

- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - The GPT model to use (defaults to 'gpt-3.5-turbo')

## Security

- The `.env` file is included in `.gitignore` to ensure sensitive information is not committed
- API keys and other sensitive data should never be committed to version control

## Best Practices

1. Always use environment variables for sensitive information
2. Keep your API keys secure and never commit them to version control
3. Use the provided Pipenv environment for consistent dependency management

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes

## Note

This is an active development project. Features and implementations may change as the project evolves.
