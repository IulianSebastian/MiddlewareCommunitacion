import multiprocessing
import subprocess
import unittest
import signal
import redis
import json
import time
import os

class Testing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = None
        multiprocessing.Process(target=cls.worker(cls)).start()
        time.sleep(2)
        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        cls.setList = "setInsults"
        cls.insultChannel= "insultChannel"

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)

    def test_addInsult(cls):
        cls.client.delete(cls.setList)
        choice = "loco"
        
        for _ in range(10):
            cls.client.publish(cls.insultChannel,json.dumps({"pet":choice}))

        time.sleep(2)
        
        cls.client.publish(cls.insultChannel,json.dumps({"pet":"3","queue":"this_queue"}))
        while True:
            result = cls.client.blpop("this_queue",timeout=0)
            if result:
                set = list((json.loads(result[1]))["result"])
                break

        if choice in set and len(set) == 1:
            cls.assertTrue(True)
        else:
            cls.assertTrue(False)
    
    def test_insultme(cls):
        cls.client.publish(cls.insultChannel,json.dumps({"pet":"4","queue":"this_queue"}))
        while True:
            result = cls.client.blpop("this_queue",timeout=0)
            if result:
                insultme = (json.loads(result[1]))["result"]
                break

        if  insultme == "loco":
            cls.assertTrue(True)
        else:
            cls.assertTrue(False)

    def test_broadcast(cls):

        messageObserver = None
        cls.client.publish(cls.insultChannel,json.dumps({"pet":"1"}))
        
        pubsub = cls.client.pubsub()
        pubsub.subscribe("observerChannel")

        for message in pubsub.listen():
            if message["type"] == "message":
                messageObserver = json.loads(message['data'])["result"]
                cls.client.publish(cls.insultChannel,json.dumps({"pet":"2"}))
                break

        cls.assertEqual("loco",messageObserver)
        
    def worker(cls):
        cls.service = subprocess.Popen(
            ["python3", "../../REDIS/service/InsultService.py","insultChannel","observerChannel"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()
