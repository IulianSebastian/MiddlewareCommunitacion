# xmlrpc IMPORT
from xmlrpc.server import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import signal 
import sys

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2')

with SimpleXMLRPCServer(('localhost',8000),requestHandler=RequestHandler,allow_none=True) as server:
    server.register_introspection_functions()

    class InsultFilterServer:
        workers = []

        def get_insults(self):
            list = []
            for worker in self.workers:
                list.append(xmlrpc.client.ServerProxy(f'http://localhost:{worker}').get_insults())
            return list
        
        def add_insult(self,phrase):
            if self.workers:
                work = self.workers.pop(0)
                xmlrpc.client.ServerProxy(f'http://localhost:{work}').work(phrase)
                self.workers.append(work)
            else:
                return 'There are no workers'

        def add_worker(self, port):
            self.workers.append(port)

        def remove_worker(self,port):
            self.workers.remove(port)


    server.register_instance(InsultFilterServer()) 
    server.serve_forever()
    