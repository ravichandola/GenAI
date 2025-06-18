#!/bin/bash


# Load env variables
export $(grep -v '^#' .env | xargs -d '\n') 

# Set Python path to include parent directory so rag_queue module can be found
export PYTHONPATH=/workspaces/GenAI

# Start RQ worker with scheduler
rq worker --with-scheduler --url redis://valkey:6379 --path /workspaces/GenAI
