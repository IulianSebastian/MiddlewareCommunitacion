import matplotlib.pyplot as plt
import multiprocessing
import xmlrpc.client
import numpy as np
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
        s.add_insult(f'{random.choice(insults)}')
        nodes.append(node)

def execute_service_xmlrpc_multiple(x,nodes):
    processos = []

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

peticions = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_xmlrpc_multiple(pet,["8080"]))

for pet in peticions:
    temps_multiple2.append(execute_service_xmlrpc_multiple(pet,["8080","8081"]))

for pet in peticions:
    temps_multiple3.append(execute_service_xmlrpc_multiple(pet,["8080","8081","8082"]))


print(temps_single)
print(temps_multiple2)
print(temps_multiple3)
print(peticions)

bar_width = 0.2
x_indices = np.arange(len(peticions))
plt.bar(x_indices - bar_width, temps_single, width=bar_width, label='Single Node')
plt.bar(x_indices, temps_multiple2, width=bar_width, label='Two Nodes')
plt.bar(x_indices + bar_width, temps_multiple3, width=bar_width, label='Three Node')
plt.title('Filter XMLRPC')
plt.xlabel('Peticions')
plt.ylabel('Temps')
plt.xticks(x_indices, peticions)
plt.legend()
plt.show()

# [2.1198649406433105, 4.251526594161987, 6.532921314239502, 8.575620651245117, 11.312185287475586, 23.219210386276245, 46.75034761428833, 62.55429792404175, 77.04675602912903, 98.38518476486206, 124.78290033340454, 258.4212565422058]
# [2.7760169506073, 4.937613010406494, 7.513391017913818, 9.755067586898804, 10.657254219055176, 20.706022024154663, 41.902889013290405, 53.16851043701172, 63.802677154541016, 84.02871346473694, 106.60553932189941, 208.09449195861816]
# [2.224402904510498, 4.244079828262329, 6.351618051528931, 8.337054014205933, 10.659653425216675, 20.736262559890747, 40.720213174819946, 51.66601800918579, 61.56506109237671, 83.4804196357727, 104.66868472099304, 203.93338632583618]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]