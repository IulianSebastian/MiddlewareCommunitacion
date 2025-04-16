import pika

connection=pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()

channel.exchange_declare(exchange='subscribers', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='subscribers', queue=queue_name)

print("Waiting for broadcaster...")

def callback(ch, method, properties, body):
    print(f"Insult received with broadcast: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.queue_declare(queue='insultChannel')
channel.basic_publish(exchange='',routing_key='insultChannel', body="1")
channel.start_consuming()