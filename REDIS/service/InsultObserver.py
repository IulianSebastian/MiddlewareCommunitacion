#python3 InsultObserver ObserverChannel
import redis
import time
import json
import sys

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

pubsub = client.pubsub()
observerChannel = sys.argv[1]
pubsub.subscribe(observerChannel)

for message in pubsub.listen():
    if message["type"] == "message":
        print(f"The message {json.loads(message['data'])["result"]}")
