import pika
import time
from multiprocessing import Process, Value, Lock

TOTAL_PETICIONS = 5000
NUM_PROCESOS = 4
PETICIONS_PER_PROC = TOTAL_PETICIONS // NUM_PROCESOS

    
def spam(counter, lock, n_peticions):
    response_holder = {"response": None}
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    result = channel.queue_declare(queue='', exclusive=True)
    callback_queue = result.method.queue

    def on_response(ch, method, props, body):
        response_holder["response"] = body.decode()

    channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

    for _ in range(n_peticions):
        channel.basic_publish(exchange='', routing_key='insultChannel', properties=pika.BasicProperties(reply_to=callback_queue),body='4')
        while response_holder["response"] is None:
            connection.process_data_events() 
        with lock:
            counter.value += 1

def main():
    counter = Value('i', 0)
    lock = Lock()
    
    procesos = []

    start_time = time.time()

    for _ in range(NUM_PROCESOS):
        p = Process(target=spam, args=(counter, lock, PETICIONS_PER_PROC))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()

    end_time = time.time() 

    total_time = end_time - start_time
    print(f"Temps total per {TOTAL_PETICIONS} peticions amb {NUM_PROCESOS} processos: {total_time:.2f} segons")

if __name__ == "__main__":
    main()
