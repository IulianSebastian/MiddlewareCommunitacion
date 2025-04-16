import Pyro4

@Pyro4.expose
class Filter:  
    def __init__(self):
        self.insults = []
        self.results = []
        ns = Pyro4.locateNS()
        uri = ns.lookup("insult.service")
        self.server = Pyro4.Proxy(uri)
    
    def send_text(self, msg):
        print("Executing send text")
        insults = self.server.get_insults()
        print(insults)
        if insults is not None:
            for insult in insults:
                msg = msg.replace(insult, "CENSORED")
        self.results.append(msg)
        print(f"Returning from send_text: {msg}")
        return f"Message store: {msg}"

    def get_result_list(self):
        return self.results
    
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Filter)
ns.register("insult.filter", uri)
print("Waiting for text...")
daemon.requestLoop()



