import matplotlib.pyplot as plot
import multiprocessing
import xmlrpc.client
import random
import time
import numpy as np

SERVICE_PORT = ["8080","8081","8082"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
PETICIONS = [1000,2000]
server_filter = xmlrpc.client.ServerProxy(f'http://localhost:8000')

def spam(x,barrier):
    barrier.wait()
    for _ in range(x):
        server_filter.send_text(f"{random.choice(INSULTS)}")

def executar_test(x):
    processos = []

    start = time.time()
    barrier = multiprocessing.Barrier(4)

    for i in range(4):
        p = multiprocessing.Process(target=spam, args=(x,barrier))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()
    
    cont = True
    while cont:
        cont = not (server_filter.done())

    end = time.time()
    return (end - start)

def inicialitzar_services(service_port):
    for port in service_port:
        client = xmlrpc.client.ServerProxy(f'http://127.0.0.1:{port}')
        for insult in INSULTS: client.add_insult(insult)

def main():
    inicialitzar_services(SERVICE_PORT)
    temps = {}

    for service in range(1,4):
        temps[service] = []
        for pet in PETICIONS:
            temps[service].append(executar_test(pet))
        if (service < 3):
            input(f"Click enter when the {service+1} worker is enabled" )
    
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

# RESULTS First without InsultService
# [53.65223288536072, 106.89030265808105, 156.0953447818756, 204.36031126976013, 255.23085141181946,512.82051,1025.64102,1282.051,1538.46,2051.28,2564.10,5128.205]
# [25.530193567276, 51.16650319099426, 77.31838583946228, 103.09995579719543, 129.2075595855713,258.0645,516.129,645.16129,774.193,1032.258,1290.322,2580.645]
# [17.012640476226807, 34.296138048172, 51.58458495140076, 68.98104357719421, 86.27896118164062,172.413,344.827,431.0344,512.72413,689.655,862.06,1724.13]
# [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]

# [63.30930424,127.334794,193.392978,271.3850815,320.8138845,641.62777,1283.25554,1604.06942,1924.88331,2566.51108,3208.13884,6416.27769]
# [33.47707319,67.63038754,100.3919251,134.3822119,166.5610631,332.00002,664.00004,830.00005,996.00006,1328.00008,1660.00011,3320.00021]
# [22.19178438,45.31132388,68.60233569,90.7766211,115.0101597,230.0000575,460.000115,575.0001438,690.0001725,920.00023,1150.000288,2300.000575]
# [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000,50000,100000]