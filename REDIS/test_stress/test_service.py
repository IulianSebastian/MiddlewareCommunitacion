import matplotlib.pyplot as plot
from itertools import cycle
import multiprocessing
import random
import redis
import time

SERVICE_NAMES = ["insultChannel","insultChannel2","insultChannel3"]
INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
PETICIONS = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insultChannel="insultChannel"
setList = "setInsults"

def spam(x, y, barrier,nodes):
    for _ in range(y):
        nodes.append(nodes.pop(0))
    barrier.wait()
    rr = cycle(nodes)
    for _ in range(x):
        client.publish(next(rr),f'{random.choice(INSULTS)}')

def executar_test(x,nodes):
    processos = []
    client.delete("setInsults")
    client.delete("counter")

    barrier = multiprocessing.Barrier(4)
    start = time.time()

    for i in range(4):
        p = multiprocessing.Process(target=spam, args=(x,(i%len(nodes)), barrier,nodes))
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

def inicialitzar_services(service_names):
    for name in service_names:
        for insult in INSULTS: client.publish(name,insult)

def main():
    inicialitzar_services(SERVICE_NAMES)
    temps = {}

    for service in [SERVICE_NAMES[:1],SERVICE_NAMES[:2],SERVICE_NAMES]:
        key = len(service)
        temps[key] = []
        for pet in PETICIONS:
            temps[key].append(executar_test(pet,service))

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

# [1.8406214714050293, 3.4845001697540283, 5.310826063156128, 7.199408054351807, 9.088252305984497, 18.585594177246094, 36.91482090950012, 46.62922167778015, 56.63040804862976, 75.64187908172607, 94.61786341667175, 191.51798367500305]
# [1.3098876476287842, 2.642327070236206, 3.829643487930298, 5.120884895324707, 6.515197038650513, 12.578030109405518, 25.47831082344055, 31.93948531150818, 38.95912218093872, 51.27389693260193, 64.56654286384583, 130.62713289260864]
# [1.0408687591552734, 2.080625534057617, 3.034597635269165, 4.036099672317505, 5.112570762634277, 9.94830870628357, 20.169342279434204, 24.76667356491089, 29.68822479248047, 39.82172393798828, 48.88668966293335, 99.09012842178345]
# [1000, 2000, 3000, 4000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]