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

def xmlrpc_client_single(x,barrier):
    s = xmlrpc.client.ServerProxy(f'http://localhost:8000')
    barrier.wait()
    for i in range(x):
        s.send_text(f"{random.choice(insults)}")

def execute_service_xmlrpc_single(x):
    processos = []

    start = time.time()
    barrier = multiprocessing.Barrier(4)

    for i in range(4):
        p = multiprocessing.Process(target=xmlrpc_client_single, args=(x,barrier))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()
    
    cont = True
    while cont:
        cont = not (xmlrpc.client.ServerProxy(f'http://localhost:8000').done())

    end = time.time()
    return (end - start)

for insult in insults:
    xmlrpc.client.ServerProxy('http://localhost:8080').add_insult(insult)

peticions = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]
temps_single = []
temps_multiple2 = []
temps_multiple3 = []

for pet in peticions:
    temps_single.append(execute_service_xmlrpc_single(pet))
    print("done")

print("Click enter when the second worker is enabled")
input()

for pet in peticions:
    temps_multiple2.append(execute_service_xmlrpc_single(pet))
    print("done")

print("Click enter when the third worker is enabled")
input()

for pet in peticions:
    temps_multiple3.append(execute_service_xmlrpc_single(pet))
    print("done")

print(temps_single)
print(temps_multiple2)
print(temps_multiple3)
print(peticions)

bar_width = 0.2
x_indices = np.arange(len(peticions))
plt.bar(x_indices - bar_width, temps_single, width=bar_width, label='Single Nodes')
plt.bar(x_indices, temps_multiple2, width=bar_width, label='Two Nodes')
plt.bar(x_indices + bar_width, temps_multiple3, width=bar_width, label='Three Nodes')
plt.title('Filter XMLRPC')
plt.xlabel('Peticions')
plt.ylabel('Temps')
plt.xticks(x_indices, peticions)
plt.legend()
plt.show()

# [53.65223288536072, 106.89030265808105, 156.0953447818756, 204.36031126976013, 255.23085141181946,512.82051,1025.64102,1282.051,1538.46,2051.28,2564.10,5128.205]
# [25.530193567276, 51.16650319099426, 77.31838583946228, 103.09995579719543, 129.2075595855713,258.0645,516.129,645.16129,774.193,1032.258,1290.322,2580.645]
# [17.012640476226807, 34.296138048172, 51.58458495140076, 68.98104357719421, 86.27896118164062,172.413,344.827,431.0344,512.72413,689.655,862.06,1724.13]
# [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]

# [63.30930424,127.334794,193.392978,271.3850815,320.8138845,641.62777,1283.25554,1604.06942,1924.88331,2566.51108,3208.13884,6416.27769]
# [33.47707319,67.63038754,100.3919251,134.3822119,166.5610631,332.00002,664.00004,830.00005,996.00006,1328.00008,1660.00011,3320.00021]
# [22.19178438,45.31132388,68.60233569,90.7766211,115.0101597,230.0000575,460.000115,575.0001438,690.0001725,920.00023,1150.000288,2300.000575]
# [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]