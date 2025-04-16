import Pyro4
ns = Pyro4.locateNS()
uri = ns.lookup("insult.service")
server = Pyro4.Proxy(uri)

print(f"Insults: {server.get_insults()}")