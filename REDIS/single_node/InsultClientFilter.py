import sys
import redis
import random

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = "work_queue"
choice = None
if sys.argv[1] == "0":
    choice = random.choice(insults)
else:
    choice = sys.argv[1] 
client.rpush(work_queue,f"Que te calles {choice} jaja")
print(choice)
