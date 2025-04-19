import pika
import time
from multiprocessing import Process, Value, Lock
from itertools import cycle

SERVEIS = ["insultChannel1", "insultChannel2", "insultChannel3"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]

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
        
        while resposta["r"] is None:
            conn.process_data_events()
            
        with lock:
            counter.value += 1

def inicialitzar():
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    
    for servei in SERVEIS:
        for insult in INSULTS:
            canal.basic_publish(exchange='', routing_key=servei, body=insult)

def executar_test(total_peticions, num_processos, canals):
    contador = Value('i', 0)
    lock = Lock()
    processos = []
    peticions_per_proc = total_peticions // num_processos

    inici = time.time()
    for _ in range(num_processos):
        p = Process(target=spam, args=(contador, lock, peticions_per_proc, canals))
        p.start()
        processos.append(p)

    # Esperar que los procesos terminen
    for p in processos:
        p.join()
    
    final = time.time()
    print(f"Peticions: {total_peticions}, Processos: {num_processos}, Canals: {len(canals)} -> Temps: {final - inici:.2f}s")

def main():
    inicialitzar()
    peticions_tests = [5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]
    num_processos = 4

    for canals_usats in [SERVEIS[:1], SERVEIS[:2], SERVEIS]:  # 1 canal, 2 canals, 3 canals
        print(f"\n-------Test amb {len(canals_usats)} node(s): {canals_usats}--------")
        for total in peticions_tests:
            executar_test(total, num_processos, canals_usats)

if __name__ == "__main__":
    main()
