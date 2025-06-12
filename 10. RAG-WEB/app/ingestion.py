# app/ingest.py
from utils import scrape_text_from_url
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import os
import logging
from typing import Dict, Any
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "webpage_chunks")
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost:6334")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_CHUNK_SIZE = int(os.getenv("MAX_CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

def validate_url(url: str) -> bool:
    """Validate if the given string is a proper URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def ingest_url_to_qdrant(url: str) -> Dict[str, Any]:
    """
    Ingest content from a URL into Qdrant vector store.
    
    Args:
        url (str): The URL to scrape and ingest
        
    Returns:
        Dict[str, Any]: Status of the ingestion
        
    Raises:
        ValueError: If URL is invalid
        Exception: For other errors during ingestion
    """
    try:
        if not validate_url(url):
            raise ValueError("Invalid URL provided")
            
        logger.info(f"Starting ingestion for URL: {url}")
        
        # Scrape content
        raw_text = scrape_text_from_url(url)
        if not raw_text:
            raise ValueError("No content could be extracted from the URL")
            
        logger.info(f"Successfully scraped {len(raw_text)} characters")

        # Chunking
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=MAX_CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )
        chunks = splitter.split_text(raw_text)
        
        if not chunks:
            raise ValueError("No chunks were created from the content")
            
        logger.info(f"Created {len(chunks)} chunks")

        # Create documents with metadata
        documents = [
            Document(
                page_content=chunk,
                metadata={
                    "source": url,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            ) for i, chunk in enumerate(chunks)
        ]

        # Initialize embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

        # Store in Qdrant
        qdrant = Qdrant.from_documents(
            documents,
            embeddings,
            url=QDRANT_HOST,
            prefer_grpc=False,
            collection_name=COLLECTION_NAME,
        )

        return {
            "status": "success",
            "message": f"Successfully ingested {len(chunks)} chunks",
            "url": url,
            "num_chunks": len(chunks),
            "collection_name": COLLECTION_NAME
        }

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise
    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}", exc_info=True)
        raise Exception(f"Failed to ingest URL: {str(e)}")
