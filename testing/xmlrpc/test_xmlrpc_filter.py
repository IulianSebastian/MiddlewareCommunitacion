import multiprocessing
import xmlrpc.client
import subprocess
import unittest
import signal
import time
import os

class Testing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = None
        multiprocessing.Process(target=cls.worker(cls)).start()
        time.sleep(2)
        cls.client = xmlrpc.client.ServerProxy('http://localhost:8080')

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)

    def test_allWorker(cls):
        cls.client.send_text("what happens motherfucker")
        insults = cls.client.get_insults()
        if any("motherfucker" in insult for insult in insults):
            cls.assertFalse(True)
        else:
            if any("CENSORED" in insult for insult in insults):
                cls.assertTrue(True)

    def worker(cls):
        cls.service = subprocess.Popen(
            ["python3", "../../XMLRPC/WorkQueue/InsultFilterWorker.py","8080"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()