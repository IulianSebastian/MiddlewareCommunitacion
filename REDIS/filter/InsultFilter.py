#python3 InsultFilter.py Queue_where_to_work
import redis
import sys

insult = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = sys.argv[1]

def censore(message):
    listCensored="listCensored"
    for ins in insult:
        if ins in message:
            message = message.replace(ins,"CENSORED")
    print(message)
    client.lpush(listCensored,message) 

while True:
    task = client.blpop(work_queue,timeout=0)
    if task:
        censore(task[1])
