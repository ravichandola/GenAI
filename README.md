# GenAI - AI Development Project

This repository contains a collection of AI-powered applications and utilities, focusing on interactions with OpenAI's GPT models and other AI-related functionalities.

## Project Structure

```
.
├── 1. Introduction/        # Basic concepts and introductory materials
├── 2. COT/                # Chain of Thought implementations
├── 3. Project/            # Main project implementations
├── 4. Persona/            # Customizable AI Persona Chatbot System
│   ├── main.py           # Main application entry point
│   ├── models.py         # Model handling and response generation
│   ├── clients.py        # API client configurations
│   ├── prompts/          # Directory for storing persona prompts
│   │   ├── naruto-prompt.py
│   │   ├── baburao-prompt.txt
│   │   ├── chaatu-employee-prompt.txt
│   │   ├── modiji-prompt.txt
│   │   └── hitesh-prompt.txt
│   └── persona.md        # System documentation
├── Pipfile                # Dependencies management
├── Pipfile.lock
└── .gitignore            # Git ignore configurations
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
3. Create a `.env` file in the root directory with your API keys:

   ```
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo  # or your preferred model

   # Gemini Configuration
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-pro

   # Provider Selection
   PROVIDER=openai  # or 'gemini'
   ```

## Project Components

### 1. Introduction

The Introduction section covers fundamental concepts and basic implementations, providing a foundation for the more advanced topics.

### 2. Chain of Thought (COT)

This section focuses on implementing Chain of Thought reasoning with GPT models, demonstrating how to:

- Structure prompts for step-by-step reasoning
- Process and parse model responses
- Handle complex problem-solving scenarios

### 3. Project

The main project implementations, featuring:

- Advanced AI interactions
- Practical applications
- Integration examples

### 4. Persona

The Persona section focuses on creating a customizable AI Persona Chatbot System.

**Read this** - [PERSONA](./4.Persona/persona.md)

## Dependencies

Main dependencies are managed through Pipenv and include:

- `openai` - OpenAI API client
- `google-generativeai` - Google Gemini API client
- `python-dotenv` - Environment variable management
- `requests` - HTTP requests library

## Environment Variables

The project uses the following environment variables (to be set in `.env`):

- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - The GPT model to use (defaults to 'gpt-3.5-turbo')
- `GEMINI_API_KEY` - Your Google Gemini API key
- `GEMINI_MODEL` - The Gemini model to use (defaults to 'gemini-pro')
- `PROVIDER` - AI provider to use ('openai' or 'gemini')

## Security

- The `.env` file and `.DS_Store` are included in `.gitignore` to ensure sensitive information is not committed
- API keys and other sensitive data should never be committed to version control

## Best Practices

1. Always use environment variables for sensitive information
2. Keep your API keys secure and never commit them to version control
3. Use the provided Pipenv environment for consistent dependency management
4. Follow the project structure when adding new implementations

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request with a clear description of your changes

## Note

This is an active development project. Features and implementations may change as the project evolves. For more information -
[JIRA BOARD Link](https://ravichandola.atlassian.net/jira/software/projects/GP/boards/3)

## PROJECT LIST

1. [COMPARE MODELS](./3.Compare%20Models/compare-models.md)
2. [PERSONA](./4.Persona/persona.md)
