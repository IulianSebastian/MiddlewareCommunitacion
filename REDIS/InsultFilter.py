import redis
# import sys
# import os
# pwd = os.getcwd()
# print(f'{pwd}/../')
# sys.path.insert(0, '/home/iulian-sebastian-oprea/Documents/sd/task1/task1_sd/')
# from insults import listInsults

insult = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = "work_queue"

def censore(message):
    listCensored="listCensored"
    for ins in insult:
        if ins in message:
            message = message.replace(ins,"CENSORED")
    client.lpush(listCensored,message) 

while True:
    task = client.blpop(work_queue,timeout=0)
    if task:
        censore(task[1])