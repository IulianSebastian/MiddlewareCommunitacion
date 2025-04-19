import Pyro4
import time
from multiprocessing import Process, Value, Lock
from itertools import cycle

TOTAL_PETICIONS = 5000
NUM_PROCESSOS = 4
PETICIONS_PER_PROC = TOTAL_PETICIONS // NUM_PROCESSOS
FILTER_NAMES = ["insult.filter1", "insult.filter2", "insult.filter3"]
SERVICE_NAMES = ["insult.service1", "insult.service2", "insult.service3"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO","VENEZOLANO","REUSENC", "MOLARENC"]

def spam(counter, lock, total_peticions, uris):
    rr = cycle(uris)
    while counter.value < total_peticions:
        uri = next(rr)
        server = Pyro4.Proxy(uri)
        server.send_text("TEXT DE PROVA")
        with lock:
            counter.value += 1

def main():
    counter = Value('i', 0)
    lock = Lock()
    ns = Pyro4.locateNS()
    
    for name in SERVICE_NAMES:
        uri = ns.lookup(name)
        server = Pyro4.Proxy(uri)
        for insult in INSULTS:
            server.add_insult(insult)
    
    
    uris = [ns.lookup(name) for name in FILTER_NAMES]

    procesos = []
    start_time = time.time()

    for _ in range(NUM_PROCESSOS):
        p = Process(target=spam, args=(counter, lock, TOTAL_PETICIONS, uris))
        p.start()
        procesos.append(p)

    for proces in procesos:
        proces.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Temps total d'execució per les {TOTAL_PETICIONS} peticions: {elapsed_time} segons")

if __name__ == "__main__":
    main()
