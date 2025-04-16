import Pyro4
import time
from multiprocessing import Process, Value, Lock

def spam(counter, lock):
    ns = Pyro4.locateNS()
    uri = ns.lookup("insult.service")
    server = Pyro4.Proxy(uri)
    
    while True:
        try:
            server.insult_me()
            with lock:
                counter.value += 1
        except:
            pass

def main():
    counter = Value('i', 0) 
    lock = Lock()

    procesos = []
    for _ in range(4): 
        p = Process(target=spam, args=(counter, lock))
        p.start()
        procesos.append(p)

    try:
        while True:
            time.sleep(1)
            with lock:
                print(f"Peticions per segon: {counter.value}")
                counter.value = 0
    except KeyboardInterrupt:
        print("Test parat.")

if __name__ == "__main__":
    main()
