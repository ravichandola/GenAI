from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from ingestion import ingest_url_to_qdrant
from retrieval import get_answer

app = FastAPI(
    title="Web Content RAG API",
    description="API for ingesting web content and answering questions using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestionRequest(BaseModel):
    url: HttpUrl

class IngestionResponse(BaseModel):
    status: str
    message: str
    url: str
    num_chunks: int
    collection_name: str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    status: str
    answer: str
    sources: List[str]
    num_docs_retrieved: int
    collection_used: str

@app.post("/ingest_url", response_model=IngestionResponse)
async def ingest_url(req: IngestionRequest):
    """
    Ingest content from a webpage URL into the vector store.
    
    - **url**: The webpage URL to scrape and ingest
    """
    try:
        result = ingest_url_to_qdrant(str(req.url))
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    """
    Answer a question based on the ingested web content.
    
    - **query**: The question to answer
    """
    try:
        result = get_answer(req.query)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Check if the API is running.
    """
    return {"status": "healthy"}