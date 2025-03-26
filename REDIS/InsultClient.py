import sys
sys.path.insert(0, '../')

import redis
from insults import listInsults
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insultChannel="insultChannel"
choice = random.choice(listInsults.insult)
# choice = 1 
client.publish(insultChannel,choice)
print(choice)