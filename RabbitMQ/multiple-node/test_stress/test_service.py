import pika
import time
from multiprocessing import Process, Value, Lock
from worker import Worker
from workerFilter import WorkerFilter
from matplotlib import pyplot as plot

INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
WORKQUEUE = "WorkQueue"
INSULTQUEUE = "insultChannel"

def spam(counter, lock, n_peticions):
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()
    q = canal.queue_declare(queue='', exclusive=True).method.queue
    resposta = {"r": None}

    def callback(ch, method, props, body):
        resposta["r"] = body.decode()

    canal.basic_consume(queue=q, on_message_callback=callback, auto_ack=True)

    for _ in range(n_peticions):
        resposta["r"] = None
        canal.basic_publish(
            exchange='',
            routing_key=WORKQUEUE,
            body="Ets un cavero i reusenc",
            properties=pika.BasicProperties(reply_to=q)
        )

        while resposta["r"] is None:
            conn.process_data_events()

        with lock:
            counter.value += 1

    conn.close()

def inicialitzar():
    conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = conn.channel()

    canal.queue_declare(queue=INSULTQUEUE, durable=False)
    canal.queue_purge(queue=INSULTQUEUE)

    for insult in INSULTS:
        canal.basic_publish(exchange='', routing_key=INSULTQUEUE, body=insult)

    conn.close()

def executar_test(total_peticions, num_processos, num_nodes):
    contador = Value('i', 0)
    lock = Lock()
    processos = []
    workers = []

    for _ in range(num_nodes):
        w = Process(target=Worker)
        f = Process(target=WorkerFilter)
        w.start()
        f.start()
        workers.extend([w, f])

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
    peticions_tests = [5000, 10000, 20000, 30000, 40000, 50000, 100000]
    num_processos = 4
    resultats = {}

    for num_nodes in [1, 2, 3]:
        print(f"\n-------Test amb {num_nodes} node(s)--------")
        resultats[num_nodes] = []
        for total in peticions_tests:
            inicialitzar()
            temps = executar_test(total, num_processos, num_nodes)
            resultats[num_nodes].append(temps)

    for num_nodes, temps_list in resultats.items():
        plot.plot(peticions_tests, temps_list, label=f"{num_nodes} node(s)")

    plot.xlabel("Nombre de peticions")
    plot.ylabel("Temps (segons)")
    plot.title("Escalabilitat RabbitMQ segons número de nodes (Worker + Filter)")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()

if __name__ == "__main__":
    main()
