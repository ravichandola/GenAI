# RAG (Retrieval Augmented Generation) Implementation

This document outlines a complete RAG-based document question-answering system that processes PDF documents, stores them in a vector database, and enables semantic search with contextual answers.

## Table of Contents

- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Setup Instructions](#setup-instructions)
- [Implementation Details](#implementation-details)
  - [Document Indexing](#document-indexing)
  - [Query Processing](#query-processing)
- [Technical Requirements](#technical-requirements)
- [Usage Guide](#usage-guide)
- [Error Handling](#error-handling)

## Project Structure

```
8. RAG/
├── chat.py              # Query processing and response generation
├── indexing.py          # Document processing and vector storage
├── docker-compose.yaml  # Qdrant vector database setup
├── nodejs.pdf          # Sample document for processing
└── rag.md              # Documentation
```

## System Architecture

The system implements a complete RAG pipeline with the following components:

1. **Document Processing**

   - PDF loading and parsing
   - Text chunking with overlap
   - Vector embedding generation

2. **Vector Store (Qdrant)**

   - Stores document embeddings
   - Enables similarity search
   - Runs in Docker container
   - Persistent storage

3. **Embedding Model**

   - Uses OpenAI's `text-embedding-3-large`
   - Converts text into high-dimensional vectors

4. **LLM Integration**
   - Utilizes GPT-4 for response generation
   - Contextual answer synthesis
   - Source reference inclusion

## Setup Instructions

### 1. Environment Setup

Create a `.env` file with:

```
OPENAI_API_KEY=your_api_key_here
```

### 2. Start Qdrant Vector Database

```bash
docker-compose up -d
```

Docker Compose configuration (`docker-compose.yaml`):

```yaml
version: "3.8"

services:
  vector-db:
    image: qdrant/qdrant
    ports:
      - "6333:6333"
      - "6334:6334" # REST API
    volumes:
      - qdrant_storage:/qdrant/storage

volumes:
  qdrant_storage:
    driver: local
```

## Implementation Details

### Document Indexing

The indexing process (`indexing.py`) handles document preprocessing:

```python
# 1. Load PDF
loader = PyPDFLoader(file_path=pdf_path)
documents = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400  # Maintains context between chunks
)
chunks = text_splitter.split_documents(documents)

# 3. Create embeddings and store
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    url="http://localhost:6333",
    collection_name="Learning-Vectors",
    embedding=embedding_model,
)
```

### Query Processing

The query processing system (`chat.py`) handles user interactions:

1. **Vector Store Connection**

```python
vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    collection_name = "Learning-Vectors",
    embedding = embedding_model,
)
```

2. **Context Formation**

```python
context = "\n\n\n".join([
    f"Page Content: {result.page_content}\n
    Page Number: {result.metadata['page_label']}\n
    File Location: {result.metadata['source']}"
    for result in search_results
])
```

3. **Response Generation**

```python
chat_completion = client.chat.completions.create(
    model = "gpt-4",
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": userQuery}
    ]
)
```

## Technical Requirements

### Dependencies

- Python 3.x
- Docker and Docker Compose
- OpenAI API key
- Required Python packages:
  - `openai`
  - `langchain_qdrant`
  - `langchain_openai`
  - `langchain_community`
  - `langchain_text_splitters`
  - `python-dotenv`

## Usage Guide

1. **Initial Setup**

   ```bash
   # Start Qdrant
   docker-compose up -d

   # Index documents
   python indexing.py
   ```

2. **Process New Documents**

   - Place PDF files in the RAG directory
   - Update the `pdf_path` in `indexing.py`
   - Run the indexing script

3. **Query Documents**
   ```bash
   python chat.py
   ```
   - Enter questions when prompted
   - Receive answers with page references
   - Type 'exit' to quit

## Error Handling

The system includes robust error handling in both indexing and querying:

1. **Indexing Errors**

   - PDF loading failures
   - Embedding generation issues
   - Vector store connection problems

2. **Query Errors**

```python
try:
    # Query processing logic
except Exception as e:
    print(f"An error occurred: {str(e)}")
    continue
```

Common error scenarios:

- API connection failures
- Vector store connectivity issues
- Invalid queries
- Rate limiting

## Future Improvements

1. Web interface implementation
2. Multi-document type support
3. Batch query processing
4. Response caching
5. Advanced filtering options
6. Automated document monitoring
7. Bulk document processing

---

_Note: The current implementation includes both document preprocessing and query processing steps. The system is configured to work with PDF documents by default, but can be extended to support other document types._
