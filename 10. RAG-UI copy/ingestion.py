import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

def ingest_pdf(pdf_path: str, collection_name: str = "Learning-Vectors"):
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    chunks = splitter.split_documents(documents)

    embedding = OpenAIEmbeddings(model="text-embedding-3-large")

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        url="http://localhost:6333",
        collection_name=collection_name,
        embedding=embedding
    )
    return True
