import pika

def on_response(ch, method, props, body):
    global response
    response = body.decode()
     
response = None
        
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

channel.basic_publish(exchange='', routing_key='WorkQueue', properties=pika.BasicProperties(reply_to=callback_queue),body='1')

print("Waiting for text list...")
while response is None:
    connection.process_data_events() 

print("Text received:", response)

connection.close()
