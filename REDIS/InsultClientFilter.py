import sys
sys.path.insert(0, '../')

import redis
from insults import listInsults
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = "work_queue"
choice = random.choice(listInsults.insult)
# choice = 1 
client.rpush(work_queue,f"Que te calles {choice} jaja")
print(choice)