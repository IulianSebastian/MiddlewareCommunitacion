import pika
import redis

class Filter:
    def __init__(cls):
        cls.channel = pika.BlockingConnection(pika.ConnectionParameters('localhost')).channel()
        cls.channel.queue_declare(queue='insultChannel')
        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        for method_frame, properties, cls.body_to_process in cls.channel.consume('filterChannel', inactivity_timeout=1):
            if method_frame:
                cls.on_new_message(cls.body_to_process, properties)
                cls.channel.basic_ack(method_frame.delivery_tag)

    def on_new_message(self,body, props):
        msg = self.body_to_process.decode()
        if msg == "1":
            list_result=self.client.lrange("listCensored",0,-1) 
            self.channel.basic_publish(exchange='', routing_key=props.reply_to,body=list_result)
        else:
            insults = self.client.smembers("setInsults")           
            msg = self.body_to_process.decode()
            for ins in insults:
                msg = msg.replace(ins, "CENSORED")
            if msg not in self.result:
                self.client.lpush("listCensored",msg)