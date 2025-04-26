import pika
import multiprocessing
import time
import random

INSULTS = ["CAVERO", "UCRANIANO", "MOLARENC", "REUSENC", "RUMANO"]

def envia_paquet(velocitat_per_proc, durada_s):
    connexio = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    canal = connexio.channel()
    canal.exchange_declare(exchange='insultExchange', exchange_type='fanout')

    interval = 1.0 / velocitat_per_proc
    t_inici = time.perf_counter()
    t_final = t_inici + durada_s
    enviats = 0

    while time.perf_counter() < t_final:
        ara = time.perf_counter()
        esperats = int((ara - t_inici) / interval)
        while enviats < esperats:
            insult = random.choice(INSULTS)
            canal.basic_publish(exchange='insultExchange', routing_key='insultChannel', body=insult)
            enviats += 1

    connexio.close()

def envia_missatges(velocitat_msgs_per_s, durada_s):
    n_processos = 8
    velocitat_per_proc = velocitat_msgs_per_s // n_processos

    processos = []
    for _ in range(n_processos):
        p = multiprocessing.Process(target=envia_paquet, args=(velocitat_per_proc, durada_s))
        p.start()
        processos.append(p)

    for p in processos:
        p.join()

if __name__ == "__main__":
    for velocitat in [10000, 20000, 30000, 40000]:
        print(f"Test amb {velocitat} missatges/segon")
        envia_missatges(velocitat, 15)
        time.sleep(3)
