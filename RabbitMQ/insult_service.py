import pika
import time
import random
import multiprocessing

manager = multiprocessing.Manager()
insults = manager.list()  # Lista compartida entre procesos
proc = None

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='insultChannel')
channel.exchange_declare(exchange='subscribers', exchange_type='fanout')

def broadcaster(shared_insults):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = conn.channel()
    ch.exchange_declare(exchange='subscribers', exchange_type='fanout')
    while True:
        print(f"{list(shared_insults)}")
        if shared_insults:
            insult = random.choice(shared_insults)
            ch.basic_publish(exchange='subscribers', routing_key='', body=insult)
            print(f'Broadcast: {insult}')
        time.sleep(5)

def activateBroadcast():
    global proc
    if proc is None or not proc.is_alive():
        print("Activating broadcast...")
        proc = multiprocessing.Process(target=broadcaster, args=(insults,))
        proc.start()
    else:
        print("Broadcast is already active")

def disableBroadcast():
    global proc
    if proc is not None and proc.is_alive():
        print("Stopping broadcast...")
        proc.terminate()
        proc = None
    else:
        print("Broadcast isn't active")

def listInsults(ch, props):
    response = ", ".join(insults)
    print("Sending insult list to", props.reply_to)
    ch.basic_publish(exchange='', routing_key=props.reply_to, body=response)

def on_message(ch, method, properties, body):
    msg = body.decode().strip()
    if msg == "1":
        activateBroadcast()
    elif msg == "2":
        disableBroadcast()
    elif msg == "3":
        listInsults(ch, properties)
    else:
        if msg not in insults:
            insults.append(msg)
            print(f"Added insult: {msg}")
        else:
            print(f"Already exists: {msg}")

channel.basic_consume(queue='insultChannel', on_message_callback=on_message, auto_ack=True)

print("Waiting for messages in 'insultChannel'...")
channel.start_consuming()
