import pika
import time

n=0
text="text num "

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='WorkQueue')



while True:
    channel.basic_publish(exchange='', routing_key='WorkQueue', body=(text+str(n)))
    print(f"New text produced: {text+str(n)}")
    n+=1
    time.sleep(5)
