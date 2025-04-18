import unittest
import pika
import time


class TestServeiInsultsRabbitMQ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.insults_de_prova = ["CAVERO", "UCRANIANO", "RUMANO"]
        cls.connexio = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        cls.canal = cls.connexio.channel()
        cls.canal.queue_declare(queue='insultChannel')

    @classmethod
    def tearDownClass(cls):
        cls.connexio.close()

    def test_1_afegir_insults(self):
        for insult in self.insults_de_prova:
            self.canal.basic_publish(exchange='', routing_key='insultChannel', body=insult)
            print(f"Insult enviat: {insult}")
        self.assertTrue(True)

    def test_2_veure_llista_insults(self):
        resultat = self.canal.queue_declare(queue='', exclusive=True)
        cua_callback = resultat.method.queue
        resposta = []

        def on_response(ch, method, props, body):
            resposta.append(body.decode())

        self.canal.basic_consume(queue=cua_callback, on_message_callback=on_response, auto_ack=True)

        self.canal.basic_publish(exchange='',routing_key='insultChannel',properties=pika.BasicProperties(reply_to=cua_callback),body='3')

        timeout = time.time() + 3
        while not resposta and time.time() < timeout:
            self.connexio.process_data_events(time_limit=0.1)

        self.assertTrue(resposta, "No s'ha rebut cap resposta amb la llista d'insults")
        llista = resposta[0]
        for insult in self.insults_de_prova:
            self.assertIn(insult, llista)

    def test_3_activar_i_rebre_broadcast(self):
        self.canal.exchange_declare(exchange='subscribers', exchange_type='fanout')
        resultat = self.canal.queue_declare(queue='', exclusive=True)
        nom_cua = resultat.method.queue
        self.canal.queue_bind(exchange='subscribers', queue=nom_cua)

        self.canal.basic_publish(exchange='', routing_key='insultChannel', body='1')

        rebut = []

        def on_message(ch, method, props, body):
            rebut.append(body.decode())

        self.canal.basic_consume(queue=nom_cua, on_message_callback=on_message, auto_ack=True)

        timeout = time.time() + 6
        while not rebut and time.time() < timeout:
            self.connexio.process_data_events(time_limit=0.1)

        self.canal.basic_publish(exchange='', routing_key='insultChannel', body='2')

        self.assertTrue(rebut, "No s'ha rebut cap insult pel canal de broadcast")


if __name__ == '__main__':
    unittest.main()
