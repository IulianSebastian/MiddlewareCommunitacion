# XMLRPC IMPORT
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

        # May be is better out of the class
        manager = multiprocessing.Manager()
        listInsult = manager.list()
        proc = None;
        listObservers = manager.list()

        def add_insult(self, insult):
            if insult not in self.listInsult:
                self.listInsult.append(insult)

        def get_insults(self):
            return list(self.listInsult)
        
        def broadcaster(self):
            while True:
                print(self.listInsult)
                choice = random.choice(self.listInsult)
                for ob in self.listObservers:
                    observer = xmlrpc.client.ServerProxy(f"{ob}")
                    observer.notify(choice)
                    print(f"{choice}")
                time.sleep(5)
        
        def activateBroadcast(self):
            if (self.proc is None) or (not self.proc.is_alive()):
                self.proc = multiprocessing.Process(target=self.broadcaster)
                self.proc.start()

        def deactivateBroadcast(self):
            if (self.proc is not None) and (self.proc.is_alive()):
                self.proc.terminate()

        def addObserver(self,url):
            self.listObservers.append(url)
            print(f"This {url} has been added as a suscriber")
        
        def deleteObserver(self,url):
            self.listObservers.remove(url)
            print(f"This {url} has been deleted as a suscriber")

    server.register_instance(InsultServer()) 
    server.serve_forever()
    