import uvicorn
from dotenv import load_dotenv
from rag_queue.server import app

load_dotenv()


def main():
    uvicorn.run(app, port=8002, host="0.0.0.0")


main()
