# app/retrieval.py
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from typing import Dict, Any, List
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "webpage_chunks")
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost:6334")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Simplified prompt template
CUSTOM_PROMPT = """Answer the question based on the context.
If you don't know the answer, just say that you don't know.

Context: {context}
Question: {question}
Answer:"""

def get_answer(query: str) -> Dict[str, Any]:
    """Get an answer for a query using RAG with web content."""
    try:
        if not query.strip():
            raise ValueError("Query cannot be empty")
            
        logger.info(f"Processing query: {query}")

        # Initialize embeddings
        embeddings_model = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        # Initialize vector store from existing collection
        vector_store = QdrantVectorStore.from_existing_collection(
            url=QDRANT_HOST,
            collection_name=COLLECTION_NAME,
            embedding=embeddings_model,
            prefer_grpc=False,
            timeout=10
        )

        # Simple retriever setup
        retriever = vector_store.as_retriever(
            search_type="similarity",
            k=3
        )

        # Initialize LLM
        llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo"
        )

        # Create QA chain with simple prompt
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": PromptTemplate(
                    template=CUSTOM_PROMPT,
                    input_variables=["context", "question"]
                )
            }
        )

        # Get answer
        result = qa_chain({"query": query})
        
        # Extract sources
        sources = []
        for doc in result.get("source_documents", []):
            if doc.metadata.get("source") not in sources:
                sources.append(doc.metadata.get("source"))

        return {
            "status": "success",
            "answer": result["result"],
            "sources": sources
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise Exception(f"Failed to get answer: {str(e)}")
