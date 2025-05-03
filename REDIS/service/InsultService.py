#python3 InsultService.py InsultChannel(Channel of comunication with client) ObserverChannel
import multiprocessing
import random
import redis
import time
import json
import sys

insultChannel = sys.argv[1]
observerChannel = sys.argv[2]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
setList = "setInsults"
proc = None

def activateBroadcast():
    global proc
    if (proc is None) or (not proc.is_alive()):
        proc = multiprocessing.Process(target=broadcaster)
        proc.start()

def deactivateBroadcast():
    if ((proc is not None) and (proc.is_alive())):
        proc.terminate()

def broadcaster():
    while True:
        insultlist = client.smembers(setList)
        if insultlist:
            choice = random.choice(list(insultlist))
            client.publish(observerChannel, json.dumps({"result":choice}))
        time.sleep(5)

def listInsults(queue):
    print(json.dumps({"result":list(client.smembers(setList))}))
    client.rpush(queue,json.dumps({"result":list(client.smembers(setList))}))

def insult_me(queue):
    client.rpush(queue,json.dumps({"result":random.choice(list(client.smembers(setList)))}))

pubsub = client.pubsub()
pubsub.subscribe(insultChannel)

for message in pubsub.listen():
    if message["type"] == "message":
        msg = json.loads(message["data"])
        if msg["pet"] == "1":
            activateBroadcast()
        elif msg["pet"] == "2":
            deactivateBroadcast()
        elif msg["pet"] == "3":
            listInsults(msg["queue"])
        elif msg["pet"] == "4":
            insult_me(msg["queue"])
        else:
            with client.pipeline() as pipe:
                pipe.multi()
                pipe.sadd(setList, msg["pet"])
                pipe.incr('counter')
                pipe.execute()