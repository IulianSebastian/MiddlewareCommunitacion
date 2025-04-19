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

def redis_client_single(x,f):
    for i in range(x):
        client.publish(insultChannel,f'{random.choice(insults)}{i}_{f}')

def execute_service_redis_single(x):
    processos = []
    start = time.time()

    client.delete("setInsults")

    for i in range(4):
        p = multiprocessing.Process(target=redis_client_single(x,i))
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

peticions = [5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
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

# [10.050384283065796, 19.66714096069336, 40.34549069404602, 51.6276638507843, 62.14417338371277, 79.64058780670166, 105.47357130050659, 208.0698630809784]
# [7.361161470413208, 14.801243305206299, 28.36282730102539, 36.64431405067444, 46.60725116729736, 57.75472116470337, 73.34221863746643, 144.22041082382202]
# [6.037182092666626, 11.763497591018677, 22.980233430862427, 28.807119131088257, 34.28817582130432, 45.06152558326721, 57.09370422363281, 112.00985908508301]
# [5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]