import pika
import time
from multiprocessing import Process, Value, Lock
from itertools import cycle
import random
from matplotlib import pyplot as plot

SERVEIS = ["insultChannel1", "insultChannel2", "insultChannel3"]
CANALS = ["WorkQueue1", "WorkQueue2", "WorkQueue3"]
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
        canal.basic_publish(exchange='', routing_key=next(rr),
                            properties=pika.BasicProperties(reply_to=q), body='1')
        while resposta["r"] is None:
            conn.process_data_events()
        with lock:
            counter.value += 1

def inicialitzar():
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    for insultservice in SERVEIS:
        for insult in INSULTS:
            canal.basic_publish(exchange='', routing_key=insultservice, body=insult)
    for insultfilter in CANALS:
        canal.basic_publish(exchange='', routing_key=insultfilter, body=f"Hola {random.choice(INSULTS)}")

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

    for p in processos:
        p.join()

    final = time.time()
    print(f"Peticions: {total_peticions}, Processos: {num_processos}, Canals: {len(canals)} -> Temps: {final - inici:.2f}s")
    temps = final - inici
    return temps

def main():
    inicialitzar()
    peticions_tests = [5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]
    num_processos = 4
    resultats={}
    
    for canals_usats in [CANALS[:1], CANALS[:2], CANALS]:  # 1 nodes, 2 nodes, 3 nodes
        print(f"\n--------Test amb {len(canals_usats)} node(s): {canals_usats}-------")
        clau = len(canals_usats)
        resultats[clau] = []
        for total in peticions_tests:
            temps = executar_test(total, num_processos, canals_usats)
            resultats[clau].append(temps)
    
    for num_canals, temps_list in resultats.items():
        plot.plot(peticions_tests, temps_list, label=f"{num_canals} canal(s)")

    plot.xlabel("Nombre de peticions")
    plot.ylabel("Temps (segons)")
    plot.title("Escalabilitat RabbitMQ segons número de nodes")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()

if __name__ == "__main__":
    main()