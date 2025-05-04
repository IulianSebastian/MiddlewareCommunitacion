import pika
import redis

class Filter:
    def __init__(cls):
        cls.channel = pika.BlockingConnection(pika.ConnectionParameters('localhost')).channel()
        cls.channel.queue_declare(queue='filterChannel')
        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        cls.result_queue = cls.channel.queue_declare(queue='', exclusive=True)
        cls.callback_queue = cls.result_queue.method.queue

        for method_frame, properties, cls.body_to_process in cls.channel.consume('filterChannel', inactivity_timeout=1):
            if method_frame:
                cls.on_new_message(cls.body_to_process, properties)
                cls.channel.basic_ack(method_frame.delivery_tag)

    def on_insult_list(method, props, body):
        global response
        global insults
        response = body.decode()
        insults = [item.strip().lower() for item in response.split(",")] # Transformem la cadena rebuda en una llista
        # print(f"Received insult list: {insults}")

    def on_new_message(self,body, props):
        msg = self.body_to_process.decode()
        global response
        if msg == "3":
            response = ", ".join(self.client.lrange("listCensored",0,-1))
            self.channel.basic_publish(exchange='', routing_key=props.reply_to, body=response)
        else:
            response = None
            self.channel.basic_publish(exchange='insultExchange',routing_key='',properties=pika.BasicProperties(reply_to=self.callback_queue),body='3')
            while response is None:
                method_frame, header_frame, body = self.channel.basic_get(self.callback_queue, auto_ack=True)
                if body:
                    self.on_insult_list(method_frame, body)
            msg = self.body_to_process.decode()
            msg = msg.lower()
            for ins in insults:
                msg = msg.replace(ins, "CENSORED")    
            self.client.lpush("listCensored",msg)