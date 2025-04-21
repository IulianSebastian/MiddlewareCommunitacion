#python3 InsultClient.py where_to_send option( 0 -> Random Insult 1-> Activate Broadcast 2 -> Deactivate Broadcast [1 and 2 only for service]) (service or filter)
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
send=sys.argv[1]
choice = None
if sys.argv[2] == "0":
    choice = random.choice(insults)
else:
    choice = sys.argv[2] 

if sys.argv[3] == "service":
    client.publish(send,choice)
elif sys.argv[3] == "filter":
    client.rpush(send,f"Que te calles {choice} jaja")
print(choice)