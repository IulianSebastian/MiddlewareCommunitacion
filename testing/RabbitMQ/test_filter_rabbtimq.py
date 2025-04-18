import pika
import unittest


class TestInsultFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        insults_de_prova = ["CAVERO", "UCRANIANO", "RUMANO"]
        cls.connexio = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        cls.canal = cls.connexio.channel()
        cls.canal.queue_declare(queue='insultChannel')
        print("Inicialitzant InsultService afegint insults")
        for insult in insults_de_prova:
            cls.canal.basic_publish(exchange='', routing_key='insultChannel', body=insult)
        cls.canal.queue_declare(queue="WorkQueue")
        cls.result = cls.canal.queue_declare(queue='', exclusive=True)
        cls.callback_queue = cls.result.method.queue

    @classmethod
    def tearDownClass(cls):
        cls.connexio.close()

    def wait_response(self):
        method, props, body = self.canal.basic_get(queue=self.callback_queue, auto_ack=True)
        while body is None:
            method, props, body = self.canal.basic_get(queue=self.callback_queue, auto_ack=True)
        return body.decode()

    def test_1_text_no_insults(self):
        print("Sending text: Text sense insults")
        self.canal.basic_publish(exchange='', routing_key='WorkQueue', body="Text sense insults")
        self.canal.basic_publish(exchange='', routing_key='WorkQueue', properties=pika.BasicProperties(reply_to=self.callback_queue), body='1')
        resposta = self.wait_response()
        print(f"Received text list: {resposta}")
        self.assertIsNotNone(resposta)
        self.assertIn("Text sense insults", resposta)

    def test_2_amb_insults(self):
        print("Sending text: Ets un CAVERO")
        print("Expected text: Ets un CENSORED")
        self.canal.basic_publish(exchange='', routing_key='WorkQueue', body="Ets un CAVERO")
        self.canal.basic_publish(exchange='', routing_key='WorkQueue', properties=pika.BasicProperties(reply_to=self.callback_queue), body='1')
        resposta = self.wait_response()
        print(f"Received text list: {resposta}")
        self.assertIsNotNone(resposta)
        self.assertIn("Ets un CENSORED", resposta)

    def test_3_get_result_list(self):
        print("Expected result list: Text sense insults, Ets un CENSORED")
        self.canal.basic_publish(exchange='', routing_key='WorkQueue', properties=pika.BasicProperties(reply_to=self.callback_queue), body='1')
        resposta = self.wait_response()
        print(f"Received result list: {resposta}")
        self.assertEqual("Text sense insults, Ets un CENSORED", resposta)
    
if __name__ == "__main__":
    unittest.main()
