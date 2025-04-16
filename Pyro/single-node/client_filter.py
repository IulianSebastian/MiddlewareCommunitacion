import Pyro4
import time
ns = Pyro4.locateNS()
uri = ns.lookup("insult.filter")
server = Pyro4.Proxy(uri)

list = ["Hola bon dia", "Bona nit", "NO es no i si es SI torna a preguntar per si de cas","Ets CAVERO i UCRANIANO"]

for text in list: 
    print(f"Sending: {text}")
    msg_store = server.send_text(text)
    print(f"Received: {msg_store}")

print(f"Result list: {server.get_result_list()}")