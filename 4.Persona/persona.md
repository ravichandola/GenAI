# Persona Chatbot System

## Overview

This is a flexible chatbot system that can work with multiple AI providers (OpenAI and Google Gemini) and can be configured with custom personas through prompt files. The system maintains conversation context and supports interactive chat sessions with customizable behavior.

## System Architecture

### File Structure

```
4.Persona/
├── main.py         # Main application entry point
├── models.py       # Model handling and response generation
├── clients.py      # API client configurations
├── prompts/        # Directory for storing prompt files
│   ├── naruto-prompt.py          # Naruto character persona
│   ├── baburao-prompt.txt        # Baburao character persona
│   ├── chaatu-employee-prompt.txt # Chaatu Employee persona
│   ├── modiji-prompt.txt         # Modi Ji character persona
│   └── hitesh-prompt.txt         # Hitesh character persona
└── persona.md      # System documentation
```

### Components

#### 1. Client Management (`clients.py`)

- Handles API client initialization for different providers
- Supports:
  - OpenAI client with API key authentication
  - Google Gemini with global configuration
- Environment variables required:
  - `OPENAI_API_KEY`: For OpenAI integration
  - `GEMINI_API_KEY`: For Google Gemini integration

#### 2. Model Interface (`models.py`)

- Manages model interactions and response generation
- Key features:
  - Dynamic provider selection (OpenAI/Gemini)
  - Prompt file loading and management
  - Message handling and response formatting
- Environment variables used:
  - `PROVIDER`: Selected AI provider ('openai' or 'gemini')
  - `OPENAI_MODEL`: OpenAI model identifier
  - `GEMINI_MODEL`: Gemini model identifier
  - `PROMPT_FILE`: Path to the prompt file

#### 3. Main Application (`main.py`)

- Implements the interactive chat loop
- Features:
  - System prompt initialization
  - Message history management
  - JSON response parsing
  - Error handling
  - Visual feedback with emojis (🤖, 🧠)

## Flow Diagram

```
User Input → main.py
    ↓
Load Environment Variables
    ↓
Initialize System Prompt
    ↓
Start Chat Loop
    ↓
Process User Message → models.py
    ↓
Select Provider (OpenAI/Gemini) → clients.py
    ↓
Generate Response
    ↓
Parse & Format Response
    ↓
Display to User
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with:

```
PROVIDER=openai|gemini
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
OPENAI_MODEL=gpt-3.5-turbo
GEMINI_MODEL=gemini-pro
PROMPT_FILE=path_to_prompt_file
```

### Prompt Files

- Store prompt files in the `prompts/` directory
- Supports `.txt` or `.py` format
- Define the system behavior and persona

Available Personas:

1. `naruto-prompt.py` - Naruto character persona
2. `baburao-prompt.txt` - Baburao character persona
3. `chaatu-employee-prompt.txt` - Chaatu Employee persona
4. `modiji-prompt.txt` - Modi Ji character persona
5. `hitesh-prompt.txt` - Hitesh character persona

To use a specific persona, set in your `.env` file:

```
PROMPT_FILE=prompts/[prompt-file-name]
```

## Usage

1. Set up environment variables in `.env`
2. Create a prompt file with the desired persona
3. Run the application:

```bash
python main.py
```

4. Interact with the chatbot (type 'exit' to quit)

## Response Format

The system supports two types of responses:

1. JSON formatted responses with:
   - `step`: "think" or "result"
   - `content`: The actual message
2. Raw text responses (fallback)

## Error Handling

- Environment variable validation
- API client initialization checks
- Response parsing error management
- Graceful exit handling

## Extensibility

The system is designed to be extensible:

- Add new AI providers by extending `clients.py`
- Modify response formatting in `models.py`
- Create custom prompts for different personas

## Dependencies

- `openai`: OpenAI API client
- `google-generativeai`: Google Gemini API
- `python-dotenv`: Environment variable management


