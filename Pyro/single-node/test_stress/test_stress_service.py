import Pyro4
import time
from multiprocessing import Process, Value, Lock

TOTAL_PETICIONS = 5000
NUM_PROCESOS = 4
PETICIONS_PER_PROC = TOTAL_PETICIONS // NUM_PROCESOS

def spam(counter, lock, n_peticions):
    ns = Pyro4.locateNS()
    uri = ns.lookup("insult.service")
    server = Pyro4.Proxy(uri)

    for _ in range(n_peticions):
        server.insult_me()
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
