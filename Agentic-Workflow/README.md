# My_Graph - Conversational AI System

A conversational AI system that classifies and routes user queries to appropriate agents (coding or general) using LangGraph.

## Features

- Query classification (coding vs general)
- Routing to specialized agents
- OpenAI integration
- Graph-based workflow

## Quick Start

### Option 1: Automated Setup

```bash
# Run the setup script
python setup.py
```

### Option 2: Manual Setup

1. **Activate virtual environment**:

   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**:

   ```bash
   # Create .env file manually
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Add your OpenAI API key**:
   - Edit the `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## Running the Application

```bash
python main.py
```

The application will prompt you with `>` and wait for your input. You can ask:

- Coding questions (will be routed to coding agent)
- General questions (will be routed to general agent)

## Project Structure

```
My_Graph/
├── main.py              # Entry point
├── graph_builder.py     # Graph workflow definition
├── agents/              # AI agents
│   ├── classifier.py    # Query classification
│   ├── coding_agent.py  # Coding-specific agent
│   ├── general_agent.py # General-purpose agent
│   └── validate_query.py # Query validation
├── models/              # Data models
│   ├── state.py         # State management
│   └── response.py      # Response models
└── utils/               # Utilities
    └── client.py        # OpenAI client setup
```

## Requirements

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

## Dependencies

- `openai` - OpenAI API client
- `langgraph` - Graph workflow framework
- `python-dotenv` - Environment variable management

## Troubleshooting

1. **API Key Error**: Make sure your OpenAI API key is correctly set in `.env`
2. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Virtual Environment**: Activate your virtual environment before running the application
