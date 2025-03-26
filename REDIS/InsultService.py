import redis
import time
import random
import multiprocessing

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

listName = "listInsults"
setList = "setInsults"
news = "news_channel"
proc = None

def activateBroadcast():
    if (proc is None) or (not proc.is_alive()):
        proc = multiprocessing.Process(target=broadcaster)
        proc.start()

def deactivateBroadcast():
    if ((proc is not None) and (proc.is_alive())):
        proc.terminate()

def broadcaster():
    while True:
        choice = random.choice(client.lrange(setList,0,-1))
        client.lpush(news,choice)
        time.sleep(5)

while True:
    task = client.lpop(listName)
    if task is not None:
        match task[0]:
            case 1:
                activateBroadcast()
            case 2:
                deactivateBroadcast()
            case _:
                client.sadd(setList,task)
    time.sleep(3)