import multiprocessing
import random
import redis
import pika
import time

class Worker:
    
    def __init__(cls):

        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        cls.list_insult = "setInsults"

        cls.manager = multiprocessing.Manager()
        cls.proc = None

        cls.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        cls.channel = cls.connection.channel()

        cls.channel.queue_declare(queue='insultChannel')
        cls.channel.exchange_declare(exchange='subscribers', exchange_type='fanout')
        
        cls.peticions = 0

        cls.start()

    def start(self):
        self.channel.basic_consume(queue='insultChannel', on_message_callback=self.on_message, auto_ack=True)
        self.channel.start_consuming()

    def broadcaster(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        ch = conn.channel()
        ch.exchange_declare(exchange='subscribers', exchange_type='fanout')
        while True:
            #print(f"{list(self.insults)}")
            if self.insults:
                insult = random.choice(self.insults)
                ch.basic_publish(exchange='subscribers', routing_key='', body=insult)
                #print(f'Broadcast: {insult}')
            time.sleep(5)

    def activateBroadcast(self):
        global proc
        if proc is None or not proc.is_alive():
            #print("Activating broadcast...")
            proc = multiprocessing.Process(target=self.broadcaster)
            proc.start()
        

    def disableBroadcast(self):
        global proc
        if proc is not None and proc.is_alive():
            #print("Stopping broadcast...")
            proc.terminate()
            proc = None
        

    def listInsults(self, ch, props):
        response = ", ".join(list(self.client.smembers(self.list_insult)))
        ch.basic_publish(exchange='', routing_key=props.reply_to, body=response)

    def insult_me(self, ch,props):
        insults = list(self.client.smembers(self.list_insult))
        if props.reply_to:
            if insults:
                response=random.choice(insults)
                #print("Insult me...")
            else:
                response="NO HI HA INSULTS A LA LLISTA"
            ch.basic_publish(exchange='', routing_key=props.reply_to, body=response)   
            
            
    def on_message(self, ch, method, properties, body):
        msg = body.decode().strip()
        if msg == "1":
            self.activateBroadcast()
        elif msg == "2":
            self.disableBroadcast()
        elif msg == "3":
            self.listInsults(ch, properties)
        elif msg== "4":
            self.insult_me(ch,properties)
        else:
            self.client.sadd(self.list_insult,msg)
            
    
