import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

listName = "listInsults"
setList = "setInsults"

while True:
    task = client.lpop(listName)
    if task is not None:
        print(task)
        client.sadd(setList,task)
        time.sleep(3)