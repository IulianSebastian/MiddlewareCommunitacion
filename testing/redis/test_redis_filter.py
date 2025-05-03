import multiprocessing
import subprocess
import unittest
import signal
import redis
import json
import time
import os

INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]

class Testing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = None
        cls.filter = None
        multiprocessing.Process(target=cls.worker(cls)).start()
        time.sleep(2)
        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        cls.work_queue = "work_queue"
        cls.listCensored="listCensored"
        for insult in INSULTS:
            cls.client.publish("insultChannel",json.dumps({"pet":insult}))

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)
        os.killpg(os.getpgid(cls.filter.pid), signal.SIGTERM)

    def test_addInsult(cls):
        cls.client.delete("listCensored")
        choice = "CAVERO"
        cls.client.rpush(cls.work_queue,json.dumps({"pet":f"Que te calles {choice}"}))
        time.sleep(5)
        value = cls.client.lrange(cls.listCensored,0,-1)[-1]
        if choice not in value and "CENSORED" in value:
            cls.assertTrue(True)
        else:
            cls.assertTrue(False)

    def test_listInsults(cls):
        cls.client.rpush(cls.work_queue,json.dumps({"pet":"3","queue":"this_queue"}))
        while True:
            result = cls.client.blpop("this_queue",timeout=0)
            if result:
                insults = list((json.loads(result[1]))["result"])
                break

        if  insults[0] == "Que te calles CENSORED":
            cls.assertTrue(True)
        else:
            cls.assertTrue(False)
        
    def worker(cls):
        cls.filter = subprocess.Popen(
            ["python3", "../../REDIS/filter/InsultFilter.py","work_queue","insultChannel","unique"],
            preexec_fn=os.setsid 
        )
        cls.service = subprocess.Popen(
            ["python3", "../../REDIS/service/InsultService.py","insultChannel","observerChannel"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()
