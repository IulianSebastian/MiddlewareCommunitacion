import pika

result = []
response = None

def on_insult_list(ch, method, props, body):
    global response
    global insults
    response = body.decode()
    insults = [item.strip().lower() for item in response.split(",")] # Transformem la cadena rebuda en una llista
    print(f"Received insult list: {insults}")

def on_new_message(body):
    global response
    response = None  
    channel.basic_publish(exchange='',routing_key='insultChannel',properties=pika.BasicProperties(reply_to=callback_queue),body='3')
    while response is None:
        method_frame, header_frame, body = channel.basic_get(callback_queue, auto_ack=True)
        if body:
            on_insult_list(channel, method_frame, header_frame, body)
            
    msg = body_to_process.decode()
    words = msg.split()
    filtered_words = ["CENSORED" if word.lower() in insults else word for word in words]
    msg_filtered = " ".join(filtered_words)

    print(f"Filtered: {msg_filtered}")
    if msg_filtered not in result:
        result.append(msg_filtered)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='WorkQueue')
result_queue = channel.queue_declare(queue='', exclusive=True)
callback_queue = result_queue.method.queue

print("Waiting for messages...")

for method_frame, properties, body_to_process in channel.consume('WorkQueue', inactivity_timeout=1):
    if method_frame:
        on_new_message(body_to_process)
        channel.basic_ack(method_frame.delivery_tag)
