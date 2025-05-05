import pika
import time
from multiprocessing import Process, Value, Lock
from worker import Worker
from matplotlib import pyplot as plot

INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
QUEUE_NAME = "insultChannel"

def spam(counter, lock, n_peticions):
    resposta = {"r": None}
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    q = canal.queue_declare(queue='', exclusive=True).method.queue

    def callback(ch, method, props, body):
        resposta["r"] = body.decode()

    canal.basic_consume(queue=q, on_message_callback=callback, auto_ack=True)

    for _ in range(n_peticions):
        resposta["r"] = None
        canal.basic_publish(exchange='', routing_key=QUEUE_NAME, properties=pika.BasicProperties(reply_to=q), body='4')

        while resposta["r"] is None:
            conn.process_data_events()

        with lock:
            counter.value += 1

    conn.close()

def inicialitzar():
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    
    canal.queue_declare(queue=QUEUE_NAME, durable=False)
    canal.queue_purge(queue=QUEUE_NAME)

    for insult in INSULTS:
        canal.basic_publish(exchange='', routing_key=QUEUE_NAME, body=insult)
    
    conn.close()


def executar_test(total_peticions, num_processos, num_nodes):
    contador = Value('i', 0)
    lock = Lock()
    processos = []
    workers = []

    for _ in range(num_nodes):
        w = Process(target=Worker)
        w.start()
        workers.append(w)

    peticions_per_proc = total_peticions // num_processos
    inici = time.time()

    for _ in range(num_processos):
        p = Process(target=spam, args=(contador, lock, peticions_per_proc))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()

    final = time.time()

    for w in workers:
        w.terminate()
        w.join()

    print(f"Peticions: {total_peticions}, Clients: {num_processos}, Nodes: {num_nodes} -> Temps: {final - inici:.2f}s")
    return final - inici

def main():
    inicialitzar()
    peticions_tests = [5000, 10000, 20000, 30000, 40000, 50000, 100000]
    num_processos = 4
    resultats = {}

    for num_nodes in [1, 2, 3]: 
        print(f"\n-------Test amb {num_nodes} node(s)--------")
        resultats[num_nodes] = []
        for total in peticions_tests:
            temps = executar_test(total, num_processos, num_nodes)
            resultats[num_nodes].append(temps)

    for num_nodes, temps_list in resultats.items():
        plot.plot(peticions_tests, temps_list, label=f"{num_nodes} node(s)")

    plot.xlabel("Nombre de peticions")
    plot.ylabel("Temps (segons)")
    plot.title("Escalabilitat RabbitMQ segons número de nodes (consumidors)")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()

if __name__ == "__main__":
    main()