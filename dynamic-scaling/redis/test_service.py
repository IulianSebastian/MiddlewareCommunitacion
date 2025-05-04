import matplotlib.pyplot as plot
import multiprocessing
import redis
import pika
import time

INSULTS = ["CAVERO", "UCRANIANO", "MOLARENC", "REUSENC", "RUMANO"]
PETICIONS = [1000,2000,3000,4000,5000,10000,25000, 30000, 40000, 50000, 100000]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def spam(x,barrier):
    connexio = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = connexio.channel()
    canal.exchange_declare(exchange='insultExchange', exchange_type='fanout')

    result_queue = canal.queue_declare(queue='', exclusive=True)
    callback_queue = result_queue.method.queue

    barrier.wait()
    for _ in range(x):
        canal.basic_publish(exchange='insultExchange',routing_key='',properties=pika.BasicProperties(reply_to=callback_queue),body='3')
        body = None
        while body is None:
            method_frame, header_frame, body = canal.basic_get(callback_queue, auto_ack=True)    

def executar_test(x):
    processos = []
    start = time.time()
    
    barrier = multiprocessing.Barrier(4)

    for _ in range(4):
        p = multiprocessing.Process(target=spam, args=(x, barrier))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    end = time.time()
    return (end - start)

def inicialitzar_services():
    for ins in INSULTS:
        client.sadd("setInsults",ins)

def main():
    inicialitzar_services()
    temps = {}
    service = "service"
    temps[service] = []
    for pet in PETICIONS:
        print(f"Fent {pet} amb 4 clients")
        temps[service].append(executar_test(pet))
    
    print(temps)

    plot.plot(PETICIONS, temps[service], label=f"Dynamic Nodes")

    plot.xlabel("Peticions")
    plot.ylabel("Temps (segons)")
    plot.title("Test Stress Service")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()

if __name__ == "__main__":
    main()

# [4.884342670440674, 5.41038966178894, 7.965413331985474, 10.794987201690674, 13.614169359207153, 27.748843908309937, 70.31820511817932, 85.34203910827637, 115.12121725082397, 143.6594202518463, 288.3577506542206]