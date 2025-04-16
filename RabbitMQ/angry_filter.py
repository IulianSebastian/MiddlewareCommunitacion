import pika
import time
import random

insults=["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
text=["Hola ", "Adeu ", "Vale ", "Ets "]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='WorkQueue')



while True:
    msg = random.choice(text)+random.choice(insults)
    channel.basic_publish(exchange='', routing_key='WorkQueue', body=msg)
    print(f"New text produced: {msg}")
    time.sleep(3)
