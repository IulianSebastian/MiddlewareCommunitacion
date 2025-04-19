import matplotlib.pyplot as plt
import multiprocessing
import xmlrpc.client
import random
import time

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
        s.add_insult(f'{random.choice(insults)}{i}')
        nodes.append(node)


def xmlrpc_client_single(x):
    s = xmlrpc.client.ServerProxy(f'http://localhost:8080')
    for i in range(x):
        s.add_insult(f'{random.choice(insults)}{i}')


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

    for p in processos:
        p.join()

    end = time.time()
    return (end - start)

peticions = [5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_xmlrpc_single(pet))

for pet in peticions:
    temps_multiple2.append(execute_service_xmlrpc_multiple(pet,["8080","8081"]))

for pet in peticions:
    temps_multiple3.append(execute_service_xmlrpc_multiple(pet,["8080","8081","8082"]))

print(temps_single)
print(temps_multiple2)
print(temps_multiple3)
print(peticions)

plt.plot(peticions, temps_single, marker='o',label='single')
plt.plot(peticions, temps_multiple2, marker='^',label='multiple2')
plt.plot(peticions, temps_multiple3, marker='s',label='multiple3')
plt.title('XMLRPCS')
plt.xlabel('Peticions')
plt.ylabel('Temps')
plt.legend() 
plt.grid(True) 
plt.show() 
