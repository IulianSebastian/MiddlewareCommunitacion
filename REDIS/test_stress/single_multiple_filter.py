import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import random
import redis
import time

insults = [
    "cavero",
    "asshole",
    "dumb",
    "motherfucker"
]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def redis_client_single(x,f):
    for i in range(x):
        client.rpush("work_queue",f'{random.choice(insults)}{i}_{f}')

def execute_service_redis_single(x):
    processos = []
    start = time.time()

    client.delete("listCensored")

    for i in range(4):
        p = multiprocessing.Process(target=redis_client_single(x,i))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    con = True
    value = x*4
    while con:
        if (len(client.lrange("listCensored",0,-1)) == value):
            con = False

    end = time.time()
    return (end - start)

peticions = [5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_redis_single(pet))

print("You have 30 seconds to start the second worker")
time.sleep(30)

for pet in peticions:
    temps_multiple2.append(execute_service_redis_single(pet))

print("You have 30 seconds to start the third worker")
time.sleep(30)

for pet in peticions:
    temps_multiple3.append(execute_service_redis_single(pet))


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
