# xmlrpc IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import multiprocessing
import xmlrpc.client
import random
import time

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',8000),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    class InsultServer:

        manager = multiprocessing.Manager()
        listInsult = manager.list()
        proc = None;
        listObservers = manager.list()

        def add_insult(self, insult):
            print(f"Received Insult : {insult}")
            if insult not in self.listInsult:
                self.listInsult.append(insult)
                return print(f"Added Insult : {insult}")

        def get_insults(self):
            return list(self.listInsult)
        
        def get_insult(self):
            return random.choice(self.listInsult)
        
        def broadcaster(self):
            while True:
                if len(self.listInsult) != 0:
                    choice = random.choice(self.listInsult)
                    for ob in self.listObservers:
                        observer = xmlrpc.client.ServerProxy(f"{ob}")
                        observer.notify(choice)
                        # print(f"Sended the insult {choice} to the observer{ob}")
                    time.sleep(5)
        
        def activateBroadcast(self):
            if (self.proc is None) or (not self.proc.is_alive()):
                self.proc = multiprocessing.Process(target=self.broadcaster)
                self.proc.start()
            return "The Broadcast has been activated"

        def deactivateBroadcast(self):
            if (self.proc is not None) and (self.proc.is_alive()):
                self.proc.terminate()
            return "The Broadcast has been deactivated"

        def addObserver(self,url):
            if url not in self.listObservers:
                self.listObservers.append(url)
            return f"This {url} has been added as a suscriber"
        
        def deleteObserver(self,url):
            if url in self.listObservers:
                self.listObservers.remove(url)
            return f"This {url} has been deleted as a suscriber"

    instance = InsultServer()
    server.register_instance(instance) 
    server.serve_forever()
    
