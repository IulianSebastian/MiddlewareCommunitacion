import multiprocessing
import subprocess
import unittest
import signal
import redis
import time
import os

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

class Testing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = None
        multiprocessing.Process(target=cls.worker(cls)).start()
        time.sleep(2)
        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        cls.work_queue = "work_queue"
        cls.listCensored="listCensored"
        for insult in insults:
            cls.client.sadd("setInsults", insult)

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)

    def test_addInsult(cls):
        choice = "motherfucker"
        cls.client.rpush(cls.work_queue,f"Que te calles {choice} jaja")
        time.sleep(5)
        value = cls.client.lrange(cls.listCensored,0,-1)[-1]
        if choice not in value and "CENSORED" in value :
            cls.assertTrue(True)
        else:
            cls.assertTrue(False)
        
    def worker(cls):
        cls.service = subprocess.Popen(
            ["python3", "../../REDIS/filter/InsultFilter.py","work_queue"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()
