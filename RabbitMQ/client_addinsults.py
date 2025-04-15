import pika

insults = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='insultChannel')

for insult in insults:
    channel.basic_publish(exchange='',
                          routing_key='insultChannel',
                          body=insult)
    print(f"Sending insult: {insult}")

connection.close()
