import pika
import uuid

def on_response(ch, method, props, body):
    global response
    response = body.decode()
     
response = None
#corr_id = str(uuid.uuid4())
        
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

channel.basic_publish(exchange='', routing_key='insultChannel', properties=pika.BasicProperties(reply_to=callback_queue),body='3')

print("Waiting for insult list...")
while response is None:
    connection.process_data_events() 

print("Insults received:", response)

connection.close()
