import unittest
import Pyro4

class TestInsultFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ns = Pyro4.locateNS()
        cls.insult_service = Pyro4.Proxy(ns.lookup("insult.service"))
        cls.filter = Pyro4.Proxy(ns.lookup("insult.filter"))

        cls.insult_service.add_insult("CAVERO")
        cls.insult_service.add_insult("UCRANIANO")

    def test_filter_censors_insults(self):
        texts = [
            "Hola, que tal",
            "Adeu CAVERO",
            "Ets CAVERO i UCRANIANO"
        ]

        expected_results = [
            "Hola, que tal",
            "Adeu CENSORED",
            "Ets CENSORED i CENSORED"
        ]

        for text, expected in zip(texts, expected_results):
            result = self.filter.send_text(text)
            self.assertIn(expected, result)

    def test_get_result_list(self):
        results = self.filter.get_result_list()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        for msg in results:
            self.assertNotIn("CAVERO", msg)
            self.assertNotIn("UCRANIANO", msg)

if __name__ == "__main__":
    unittest.main()
