import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import redis
import random
import time

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insultChannel="insultChannel"
setList = "setInsults"

def redis_client_multiple(x, y, barrier,nodes,f):
    for w in range(y):
        nodes.append(nodes.pop(0))
    barrier.wait()
    for i in range(x):
        node = nodes.pop(0)
        client.publish(node,f'{random.choice(insults)}{i}_{f}')
        nodes.append(node)

def redis_client_single(x,f,barrier):
    barrier.wait()
    for i in range(x):
        client.publish(insultChannel,f'{random.choice(insults)}{i}_{f}')

def execute_service_redis_single(x):
    processos = []
    start = time.time()

    # Crear barrera para sincronizar 4 procesos
    barrier = multiprocessing.Barrier(4)
    client.delete("setInsults")

    for i in range(4):
        p = multiprocessing.Process(target=redis_client_single, args=(x, i, barrier))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    con = True
    value = x*4
    while con:
        if (len(client.smembers(setList)) == value):
            con = False

    end = time.time()
    return (end - start)

def execute_service_redis_multiple(x,nodes):
    processos = []
    client.delete("setInsults")

    barrier = multiprocessing.Barrier(4)
    start = time.time()

    for i in range(4):
        p = multiprocessing.Process(target=redis_client_multiple, args=(x,(i%len(nodes)), barrier,nodes,i))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    con = True
    value = x * 4
    while con:
        if (len(client.smembers("setInsults")) == value):
            con = False

    end = time.time()
    client.delete("setInsults")
    return (end - start)

peticions = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_redis_single(pet))

for pet in peticions:
    temps_multiple2.append(execute_service_redis_multiple(pet,["insultChannel","insultChannel2"]))

for pet in peticions:
    temps_multiple3.append(execute_service_redis_multiple(pet,["insultChannel","insultChannel2","insultChannel3"]))


print(temps_single)
print(temps_multiple2)
print(temps_multiple3)
print(peticions)

bar_width = 0.2
x_indices = np.arange(len(peticions))
plt.bar(x_indices - bar_width, temps_single, width=bar_width, label='Single')
plt.bar(x_indices, temps_multiple2, width=bar_width, label='Two Nodes')
plt.bar(x_indices + bar_width, temps_multiple3, width=bar_width, label='Three Nodes')
plt.title('Filter XMLRPC')
plt.xlabel('Peticions')
plt.ylabel('Temps')
plt.xticks(x_indices, peticions)
plt.legend()
plt.show()

# [1.8919258117675781, 3.687692880630493, 5.443915843963623, 7.842932939529419, 9.842177867889404, 19.930978775024414, 38.840205907821655, 51.05766773223877, 58.918275594711304, 79.23307633399963, 99.42939686775208, 195.0894136428833]
# [1.368377685546875, 2.6213228702545166, 3.8944451808929443, 5.181405544281006, 6.516364097595215, 12.740394353866577, 25.945109844207764, 32.85791206359863, 38.8869309425354, 52.85357689857483, 64.93516945838928, 128.33199048042297]
# [0.9808788299560547, 1.9805653095245361, 2.980816125869751, 4.041535139083862, 5.24568247795105, 10.207138776779175, 20.48221445083618, 25.483949184417725, 31.533970832824707, 40.57032036781311, 51.79946446418762, 102.82441806793213]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]