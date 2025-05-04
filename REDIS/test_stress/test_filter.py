import matplotlib.pyplot as plot
import multiprocessing
import json
import random
import redis
import time

INSULTS = ["CAVERO", "UCRANIANO", "RUMANO", "VENEZOLANO", "REUSENC", "MOLARENC"]
PETICIONS = [1000,2000,3000,4000,5000, 10000, 20000, 25000, 30000, 40000, 50000, 100000]

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def spam(x,barrier):
    barrier.wait()
    for _ in range(x):
        client.rpush("work_queue",json.dumps({"pet":f'{random.choice(INSULTS)}'}))

def executar_test(x):
    processos = []
    start = time.time()
    
    barrier = multiprocessing.Barrier(4)
    client.delete("listCensored")
    client.delete("counter")
    client.set("counter", 0)

    for _ in range(4):
        p = multiprocessing.Process(target=spam, args=(x, barrier))
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

def inicialitzar_services():
    for insult in INSULTS:
        client.sadd("setInsults", insult)

def main():
    inicialitzar_services()
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
    plot.title("Test Stress Filter")
    plot.legend()
    plot.grid(True)
    plot.tight_layout()
    plot.show()

if __name__ == "__main__":
    main()

# [17.507830142974854, 29.252108812332153, 35.21633791923523, 46.38166666030884, 55.38216161727905, 109.53249287605286, 214.0751495361328, 236.8441252708435, 252.7665467262268, 336.9586009979248, 413.26318526268005, 838.478408575058]
# [5.539689302444458, 11.176070928573608, 16.228638410568237, 19.130950927734375, 24.09040379524231, 49.15814709663391, 101.00695776939392, 125.15039086341858, 150.1943497657776, 198.78561687469482, 251.93161606788635, 501.5364396572113]
# [4.277303695678711, 8.968117713928223, 13.23780632019043, 16.23723864555359, 18.855679988861084, 37.937251329422, 77.30541062355042, 97.66989517211914, 115.98983216285706, 154.1713833808899, 194.22239422798157, 382.7013578414917]