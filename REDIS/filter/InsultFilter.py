#python3 InsultFilter.py queue_where_to_work channel_service unique_queue_where_service_wil_send_message
import redis
import json
import sys

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = sys.argv[1]
channel = sys.argv[2]
queue = sys.argv[3]
listCensored="listCensored"

def censore(message):
    client.publish(channel,json.dumps({"pet":"3","queue":queue}))

    insults = None
    while insults is None:
        result = client.blpop(queue,timeout=0)
        if result:
            insults=list((json.loads(result[1]))["result"])

    for ins in insults:
        if ins in message:
            message = message.replace(ins,"CENSORED")

    with client.pipeline() as pipe:
        pipe.multi()
        client.lpush(listCensored,message)
        pipe.incr('counter')
        pipe.execute()

def listInsults(queue):
    client.rpush(queue,json.dumps({"result":list(client.lrange(listCensored,0,-1))}))

while True:
    task = client.blpop(work_queue,timeout=0)
    if task:
        msg = json.loads(task[1])
        if msg["pet"] == "3":
            listInsults(msg["queue"])
        else:
            censore(message=msg["pet"])

