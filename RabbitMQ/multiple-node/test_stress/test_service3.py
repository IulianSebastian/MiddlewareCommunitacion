import pika
import time
from multiprocessing import Process, Value, Lock
from itertools import cycle

TOTAL_PETICIONS = 5000
NUM_PROCESOS = 4
PETICIONS_PER_PROC = TOTAL_PETICIONS // NUM_PROCESOS
CANALS = ["insultChannel1", "insultChannel2", "insultChannel3"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO","VENEZOLANO","REUSENC", "MOLARENC"]

def spam(counter, lock, n_peticions, canals):
    rr = cycle(canals)
    resposta = {"r": None}
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    q = canal.queue_declare(queue='', exclusive=True).method.queue
    
    def callback(ch, method, props, body): 
        resposta["r"] = body.decode()
        
    canal.basic_consume(queue=q, on_message_callback=callback, auto_ack=True)

    for _ in range(n_peticions):
        resposta["r"] = None
        canal.basic_publish(exchange='', routing_key=next(rr), properties=pika.BasicProperties(reply_to=q), body='4')
        while resposta["r"] is None: conn.process_data_events()
        with lock: counter.value += 1

def main():
    contador = Value('i', 0)
    lock = Lock()
    processos = []
    inici = time.time()
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    for channel in CANALS:
        for insult in INSULTS:
            canal.basic_publish(exchange='', routing_key=channel, body=insult)
        
    for _ in range(NUM_PROCESOS):
        p = Process(target=spam, args=(contador, lock, PETICIONS_PER_PROC, CANALS))
        p.start()
        processos.append(p)

    for p in processos: p.join()
    final = time.time()
    print(f"Temps total per {TOTAL_PETICIONS} peticions amb {NUM_PROCESOS} processos i {len(CANALS)} canals: {final - inici:.2f} segons")

if __name__ == "__main__":
    main()
