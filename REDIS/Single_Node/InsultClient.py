import sys
sys.path.insert(0, '../../')

import redis
from insults import listInsults
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
listName = "listInsults"
choice = random.choice(listInsults.insult)
client.rpush(listName,choice)
print(choice)