from redis import Redis
from rq import Queue

# Now I want to create one queue
queue = Queue(connection=Redis())
