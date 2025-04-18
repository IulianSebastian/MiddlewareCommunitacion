import Pyro4
import time
from multiprocessing import Process, Value, Lock

TOTAL_PETICIONS=5000
NUM_PROCESSOS=4
PETICIONS_PER_PROC=5000//4

def spam(counter, lock, total_peticions):
    ns = Pyro4.locateNS()
    uri = ns.lookup("insult.filter")
    server = Pyro4.Proxy(uri)
    
    while counter.value < total_peticions:
        server.send_text("TEXT DE PROVA")
        with lock:
            counter.value += 1

def main():
    counter = Value('i', 0)  
    lock = Lock()

    start_time = time.time()

    procesos = []
    for _ in range(NUM_PROCESSOS):
        p = Process(target=spam, args=(counter, lock, PETICIONS_PER_PROC))
        p.start()
        procesos.append(p)

    for proces in procesos:
        proces.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Temps total d'execució per les 5000 peticions: {elapsed_time} segons")

if __name__ == "__main__":
    main()
