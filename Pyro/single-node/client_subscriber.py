import Pyro4

@Pyro4.expose
class client:
    def update(self, message):
        print(message)

daemon = Pyro4.Daemon()
ns= Pyro4.locateNS()
uri = daemon.register(client)
ns.register("client1.server", uri) #Registrem un servidor per poder rebre les notificacions relacionades al subject

ns = Pyro4.locateNS()
uri = ns.lookup("insult.service") # Cercem l'observable object amb el mètode lookup de name server
obj = Pyro4.Proxy(uri)
print(obj.subscribe("client1.server")) # Ens subscribim
print(obj.activate_broadcast())

daemon.requestLoop() # Esperem notificacions del subject al nostre servidor client1.server