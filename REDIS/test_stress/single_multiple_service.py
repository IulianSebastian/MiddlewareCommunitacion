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

def redis_client_multiple(x, y, barrier,nodes):
    for w in range(y):
        nodes.append(nodes.pop(0))
    barrier.wait()
    for i in range(x):
        node = nodes.pop(0)
        client.publish(node,f'{random.choice(insults)}')
        nodes.append(node)

def execute_service_redis_multiple(x,nodes):
    processos = []
    client.delete("setInsults")
    client.delete("counter")

    barrier = multiprocessing.Barrier(4)
    start = time.time()

    for i in range(4):
        p = multiprocessing.Process(target=redis_client_multiple, args=(x,(i%len(nodes)), barrier,nodes))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    con = True
    value = x*4
    while con:
        if (int(client.get("counter")) == value):
            con = False

    end = time.time()
    client.delete("setInsults")
    return (end - start)

peticions = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_redis_multiple(pet,["insultChannel"]))

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
plt.title('Service Redis')
plt.xlabel('Peticions')
plt.ylabel('Temps')
plt.xticks(x_indices, peticions)
plt.legend()
plt.show()

# [1.8406214714050293, 3.4845001697540283, 5.310826063156128, 7.199408054351807, 9.088252305984497, 18.585594177246094, 36.91482090950012, 46.62922167778015, 56.63040804862976, 75.64187908172607, 94.61786341667175, 191.51798367500305]
# [1.3098876476287842, 2.642327070236206, 3.829643487930298, 5.120884895324707, 6.515197038650513, 12.578030109405518, 25.47831082344055, 31.93948531150818, 38.95912218093872, 51.27389693260193, 64.56654286384583, 130.62713289260864]
# [1.0408687591552734, 2.080625534057617, 3.034597635269165, 4.036099672317505, 5.112570762634277, 9.94830870628357, 20.169342279434204, 24.76667356491089, 29.68822479248047, 39.82172393798828, 48.88668966293335, 99.09012842178345]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]
