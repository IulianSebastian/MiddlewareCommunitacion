import pika
import random
import time

class Worker:
    def __init__(self):
        self.insults = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        
        self.channel.queue_declare(queue='insultChannel')
        self.channel.exchange_declare(exchange='subscribers', exchange_type='fanout')
        
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='insultChannel', on_message_callback=self.on_message, auto_ack=False)
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, body):
        msg = body.decode().strip()
        if msg == "4":  
            if properties.reply_to:
                response = random.choice(self.insults) if self.insults else "NO HI HA INSULTS A LA LLISTA"
                ch.basic_publish(exchange='', routing_key=properties.reply_to, body=response)
        elif msg == "3":  
            if properties.reply_to:
                response = ", ".join(self.insults)
                ch.basic_publish(exchange='', routing_key=properties.reply_to, body=response)
        else:  
            if msg not in self.insults:
                self.insults.append(msg)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

