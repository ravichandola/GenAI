#Retrieval Phase
#1. Take the user query
#2. Vector Similarity Search [Query] in DB
#3. Retrieve the relevant chunks
#4. Pass the chunks to the LLM
#5. Return the answer

from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

#Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)
#Load the vector store
vector_db = QdrantVectorStore.from_existing_collection(
    url = "http://localhost:6333",
    collection_name = "Learning-Vectors",
    embedding = embedding_model,
)

while True:
    try:
        #Take the user query    
        userQuery = input("\nEnter your query here (or type 'exit' to quit): ")
        
        if userQuery.lower() == 'exit':
            print("Goodbye! 👋")
            break
            
        #vector Similarity Search [Query] in DB
        search_results = vector_db.similarity_search(
            query = userQuery,
            )

        context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

        #System Prompt
        system_prompt = f"""
        You are a helpful assistant that can answer user query based on the available context retrieved from
        a pdf file. anlong with the page_content and page number. 

        You should only answer the question based on the context provided and navigate the user to open the right
        page number in the pdf file.

        Context:
        {context}
        """

        chat_completion = client.chat.completions.create(
            model = "gpt-4",  # Fixed typo in model name
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": userQuery}
            ]
        )

        print(f"🤖: {chat_completion.choices[0].message.content}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        continue
