import pika
import redis

class Filter:

    def __init__(cls):
        cls.result = []
        cls.response = None

        cls.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        cls.channel = cls.connection.channel()

        cls.channel.queue_declare(queue='insultChannel')
        cls.result_queue = cls.channel.queue_declare(queue='resultQueue', exclusive=True)
        cls.callback_queue = cls.result_queue.method.queue

        cls.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

        # print("Waiting for messages...")

        for method_frame, properties, cls.body_to_process in cls.channel.consume('filterChannel', inactivity_timeout=1):
            if method_frame:
                # print(f'{cls.body_to_process} Que passa')
                cls.on_new_message(cls.body_to_process, properties)
                cls.channel.basic_ack(method_frame.delivery_tag)

    def on_insult_list(ch, method, props, body):
        global response
        global insults
        response = body.decode()
        insults = [item.strip().lower() for item in response.split(",")] # Transformem la cadena rebuda en una llista
        print(f"Received insult list: {insults}")

    def on_new_message(self,body, props):
        msg = self.body_to_process.decode()
        if msg == "1":
            print("Sending result list...")
            list_result = ", ".join(self.result)
            self.channel.basic_publish(exchange='', routing_key=props.reply_to,body=list_result)
        else:
            print("ESTIC AQUI")
            global response
            response = None  
            self.channel.basic_publish(exchange='insultExchange',routing_key='',properties=pika.BasicProperties(reply_to=self.callback_queue),body='3')
            while response is None:
                print(self.result_queue)
                method_frame, header_frame, body = self.channel.basic_get(self.callback_queue, auto_ack=True)
                print(body)
                if body:
                    self.on_insult_list(self.channel, method_frame, header_frame, body)
                    
            msg = self.body_to_process.decode()
            words = msg.split()
            filtered_words = ["CENSORED" if word.lower() in insults else word for word in words]
            msg_filtered = " ".join(filtered_words)
            print("ESTIC AQUI2")
            self.client.lpush("llistafilter",msg_filtered)

            print(f"Filtered: {msg_filtered}")
            if msg_filtered not in self.result:
                self.result.append(msg_filtered)

