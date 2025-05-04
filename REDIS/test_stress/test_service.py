import matplotlib.pyplot as plot
from itertools import cycle
import multiprocessing
import json
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
        client.publish(next(rr),json.dumps({"pet":f'{random.choice(INSULTS)}'}))

def executar_test(x,nodes):
    processos = []
    client.delete("setInsults")
    client.delete("counter")
    client.set("counter", 0)

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
        for insult in INSULTS: client.publish(name,json.dumps({"pet":insult}))

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

# [1.8284587860107422, 4.280682802200317, 5.786776781082153, 6.965850353240967, 9.184211015701294, 17.587696075439453, 33.59638857841492, 42.83034062385559, 51.20068550109863, 69.49760341644287, 87.7620906829834, 175.61404132843018]
# [1.015014886856079, 2.0003674030303955, 3.19822096824646, 4.806658029556274, 5.122742176055908, 10.341369390487671, 20.97216534614563, 28.162203311920166, 32.13843059539795, 41.77292847633362, 53.14455270767212, 104.60288596153259]
# [0.9052281379699707, 1.8040530681610107, 2.510085344314575, 3.1137263774871826, 4.6769678592681885, 8.15054178237915, 16.356866598129272, 19.47767186164856, 24.521013259887695, 33.257368087768555, 40.03443646430969, 76.89593410491943]