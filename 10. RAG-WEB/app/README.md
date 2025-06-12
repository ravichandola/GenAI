# Web Content RAG API

A FastAPI-based API that allows you to ingest web content and ask questions about it using Retrieval-Augmented Generation (RAG).

## Features

- Scrape and ingest content from any webpage
- Clean and process text content
- Store content in Qdrant vector database
- Answer questions about the ingested content using OpenAI's GPT model
- RESTful API with proper error handling and documentation

## Prerequisites

- Python 3.8+
- Docker (for running Qdrant)
- OpenAI API key

## Setup

1. Clone the repository and navigate to the app directory:

```bash
cd app
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your-openai-api-key
QDRANT_HOST=http://localhost:6334
COLLECTION_NAME=webpage_chunks
MAX_CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

4. Start Qdrant using Docker:

```bash
docker-compose up -d
```

5. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Ingest URL

```http
POST /ingest_url
Content-Type: application/json

{
    "url": "https://example.com/article"
}
```

### 2. Query Content

```http
POST /query
Content-Type: application/json

{
    "query": "What is the main topic of the article?"
}
```

### 3. Health Check

```http
GET /health
```

## API Documentation

Once the server is running, you can access:

- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Error Handling

The API includes comprehensive error handling for:

- Invalid URLs
- Network issues
- Content extraction failures
- Empty or invalid queries
- Database connection issues

## Example Usage

1. Ingest a webpage:

```bash
curl -X POST "http://localhost:8000/ingest_url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/article"}'
```

2. Ask a question:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the main topic discussed?"}'
```

## Notes

- The API uses OpenAI's GPT model for generating answers
- Content is stored in Qdrant vector database for efficient retrieval
- Text is cleaned and processed before storage
- Responses include source URLs and metadata
- CORS is enabled for all origins (customize in production)
