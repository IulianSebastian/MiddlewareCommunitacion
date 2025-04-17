import Pyro4
import time
from multiprocessing import Process, Value, Lock

def spam(counter, lock):
    ns = Pyro4.locateNS()
    uri = ns.lookup("insult.service")
    server = Pyro4.Proxy(uri)
    
    while True:
        server.insult_me()
        with lock:
            counter.value += 1
        
def main():
    counter = Value('i', 0)  
    lock = Lock()
    n_peticions=0

    procesos = []
    for _ in range(10):  
        p = Process(target=spam, args=(counter, lock))
        p.start()
        procesos.append(p)

    for _ in range(10):
        time.sleep(1)
        with lock:
            print(f"Peticions per segon: {counter.value}")
            n_peticions+=counter.value
            counter.value = 0
    print(f"Mitja de peticions per segon: {int(n_peticions/10)}")
    
    for proces in procesos:
        proces.terminate()
    
if __name__ == "__main__":
    main()
