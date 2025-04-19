import multiprocessing
import subprocess
import unittest
import signal
import redis
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
        cls.observerChannel = "newsChannel"

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)

    def test_addInsult(cls):
        cls.client.delete(cls.setList)
        choice = "loco"
        for i in range(10):
            cls.client.publish(cls.insultChannel,choice)
        time.sleep(2)
        set = cls.client.smembers(cls.setList)
        if choice in set and len(set) == 1:
            cls.assertTrue(True)
        else:
            cls.assertTrue(False)

    def test_broadcast(cls):

        messageObserver = None
        cls.client.publish(cls.insultChannel,"1")
        
        pubsub = cls.client.pubsub()
        pubsub.subscribe(cls.observerChannel)

        for message in pubsub.listen():
            if message["type"] == "message":
                messageObserver = message["data"]
                cls.client.publish(cls.insultChannel,"2")
                break

        cls.assertEqual("loco",messageObserver)
        
    def worker(cls):
        cls.service = subprocess.Popen(
            ["python3", "../../REDIS/single_node/InsultService.py"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()
