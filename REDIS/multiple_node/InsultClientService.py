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
insultChannel=sys.argv[2]
choice = None
if sys.argv[1] == "0":
    choice = random.choice(insults)
else:
    choice = sys.argv[1] 
client.publish(insultChannel,choice)
print(choice)
