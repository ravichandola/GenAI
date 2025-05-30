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

#### 1. Client Management (`
