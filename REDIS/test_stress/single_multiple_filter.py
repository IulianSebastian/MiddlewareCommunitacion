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

def redis_client_single(x,barrier):
    barrier.wait()
    for i in range(x):
        client.rpush("work_queue",f'{random.choice(insults)}')

def execute_filter_redis_single(x):
    processos = []
    start = time.time()
    
    barrier = multiprocessing.Barrier(4)
    client.delete("listCensored")
    client.delete("counter")

    for i in range(4):
        p = multiprocessing.Process(target=redis_client_single, args=(x, barrier))
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
    return (end - start)

peticions = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_filter_redis_single(pet))

print("Click enter when the second worker is enabled")
input()

for pet in peticions:
    temps_multiple2.append(execute_filter_redis_single(pet))

print("Click enter when the third worker is enabled")
input()

for pet in peticions:
    temps_multiple3.append(execute_filter_redis_single(pet))


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

# [3.0933995246887207, 5.8338401317596436, 9.26704454421997, 12.187772512435913, 15.463058233261108, 31.616037845611572, 61.15545916557312, 77.2257080078125, 94.10784101486206, 123.07536840438843, 156.4419448375702, 302.82459783554077]
# [2.212317943572998, 4.004438877105713, 6.138041257858276, 8.124750852584839, 10.267655611038208, 20.479697227478027, 41.64139223098755, 50.49235987663269, 61.054208517074585, 81.69934916496277, 102.30117750167847, 202.0143439769745]
# [1.6043822765350342, 3.2062199115753174, 4.763687372207642, 6.195982217788696, 7.877846717834473, 16.20200276374817, 31.57068967819214, 39.85153341293335, 47.936761140823364, 64.18114423751831, 79.04687762260437, 168.38964939117432]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]

# [4.069791793823242, 7.934994220733643, 11.957417488098145, 17.582671880722046, 21.692752599716187, 42.998619079589844, 85.0755364894867, 106.29883360862732, 128.3746109008789, 171.30626249313354, 216.95435976982117, 431.3401520252228]
# [2.7870688438415527, 5.5733442306518555, 8.16147518157959, 11.132194757461548, 13.909170389175415, 28.133323669433594, 56.75052809715271, 70.7783796787262, 85.25767588615417, 113.79060745239258, 145.10056972503662, 282.8157572746277]
# [2.176778793334961, 4.3610756397247314, 6.348760604858398, 8.668060779571533, 11.022999286651611, 21.796825170516968, 43.90621256828308, 54.24502754211426, 64.95735096931458, 86.31551432609558, 107.82681369781494, 216.38954520225525]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]