import unittest
import Pyro4
import time



@Pyro4.expose
class FakeClient:
    def __init__(self):
        self.last_message = None

    def update(self, message):
        self.last_message = message
        print(f"Rebut broadcast: {message}")

class TestInsultServicePyro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ns = Pyro4.locateNS()
        uri = ns.lookup("insult.service")
        cls.server = Pyro4.Proxy(uri)

    def test_1_add_insult(self):
        r1 = self.server.add_insult("TEST_INSULT")
        self.assertIn("added", r1)

        r2 = self.server.add_insult("TEST_INSULT")
        self.assertIn("already", r2)

    def test_2_get_insults(self):
        insults = self.server.get_insults()
        self.assertIsInstance(insults, list)
        self.assertIn("TEST_INSULT", insults)

    def test_3_insult_me(self):
        insult = self.server.insult_me()
        self.assertIn(insult, self.server.get_insults())

    def test_4_subscribe_and_broadcast(self):
        fake = FakeClient()
        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        client_uri = daemon.register(fake)
        ns.register("test.fakeclient", client_uri)

        self.server.subscribe("test.fakeclient")
        self.server.activate_broadcast()
        end_time = time.time() + 6

        def loopCondition():
            return time.time() < end_time

        daemon.requestLoop(loopCondition=loopCondition)

        self.assertIsNotNone(fake.last_message)
        self.server.disable_broadcast()
        self.server.unsubscribe("test.fakeclient")
        ns.remove("test.fakeclient")
        daemon.shutdown()

if __name__ == "__main__":
    unittest.main()
