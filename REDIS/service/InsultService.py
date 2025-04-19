#python3 InsultService.py InsultChannel(Channel of comunication with client) ObserverChannel
import multiprocessing
import random
import redis
import time
import sys

insultChannel = sys.argv[1]
observerChannel = sys.argv[2]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
setList = "setInsults"
proc = None

# Methods for the Broadcast Utility
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
            client.publish(observerChannel, choice)
        time.sleep(5)

# InsultService request and activate/deactivate.Broadcast
pubsub = client.pubsub()
pubsub.subscribe(insultChannel)

for message in pubsub.listen():
    if message["type"] == "message":
        match message["data"][0]:
            case "1":
                print("Activating broadcast")
                activateBroadcast()
            case "2":
                print("Deactivating broadcast")
                deactivateBroadcast()
            case _:
                client.sadd(setList, message["data"])
