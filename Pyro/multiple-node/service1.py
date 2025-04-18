import Pyro4
import Pyro4.core
import time
import random
import multiprocessing

@Pyro4.expose
class Service:
    manager = multiprocessing.Manager()    
    insults= manager.list()
    subscribers=manager.list()
    proces = None
    iteration=0
    def get_insults(self):
        print("Sending insults list...")
        if len(self.insults) == 0: return None
        return list(self.insults)
    
    #For testing server stress
    def insult_me(self):
        if len(self.insults) == 0: return "Insults list is empty"
        print("Insult me...")
        return random.choice(self.insults)
    
    def add_insult(self, insult):
        if insult in self.insults:
            print(f"{insult} is already in list!")
            return(f"{insult} is already in list!")
        else:
            self.insults.append(insult)
            print(f"{insult} added!")
            return (f"{insult} added!")
        
    def subscribe(self, client):
        if client in self.subscribers:
            print(f"{client} is already registered!")
            return (f"{client} is already registered!")
        else:
            self.subscribers.append(client)
            print(f"{client} subscribed!")
            return (f"{client} subscribed!")
    
    def unsubscribe(self, client):
        if client in self.subscribers:
            self.subscribers.remove(client)
            print(f"Removed {client}")
            return(f"Removed {client}")
        else:
            print(f"Error: {client} isn't registered")
            return(f"Error: {client} isn't registered")
    def broadcast(self):
        while True:
            if len(self.insults) != 0:
                random_insult = random.choice(self.insults)
                for sub in self.subscribers:
                    print(f"Notifying {sub}...")
                    Pyro4.Proxy(f"PYRONAME:{sub}").update(f"Random Insult for subscribers {self.iteration}: {random_insult} ")       
                    self.iteration+=1
            time.sleep(5)
            
    def activate_broadcast(self):
        if self.proces == None:
            self.proces = multiprocessing.Process(target=self.broadcast)
            self.proces.start()
            print("Starting pyro broadcast...")
            return ("Starting pyro broadcast...")
        else:
            print("Pyro broadcast is already started")
            return ("Pyro broadcast is already started")
        
    def disable_broadcast(self):
        if self.proces == None:
            print("Pyro broadcast is already disable")
        else:
            print("Finishing pyro broadcast...")
            self.proces.terminate()
            self.proces = None
      

        
daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(Service)
ns.register("insult.service1", uri)
print("Waiting for requests...")
daemon.requestLoop()