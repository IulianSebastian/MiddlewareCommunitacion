import multiprocessing
import xmlrpc.client
import subprocess
import unittest
import signal
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
        cls.working = None
        cls.server = None
        multiprocessing.Process(target=cls.worker(cls)).start()
        time.sleep(2)
        cls.client = xmlrpc.client.ServerProxy('http://localhost:8080')
        for insult in insults:
            xmlrpc.client.ServerProxy('http://localhost:8000').add_insult(insult)

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)
        os.killpg(os.getpgid(cls.working.pid), signal.SIGTERM)
        os.killpg(os.getpgid(cls.server.pid), signal.SIGTERM)

    def test_allWorker(cls):
        cls.client.send_text("what happens motherfucker")
        insults = cls.client.get_insults()
        if any("motherfucker" in insult for insult in insults):
            cls.assertFalse(True)
        else:
            if any("CENSORED" in insult for insult in insults):
                cls.assertTrue(True)

    def worker(cls):
        cls.server = subprocess.Popen(
            ["python3", "../../XMLRPC/filter/InsultFilterServer.py","8080"],
            preexec_fn=os.setsid 
        )
        time.sleep(5)
        cls.working = subprocess.Popen(
            ["python3", "../../XMLRPC/filter/InsultFilterWorker.py","8080","8081","8000"],
            preexec_fn=os.setsid 
        )
        time.sleep(5)
        cls.service = subprocess.Popen(
            ["python3", "../../XMLRPC/service/InsultService.py","8000"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()