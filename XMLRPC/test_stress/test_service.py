import matplotlib.pyplot as plot
from itertools import cycle
import multiprocessing
import xmlrpc.client
import random
import time

SERVICE_PORT = ["8080","8081","8082"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
PETICIONS = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]

def inicialitzar_services(service_port):
    for port in service_port:
        client = xmlrpc.client.ServerProxy(f'http://127.0.0.1:{port}')
        for insult in INSULTS: client.add_insult(insult)

def spam(x, y, barrier,nodes):
    for _ in range(y):
        nodes.append(nodes.pop(0))
    rr = cycle(nodes)
    barrier.wait()
    for i in range(x):
        xmlrpc.client.ServerProxy(f'http://localhost:{next(rr)}').add_insult(f'{random.choice(INSULTS)}')

def executar_test(x,nodes):
    processos = []

    barrier = multiprocessing.Barrier(4)
    start = time.time()

    for i in range(4):
        p = multiprocessing.Process(target=spam, args=(x,(i%len(nodes)), barrier,nodes))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    end = time.time()
    return (end - start)

def main():
    inicialitzar_services(SERVICE_PORT)
    temps = {}

    for service in [SERVICE_PORT[:1],SERVICE_PORT[:2],SERVICE_PORT]:
        key = len(service)
        temps[key] = []
        for pet in PETICIONS:
            temps[key].append(executar_test(pet,service))

    print(temps)

    for i in range(1,4):
        plot.plot(PETICIONS, temps[i], label=f"{i} Nodes")

    plot.xlabel("Peticions")
    plot.ylabel("Temps (segons)")
    plot.title("Test Stress Service")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()

if __name__ == "__main__":
    main()

# Results 
# [2.1198649406433105, 4.251526594161987, 6.532921314239502, 8.575620651245117, 11.312185287475586, 23.219210386276245, 46.75034761428833, 62.55429792404175, 77.04675602912903, 98.38518476486206, 124.78290033340454, 258.4212565422058]
# [2.7760169506073, 4.937613010406494, 7.513391017913818, 9.755067586898804, 10.657254219055176, 20.706022024154663, 41.902889013290405, 53.16851043701172, 63.802677154541016, 84.02871346473694, 106.60553932189941, 208.09449195861816]
# [2.224402904510498, 4.244079828262329, 6.351618051528931, 8.337054014205933, 10.659653425216675, 20.736262559890747, 40.720213174819946, 51.66601800918579, 61.56506109237671, 83.4804196357727, 104.66868472099304, 203.93338632583618]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]