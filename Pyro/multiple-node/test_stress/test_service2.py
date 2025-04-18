import Pyro4
import time
from multiprocessing import Process, Value, Lock
from itertools import cycle

TOTAL_PETICIONS = 5000
NUM_PROCESOS = 4
PETICIONS_PER_PROC = TOTAL_PETICIONS // NUM_PROCESOS

SERVICE_NAMES = ["insult.service1", "insult.service2"]

def spam(counter, lock, n_peticions, service_uris):
    rr_iterator = cycle(service_uris)

    for _ in range(n_peticions):
        uri = next(rr_iterator)
        server = Pyro4.Proxy(uri)
        server.insult_me()
        with lock:
            counter.value += 1

def main():
    counter = Value('i', 0)
    lock = Lock()
    
    ns = Pyro4.locateNS()
    service_uris = []
    
    for name in SERVICE_NAMES:
        uri = ns.lookup(name)
        service_uris.append(uri)

    procesos = []
    start_time = time.time()

    for _ in range(NUM_PROCESOS):
        p = Process(target=spam, args=(counter, lock, PETICIONS_PER_PROC, service_uris))
        p.start()
        procesos.append(p)

    for p in procesos:
        p.join()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Temps total per {TOTAL_PETICIONS} peticions amb {NUM_PROCESOS} processos i {len(service_uris)} serveis: {total_time:.2f} segons")

if __name__ == "__main__":
    main()
