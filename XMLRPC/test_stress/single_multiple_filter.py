import matplotlib.pyplot as plt
import multiprocessing
import xmlrpc.client
import random
import time
import numpy as np

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

def xmlrpc_client_multiple(x, y, barrier,nodes):
    for w in range(y):
        nodes.append(nodes.pop(0))
    print(nodes)
    barrier.wait()
    for i in range(x):
        node = nodes.pop(0)
        s = xmlrpc.client.ServerProxy(f'http://localhost:{node}')
        s.send_text(f"What happened {random.choice(insults)}")
        nodes.append(node)


def xmlrpc_client_single(x):
    s = xmlrpc.client.ServerProxy(f'http://localhost:8000')
    for i in range(x):
        s.send_text(f"What happened {random.choice(insults)}")

def execute_service_xmlrpc_single(x):
    processos = []

    # Crear barrera para sincronizar 4 procesos
    start = time.time()

    for i in range(4):
        p = multiprocessing.Process(target=xmlrpc_client_single(x))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()
    
    cont = True
    while cont:
        cont = not (xmlrpc.client.ServerProxy(f'http://localhost:8000').done())

    end = time.time()
    return (end - start)

def execute_service_xmlrpc_multiple(x,nodes):
    processos = []

    # Crear barrera para sincronizar 4 procesos
    barrier = multiprocessing.Barrier(4)
    start = time.time()

    for i in range(4):
        p = multiprocessing.Process(target=xmlrpc_client_multiple, args=(x,(i%len(nodes)), barrier,nodes))
        processos.append(p)
        p.start()

    for node in nodes:
        cont = True
        while cont:
            cont = not (xmlrpc.client.ServerProxy(f'http://localhost:{node}').done())

    for p in processos:
        p.join()

    end = time.time()
    return (end - start)


peticions = [5000, 10000, 20000, 25000, 30000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_xmlrpc_single(pet))

for pet in peticions:
    temps_multiple2.append(execute_service_xmlrpc_multiple(pet,["8080","8083"]))

for pet in peticions:
    temps_multiple3.append(execute_service_xmlrpc_multiple(pet,["8080","8083","8086"]))

print(temps_single)
print(temps_multiple2)
print(temps_multiple3)
print(peticions)

bar_width = 0.2
x_indices = np.arange(len(peticions))
plt.bar(x_indices - bar_width, temps_single, width=bar_width, label='Conjunto 1')
plt.bar(x_indices, temps_multiple2, width=bar_width, label='Conjunto 2')
plt.bar(x_indices + bar_width, temps_multiple3, width=bar_width, label='Conjunto 3')
plt.title('Filter XMLRPC')
plt.xlabel('Peticions')
plt.ylabel('Temps')
plt.xticks(x_indices, peticions)
plt.legend()
plt.show()
