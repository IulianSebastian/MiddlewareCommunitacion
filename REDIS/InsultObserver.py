import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

pubsub = client.pubsub()
observerChannel = "newsChannel"
pubsub.subscribe(observerChannel)

for message in pubsub.listen():
    if message["type"] == "message":
        print(f"The message {message['data']}")