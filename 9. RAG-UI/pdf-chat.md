# PDF Chat Application Documentation

## Overview

PDF Chat is an interactive application that allows users to have conversations with their PDF documents through various AI personas. The application combines document processing, vector storage, and natural language processing to create an engaging and informative chat experience.

## Features

- 📄 PDF Document Processing
- 💬 Interactive Chat Interface
- 🎭 Multiple AI Personas
- 🔍 Semantic Search
- 📱 Responsive Design
- 💾 Chat History Management

## Architecture

### Components

1. **Frontend (Streamlit)**

   - User interface for PDF upload
   - Chat interface
   - Persona selection
   - Chat history management

2. **Vector Database (Qdrant)**

   - Document storage
   - Vector embeddings
   - Similarity search

3. **Document Processing**

   - PDF parsing
   - Text chunking
   - Embedding generation

4. **AI Integration**
   - OpenAI GPT-4 for chat responses
   - OpenAI Embeddings for text vectorization

## Setup and Installation

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API Key

### Environment Variables

Create a `.env` file with:

```
OPENAI_API_KEY=your_api_key_here
```

### Installation Steps

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the vector database:
   ```bash
   docker-compose up -d
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

### Uploading a PDF

1. Click the "Upload PDF" button
2. Select a PDF file (max 10MB)
3. Click "Process PDF" to begin ingestion

### Selecting a Persona

Choose from available personas:

- Hitesh Choudhary (Tech Educator)
- Narendra Modi (Visionary Leader)
- Naruto Uzumaki (Enthusiastic Ninja)
- Baburao (Grumpy but Wise)
- Chaatu Employee (Overly Flattering)
- Bot (Precise AI Assistant)

### Chatting with the Document

1. Type your question in the chat input
2. Click "Send" or press Enter
3. View the persona-styled response
4. Access chat history in the sidebar

## Technical Details

### Document Processing (`ingestion.py`)

```python
- PDF loading using PyPDFLoader
- Text splitting with RecursiveCharacterTextSplitter
- Document chunking (1000 chars, 400 overlap)
- Vector embedding using OpenAI
```

### Vector Storage (`docker-compose.yaml`)

```yaml
- Qdrant vector database
- Persistent storage volume
- Exposed ports: 6333 (API), 6334 (REST)
```

### Query Processing (`retrieval.py`)

- Similarity search in vector database
- Context assembly from relevant chunks
- Persona-specific prompt engineering
- GPT-4 response generation

## UI Components

### Main Layout

- Two-column design
- Left: Chat interface
- Right: Persona selector

### Styling Features

- Gradient text effects
- Animated transitions
- Responsive containers
- Custom button styling
- Chat message formatting

## Error Handling

- File size validation
- PDF processing error handling
- Query processing error management
- Database connection error handling

## Performance Considerations

- Chunk size optimization
- Vector search efficiency
- Response caching
- UI responsiveness

## Security

- File size limitations
- API key protection
- Docker volume security
- Input validation

## Future Enhancements

1. Multi-file support
2. Custom persona creation
3. Export chat history
4. Advanced search filters
5. Collaborative features

## Troubleshooting

### Common Issues

1. **PDF Processing Fails**

   - Check file format
   - Verify file size
   - Ensure proper permissions

2. **Vector Database Connection**

   - Verify Docker container status
   - Check port availability
   - Confirm network connectivity

3. **Chat Response Delays**
   - Monitor API rate limits
   - Check chunk size settings
   - Verify system resources

### Support

For additional support or feature requests, please create an issue in the repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
