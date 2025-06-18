from fastapi import FastAPI, Query, Path
from rag_queue.task_queue.connection import queue

app = FastAPI()


@app.get('/')
def root():
    return {"status": 'Server is up and running'}


@app.post('/chat')
def chat(
    query: str = Query(..., description="Chat Message")
):
    # Enqueue the job with the function path as string
    job = queue.enqueue('rag_queue.task_queue.workers.process_query', query)

    # Return job status
    return {"status": "queued", "job_id": job.id}


@app.get("/result/{job_id}")
def get_result(
    job_id: str = Path(..., description="Job ID")
):
    job = queue.fetch_job(job_id=job_id)
    if job is None:
        return {"error": "Job not found", "status": "not_found"}

    if job.is_finished:
        result = job.return_value()
        return {"result": result, "status": "completed"}
    elif job.is_failed:
        return {"error": str(job.exc_info), "status": "failed"}
    else:
        return {"status": "in_progress"}
