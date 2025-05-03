# python3 InsultClient.py (service or filter) / where_to_send / petition / queue 
import sys
import redis
import json

client=redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
send=sys.argv[2]
choice=json.dumps({"pet":sys.argv[3],"queue":sys.argv[4]})

if sys.argv[1] == "service":
    client.publish(send,choice)
elif sys.argv[1] == "filter":
    client.rpush(send,choice)

if sys.argv[4] != "0":
    while True:
        result = client.blpop(sys.argv[4],timeout=0)
        if result:
            print(list((json.loads(result[1]))["result"]))
            break