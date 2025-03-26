import Pyro4
import Pyro4.core
import time
import random

@Pyro4.expose
class Service:
    insults=[]
    subscribers=[]
    iteration=0
    def get_insults(self):
        return self.insults
    
    def add_insult(self, insult):
        if insult in self.insults:
            return(f"{insult} is already in list!")
        else:
            self.insults.append(insult)
            return (f"{insult} added!")
        
    def subscribe(self, client):
        if client in self.subscribers:
            return (f"{client} is already registered!")
        else:
            self.subscribers.append(client)
            return (f"{client} subscribed!")
    
    def unsubscribe(self, client):
        if client in self.subscribers:
            self.subscribers.remove(client)
            return(f"Removed {client}")
        else:
            return(f"Error: {client} isn't registered")
    
    def broadcast(self):
        while True:
            random_insult = random.choice(self.insults)
            for sub in self.subscribers:
                print(f"Notifying {sub}...")
                Pyro4.Proxy(f"PYRONAME:{sub}").update(f"Random Insult for subscribers {self.iteration}: {random_insult} ")       
                self.iteration+=1
            time.sleep(5)
    
    
        
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Service)
ns.register("insult.service", uri)
daemon.requestLoop()