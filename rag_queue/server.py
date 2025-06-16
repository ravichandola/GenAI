from fastapi import FastAPI, Query
from .queue.connection import queue
from .queue.workers import process_query

app = FastAPI()


@app.get("/")
def root():
    return {"status" : "server is up and running"}


@app.post("/chat")
def chat(
    query: str = Query(..., description="The query to search for")
):
    job = queue.enqueue(process_query, query)
    return {"status" : "your job recieved and is being processed","job_id" : job.id}

#is query ko queue me add karna hai
#user ko bolo your job recieved

