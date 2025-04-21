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
        cls.client = xmlrpc.client.ServerProxy('http://localhost:8000')

    @classmethod
    def tearDownClass(cls):
        os.killpg(os.getpgid(cls.service.pid), signal.SIGTERM)

    def test_addInsult(self):
        self.client.add_insult("Loco")
        self.assertEqual(["Loco"],self.client.get_insults())

    def test_getInsult(self):
        self.assertEqual("Loco",self.client.get_insult())

    def test_observer(self):
        with open("observer.txt", "w") as sal:
            observer = subprocess.Popen(
                ["python3", "-u", "../../XMLRPC/service/InsultObserver.py","8000","4848"],
                stdout=sal,
                stderr=sal,
                preexec_fn=os.setsid
            )

            time.sleep(5)
            os.killpg(os.getpgid(observer.pid), signal.SIGTERM)
            observer.wait()

        with open("observer.txt", "r") as file:
            lines = file.readlines()
            if (any("This http://localhost:4848 has been added as a suscriber" in line for line in lines) and 
                any("The Broadcast has been activated" in line for line in lines) and 
                any("Loco" in line for line in lines) and 
                any("The Broadcast has been deactivated" in line for line in lines) and 
                any("This http://localhost:4848 has been deleted as a suscriber" in line for line in lines)):
                    self.assertTrue(True)
            else:
                self.assertTrue(False)

    def worker(cls):
        cls.service = subprocess.Popen(
            ["python3", "../../XMLRPC/service/InsultService.py","8000"],
            preexec_fn=os.setsid 
        )

if __name__ == 'main':
    unittest.main()
