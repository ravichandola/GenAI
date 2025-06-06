#Ingestion Phase 
#1. Load the PDF file
#2. Split the documents into chunks
#3. Vector Embeddings
#4. Index the chunks in the vector store

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "nodejs.pdf"

# Load the PDF file

loader = PyPDFLoader(file_path=pdf_path)
documents = loader.load()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
#overlap of 400 characters between chunks to maintain context
chunks = text_splitter.split_documents(documents)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Create a vector store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    url="http://localhost:6333",
    collection_name="Learning-Vectors",
    embedding=embedding_model,
)

print("Indexing completed")






