import Pyro4
import time
ns = Pyro4.locateNS()
uri = ns.lookup("insult.service")
server = Pyro4.Proxy(uri)

list = ["CAVERO", "UCRANIANO", "RUMANO","VENEZOLANO","REUSENC", "MOLARENC"]
for insult in list: 
    print(server.add_insult(insult))
while True:
    print(server.insult_me())
    time.sleep(3)