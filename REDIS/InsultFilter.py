import redis
import sys
from insults import listInsults

sys.path.insert(0, '../')

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = "work_queue"

def censore(message):
    listCensored="listCensored"
    for insult in listInsults.insults:
        if insult in message:
            message.replace(insult,"CENSORED")
    client.lpush(listCensored,message) 

while True:
    task = client.blpop(work_queue,timeout=0)
    if task:
        censore(task[0])