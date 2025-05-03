import Pyro4
import time
from multiprocessing import Process, Value, Lock
from itertools import cycle
from matplotlib import pyplot as plot

SERVICE_NAMES = ["insult.service1", "insult.service2", "insult.service3"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]

def spam(counter, lock, total_peticions, uris):
    rr = cycle(uris)
    while counter.value < total_peticions:
        Pyro4.Proxy(next(rr)).insult_me()
        with lock: counter.value += 1

def inicialitzar_services(service_names):
    ns = Pyro4.locateNS()
    for name in service_names:
        server = Pyro4.Proxy(ns.lookup(name))
        for insult in INSULTS: server.add_insult(insult)

def executar_test(total_peticions, num_processos, service_names):
    ns = Pyro4.locateNS()
    uris = [ns.lookup(name) for name in service_names]
    counter = Value('i', 0)
    lock = Lock()
    processos = []

    inici = time.time()
    for _ in range(num_processos):
        p = Process(target=spam, args=(counter, lock, total_peticions, uris))
        p.start()
        processos.append(p)
    for p in processos: p.join()
    final = time.time()
    temps = final - inici
    print(f"Peticions: {total_peticions}, Processos: {num_processos}, Serveis: {len(service_names)} -> Temps: {final - inici:.2f}s")
    return temps
    
def main():
    inicialitzar_services(SERVICE_NAMES)
    peticions_tests = [5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]
    num_processos = 4
    resultats={}

    for serveis_usats in [SERVICE_NAMES[:1], SERVICE_NAMES[:2], SERVICE_NAMES]:
        print(f"\n-------Test amb {len(serveis_usats)} node(s): {serveis_usats}--------")
        clau = len(serveis_usats)
        resultats[clau] = []
        for total in peticions_tests:
            temps = executar_test(total, num_processos, serveis_usats)
            resultats[clau].append(temps)
    
    for num_nodes, temps_list in resultats.items():
        plot.plot(peticions_tests, temps_list, label=f"{num_nodes} node(s)")

    plot.xlabel("Nombre de peticions")
    plot.ylabel("Temps (segons)")
    plot.title("Escalabilitat segons número de serveis (nodes)")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()  
    
if __name__ == "__main__":
    main()
